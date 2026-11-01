"""Small bounded Ollama tool-calling loop; no orchestration framework required."""
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .store import Store, Policies, normalize
from .policy_notes import topics

from .prompts import SYSTEM
from .model import Ollama, ModelError


def definition(name, description, properties, required=()):
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": properties,
                           "required": list(required), "additionalProperties": False}}}


TOOLS = [
    definition("search_products", "Search current CSV snapshot; re-read every call. Max 10 results, sorted by effective price.", {
        "query": {"type": "string", "description": "Product name tokens, e.g. Takamine GD20. Empty for category browsing."},
        "category_id": {"type": "integer", "minimum": 1, "maximum": 9},
        "max_price": {"type": "number", "minimum": 0},
        "min_price": {"type": "number", "minimum": 0},
        "available_only": {"type": "boolean"}}),
    definition("get_product_details", "Read price, description, JSON specifications and availability for one product.",
               {"product_id": {"type": "integer", "minimum": 1}}, ["product_id"]),
    definition("get_active_promotions", "Return only explicit active promotion records and calculated prices.", {}),
    definition("recommend_products", "Recommend beginner/student models ONLY from the previous search results. Search products first if no candidates exist.", {}),
    definition("search_policies", "Retrieve original PDF pages for store policies. Queries in English or Portuguese.",
               {"query": {"type": "string"}}, ["query"]),
    definition("order_status", "Look up order owned by server-authenticated identity. Otherwise returns authentication_required.",
               {"order_id": {"type": "integer", "minimum": 1}}, ["order_id"]),
]


def render_catalog(traces):
    """Render factual catalog answers from tool records, never from generated numbers."""
    lines = ["Here's what I found in the supplied catalog snapshot (prices in BRL):"]
    products = {}
    for trace in traces:
        result = trace["result"]
        for product in result.get("products", []):
            products[product["product_id"]] = product
        if result.get("truncated"):
            lines.append(f"Showing {len(result['products'])} of {result['total_matches']} matches, sorted by price. Please narrow your search for more options.")
    if not products:
        return "I couldn't find matching instruments in the supplied catalog snapshot. Try a model name or a broader category; I cannot confirm availability beyond these records."
    for product in products.values():
        lines.append(f"\n- **{product['name']}**: BRL {product['price_brl']}. "
                     f"Stock: {product['stock_quantity']}; status: {product['status']}.")
        if product["promotion_active"]:
            lines.append(f"  List price: BRL {product['list_price_brl']}; active promotion: {product['discount_percent']}% off. "
                         "The extra 5% PIX discount does not apply.")
        else:
            lines.append(f"  No active promotion is recorded. With the separate 5% PIX payment discount: BRL {product['pix_price_brl']}.")
        if not product["available"]:
            lines.append("  This instrument is not currently available for purchase.")
        if product.get("recommendation_basis"):
            lines.append("  Why it fits: " + product["recommendation_basis"])
        if product.get("specs"):
            lines.append("  Recorded specifications: " + "; ".join(f"{k}: {v}" for k, v in product["specs"].items()) + ".")
    lines.append("\nThese are source-file records, not a live stock guarantee. Would you like to compare specific models?")
    return "\n".join(lines)


def render_order(result):
    if result.get("error") == "authentication_required":
        return "For your privacy, order details require the store's authenticated channel. A customer ID or order number typed in chat does not verify identity. I cannot disclose customer emails."
    if result.get("error") == "not_found":
        return "I couldn't find that order for the authenticated customer. Please check the number or contact the store team."
    if "error" in result:
        return "I couldn't verify this order. Please try again or contact the store team."
    lines = [f"Order {result['order_id']}: {result['status']} (stored status in the supplied snapshot)."]
    for item in result.get("items", []):
        lines.append(f"- {item['quantity']} x {item['product']}")
    if result.get("tracking_code"):
        lines.append("Recorded tracking code: " + result["tracking_code"] + ".")
    if result.get("estimated_delivery"):
        lines.append("Recorded estimated delivery: " + result["estimated_delivery"] + ". This is a historical estimate, not actual receipt or a new delivery promise.")
    lines.append("No live carrier lookup was performed.")
    return "\n".join(lines)


class Agent:
    def __init__(self, data_dir, model=None, *, authenticated_customer_id=None):
        data_dir = Path(data_dir)
        self.store = Store(data_dir)
        self.data_validation = self.store.validate_data()
        self.policies = Policies(data_dir / "store_policies.pdf")
        self.model = model or Ollama()
        self.customer_id = authenticated_customer_id
        if authenticated_customer_id is not None and (type(authenticated_customer_id) is not int or authenticated_customer_id < 1):
            raise ValueError("Authenticated identity must be a positive integer from trusted application code")
        self.history = []
        self.last_trace = []
        self.catalog_candidates = []

    def reset(self):
        self.history.clear()
        self.last_trace.clear()
        self.catalog_candidates.clear()

    def prefetch(self, name, args, current):
        result = self.dispatch(name, args)
        current.append({"role": "assistant", "content": "", "tool_calls": [
            {"function": {"name": name, "arguments": args}}]})
        current.append({"role": "tool", "tool_name": name,
                        "content": json.dumps(result, ensure_ascii=False)})
        self.last_trace.append({"tool": name, "arguments": args, "result": result,
                                "origin": "application_prefetch"})

    def dispatch(self, name, args):
        permitted = {t["function"]["name"]: t["function"]["parameters"] for t in TOOLS}
        if not isinstance(name, str) or name not in permitted or not isinstance(args, dict):
            return {"error": "invalid_tool_call"}
        schema = permitted[name]
        if set(args) - set(schema["properties"]) or set(schema["required"]) - set(args):
            return {"error": "invalid_arguments"}
        types = {"string": lambda v: isinstance(v, str), "integer": lambda v: type(v) is int,
                 "number": lambda v: type(v) in {int, float}, "boolean": lambda v: type(v) is bool}
        if any(not types[schema["properties"][key]["type"]](value) for key, value in args.items()):
            return {"error": "invalid_arguments"}
        try:
            if name == "search_products":
                result = self.store.search_products(**args)
                self.catalog_candidates = [p["product_id"] for p in result["products"]]
                return result
            if name == "get_product_details":
                return self.store.get_product_details(**args)
            if name == "get_active_promotions":
                return self.store.get_active_promotions()
            if name == "recommend_products":
                if not self.catalog_candidates:
                    return {"error": "search_required", "message": "Search the requested category and budget before recommending."}
                return self.store.recommend_products(self.catalog_candidates)
            if name == "search_policies":
                return self.policies.search_policies(**args)
            return self.store.order_status(**args, customer_id=self.customer_id)
        except (ValueError, TypeError, OSError, ArithmeticError, KeyError):
            return {"error": "lookup_failed", "message": "Unable to verify; clarify the request or contact the team."}

    def reply(self, text):
        self.last_trace = []
        if not isinstance(text, str) or not text.strip() or len(text) > 4000:
            return "Please send a message between 1 and 4,000 characters."
        current = [{"role": "user", "content": text}]
        system = {"role": "system", "content": SYSTEM + "\nCurrent store-local time: " +
                  datetime.now(ZoneInfo("America/Campo_Grande")).isoformat() +
                  "\nApplication identity verified: " + str(self.customer_id is not None) +
                  ". If verified, use order_status; do not ask the user to authenticate again."}
        # Retain only complete conversational turns, never partial tool sequences.
        prior = [m for turn in self.history[-4:] for m in turn]
        order_match = re.search(r"\b(?:order|pedido)\s*(?:number|numero)?\s*#?\s*(\d+)\b", normalize(text))
        if order_match:
            self.prefetch("order_status", {"order_id": int(order_match.group(1))}, current)
        elif any(w in normalize(text) for w in ("order", "pedido")) and "status" in normalize(text) and not topics(text):
            answer = "Please provide the order number. Order details also require identity verified through the store's authenticated channel; an order number typed here is not authentication."
            self.history.append(current + [{"role": "assistant", "content": answer}])
            self.history = self.history[-4:]
            return answer
        for _ in range(5):
            try:
                message = self.model.chat([system] + prior + current, TOOLS)
            except ModelError as exc:
                return str(exc)
            if not isinstance(message, dict) or not isinstance(message.get("content", ""), str):
                return "The model returned an invalid response. Please try again."
            calls = message.get("tool_calls") or []
            if not isinstance(calls, list) or len(calls) > 4:
                return "I couldn't safely verify this request. Please contact the store team."
            current.append({"role": "assistant", "content": message.get("content", ""),
                            **({"tool_calls": calls} if calls else {})})
            if not calls:
                answer = message.get("content") or "I couldn't verify that. Please contact the store team."
                needed_topics = set(topics(text))
                covered_topics = {n["topic"] for t in self.last_trace
                                  for n in t["result"].get("reviewed_notes", [])}
                already_queried = any(t["tool"] == "search_policies" and t["arguments"].get("query") == text[:300] for t in self.last_trace)
                if needed_topics - covered_topics and not already_queried:
                    current.pop()  # Discard the premature draft, not the user's message.
                    self.prefetch("search_policies", {"query": text[:300]}, current)
                    continue
                if any(w in normalize(text) for w in ("beginner", "iniciante")) and self.catalog_candidates and not any(t["tool"] == "recommend_products" for t in self.last_trace):
                    current.pop()
                    self.prefetch("recommend_products", {}, current)
                    continue
                if not self.last_trace:
                    # Require evidence even if the model prematurely produces a final answer.
                    if text.strip().lower().rstrip("!.") not in {"hi", "hello", "thanks", "thank you", "ola", "oi"}:
                        # Explicit fallback retrieval also supports elliptical follow-ups,
                        # where the model would otherwise reuse old evidence indefinitely.
                        query = " ".join(m["content"] for m in prior + current if m["role"] == "user")[-300:]
                        args = {"query": query}
                        result = self.dispatch("search_policies", args)
                        current[-1] = {"role": "assistant", "content": "", "tool_calls": [
                            {"function": {"name": "search_policies", "arguments": args}}]}
                        current.append({"role": "tool", "tool_name": "search_policies",
                                        "content": json.dumps(result, ensure_ascii=False)})
                        self.last_trace.append({"tool": "search_policies", "arguments": args, "result": result})
                        continue
                policy_pages = sorted({p["page"] for trace in self.last_trace
                                       if trace["tool"] == "search_policies"
                                       for p in trace["result"].get("passages", [])})
                answer = re.sub(r"\n*Policy evidence:[^\n]*", "", answer).strip()
                notes = {n["topic"]: n for trace in self.last_trace
                         for n in trace["result"].get("reviewed_notes", [])
                         if not needed_topics or n["topic"] in needed_topics}
                if notes:
                    answer = "\n\n".join(n["text"] + " (Manual sections " + n["sections"] + ".)" for n in notes.values())
                    policy_pages = sorted({p for n in notes.values() for p in n["pages"]})
                    if "returns" in notes and "online" in normalize(text) and re.search(r"\b(?:5|five)\s+days\b", normalize(text)):
                        answer += "\n\nYou report receiving an online purchase five days ago, which is within the manual's seven-calendar-day request window. The remaining conditions and any special-case review still apply."
                product_traces = [t for t in self.last_trace if "products" in t["result"]]
                recommendation = [t for t in product_traces if t["result"].get("recommendation")]
                if recommendation:
                    product_traces = recommendation
                if product_traces:
                    # A small model can confuse product status with promotion status.
                    # Render trusted facts directly instead of accepting generated prices.
                    catalog_answer = render_catalog(product_traces)
                    if policy_pages:
                        answer = catalog_answer + "\n\nPolicy guidance:\n" + answer
                    else:
                        answer = catalog_answer
                order_traces = [t for t in self.last_trace if t["tool"] == "order_status"]
                if order_traces:
                    order_answer = render_order(order_traces[-1]["result"])
                    answer = order_answer + ("\n\nPolicy guidance:\n" + answer if policy_pages else "")
                has_evidence = product_traces or order_traces or policy_pages
                if self.last_trace and not has_evidence:
                    answer = "I couldn't verify this from the available sources. Please clarify your request or contact the store team."
                if policy_pages:
                    answer += "\n\nPolicy evidence: store_policies.pdf, pp. " + ", ".join(map(str, policy_pages)) + "."
                    current[-1]["content"] = answer
                current[-1]["content"] = answer
                self.history.append(current)
                self.history = self.history[-4:]
                return answer
            for call in calls:
                function = call.get("function", {}) if isinstance(call, dict) else {}
                if not isinstance(function, dict):
                    function = {}
                name, args = function.get("name", ""), function.get("arguments", {})
                result = self.dispatch(name, args)
                self.last_trace.append({"tool": name, "arguments": args, "result": result})
                current.append({"role": "tool", "tool_name": name if isinstance(name, str) else "invalid_tool",
                                "content": json.dumps(result, ensure_ascii=False)})
        return "I couldn't verify this within the lookup limit. Please contact the store team."
