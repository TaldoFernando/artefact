import csv
import json
import tempfile
import unittest
from pathlib import Path
from shutil import copytree

from emporio.agent import Agent, ModelError, Ollama
from emporio.store import Policies, Store

DATA = Path(__file__).resolve().parents[1] / "data"


def tool(name, **arguments):
    return {"role": "assistant", "content": "", "tool_calls": [
        {"function": {"name": name, "arguments": arguments}}]}


class ScriptedModel:
    """Protocol fixture, not a replacement for evaluating the real LLM."""
    def __init__(self, *messages):
        self.responses = iter(messages)
        self.requests = []

    def chat(self, messages, tools):
        self.requests.append(messages)
        return next(self.responses)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(DATA)

    def test_budget_category_and_stock(self):
        result = self.store.search_products(category_id=5, max_price=1000)
        self.assertGreater(result["total_matches"], 0)
        for p in result["products"]:
            self.assertLessEqual(float(p["price_brl"]), 1000)
            self.assertGreater(p["stock_quantity"], 0)
            self.assertEqual(p["status"], "active")

    def test_exact_model_and_expired_promotion(self):
        p = self.store.search_products("Takamine GD20")["products"][0]
        self.assertEqual(p["price_brl"], "2199.00")
        self.assertEqual(p["discount_percent"], "0")
        self.assertEqual(p["pix_price_brl"], "2089.05")

    def test_active_promotion_does_not_stack_pix(self):
        p = next(p for p in self.store.search_products("", available_only=False)["products"]
                 if p["product_id"] == 127)
        self.assertEqual(p["discount_percent"], "10")
        self.assertEqual(p["price_brl"], p["pix_price_brl"])

    def test_unavailable_and_discontinued(self):
        rows = self.store.rows("products")
        for row in rows:
            if row["status"] != "active" or int(row["stock_quantity"]) <= 0:
                self.assertEqual(self.store.search_products(row["name"])["total_matches"], 0)
                self.assertEqual(self.store.search_products(row["name"], available_only=False)["total_matches"], 1)

    def test_reloads_modified_source(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "data"
            copytree(DATA, target)
            store = Store(target)
            self.assertEqual(store.search_products("Takamine GD20")["total_matches"], 1)
            path = target / "desafio_tecnico_ai_eng - products.csv"
            rows = store.rows("products")
            next(r for r in rows if r["product_id"] == "95")["stock_quantity"] = "0"
            with path.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            self.assertEqual(store.search_products("Takamine GD20")["total_matches"], 0)

    def test_invalid_filters(self):
        for value in [-1, "NaN", "Infinity"]:
            with self.assertRaises(ValueError):
                self.store.search_products(max_price=value)

    def test_unknown_model(self):
        self.assertEqual(self.store.search_products("imaginary model")["total_matches"], 0)

    def test_wrong_category_does_not_hide_named_product(self):
        result = self.store.search_products("Takamine GD20", category_id=1)
        self.assertEqual(result["products"][0]["product_id"], 95)
        self.assertIn("search_note", result)

    def test_order_requires_authentication(self):
        self.assertEqual(self.store.order_status(1)["error"], "authentication_required")

    def test_order_ownership_and_minimization(self):
        self.assertEqual(self.store.order_status(1, customer_id=7)["error"], "not_found")
        result = self.store.order_status(1, customer_id=3)
        self.assertEqual(result["status"], "delivered")
        self.assertNotIn("customer_id", result)
        self.assertNotIn("notes", result)
        self.assertNotIn("actual_delivery", result)


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policies = Policies(DATA / "store_policies.pdf")

    def test_english_returns_query_finds_original_policy(self):
        results = self.policies.search_policies("online return refund")
        self.assertIn(4, [p["page"] for p in results["passages"]])
        self.assertTrue(any("sete" in p["text"] for p in results["passages"]))

    def test_hours_and_address(self):
        for query in ["hours", "address"]:
            self.assertIn(2, [p["page"] for p in self.policies.search_policies(query)["passages"]])

    def test_empty_query(self):
        with self.assertRaises(ValueError):
            self.policies.search_policies("")


class AgentTests(unittest.TestCase):
    def test_tool_roundtrip_and_history(self):
        model = ScriptedModel(tool("search_products", query="Takamine GD20"),
                              {"content": "BRL 2,199.00"}, {"content": "Anything else?"})
        agent = Agent(DATA, model)
        answer = agent.reply("Price of Takamine GD20?")
        self.assertIn("BRL 2199.00", answer)
        self.assertIn("No active promotion", answer)
        evidence = json.loads(model.requests[1][-1]["content"])
        self.assertEqual(evidence["products"][0]["price_brl"], "2199.00")
        agent.reply("Thanks")
        self.assertTrue(any(m["role"] == "tool" for m in model.requests[2]))

    def test_model_cannot_choose_identity(self):
        agent = Agent(DATA, ScriptedModel())
        result = agent.dispatch("order_status", {"order_id": 1, "customer_id": 3})
        self.assertEqual(result["error"], "invalid_arguments")
        self.assertEqual(agent.dispatch("order_status", {"order_id": 1})["error"], "authentication_required")

    def test_unknown_tool_and_invalid_args(self):
        agent = Agent(DATA, ScriptedModel())
        self.assertEqual(agent.dispatch("execute_sql", {"sql": "DROP TABLE products"})["error"], "invalid_tool_call")
        self.assertEqual(agent.dispatch("search_policies", {})["error"], "invalid_arguments")
        self.assertEqual(agent.dispatch("search_products", {"available_only": "false"})["error"], "invalid_arguments")

    def test_tool_loop_is_bounded(self):
        agent = Agent(DATA, ScriptedModel(*[tool("search_products") for _ in range(5)]))
        self.assertIn("lookup limit", agent.reply("Find a guitar"))
        self.assertEqual(len(agent.last_trace), 5)
        self.assertEqual(agent.history, [])

    def test_provider_failure_is_visible(self):
        class BrokenModel:
            def chat(self, messages, tools):
                raise ModelError("Ollama unavailable")
        agent = Agent(DATA, BrokenModel())
        self.assertEqual(agent.reply("Hello"), "Ollama unavailable")
        self.assertEqual(agent.history, [])

    def test_memory_bounded_to_complete_turns(self):
        agent = Agent(DATA, ScriptedModel(*[{"content": "Hello"}] * 7))
        for _ in range(7):
            agent.reply("Hi")
        self.assertEqual(len(agent.history), 4)

    def test_input_limit(self):
        agent = Agent(DATA, ScriptedModel())
        self.assertIn("4,000", agent.reply("x" * 4001))

    def test_ungrounded_answer_triggers_lookup(self):
        model = ScriptedModel({"content": "The store is always open."},
                              tool("search_policies", query="hours"),
                              {"content": "Regular hours are on page 2."})
        agent = Agent(DATA, model)
        answer = agent.reply("When is the store open?")
        self.assertNotIn("always open", answer)
        self.assertIn("Policy evidence", answer)
        self.assertEqual(agent.last_trace[0]["tool"], "search_policies")


if __name__ == "__main__":
    unittest.main()
