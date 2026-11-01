"""Read-only, fresh-per-call CSV tools. Business arithmetic never belongs to the LLM."""
import csv
import re
import unicodedata
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower())
                   if not unicodedata.combining(c))


def money(value):
    return str(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class Store:
    def __init__(self, root: Path):
        self.root = root

    def rows(self, table):
        with (self.root / f"desafio_tecnico_ai_eng - {table}.csv").open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def search_products(self, query="", category_id=None, max_price=None, available_only=True):
        """AND token search by product name; optional category and effective price filters."""
        if not isinstance(query, str) or len(query) > 200:
            raise ValueError("query must be a string up to 200 characters")
        if type(available_only) is not bool:
            raise ValueError("available_only must be boolean")
        if category_id is not None and (type(category_id) is not int or not 1 <= category_id <= 9):
            raise ValueError("category_id must be an integer from 1 to 9")
        ceiling = None if max_price is None else Decimal(str(max_price))
        if ceiling is not None and (not ceiling.is_finite() or ceiling < 0):
            raise ValueError("max_price must be a finite non-negative number")
        promotions = self.rows("promotions")
        results = []
        for row in self.rows("products"):
            if any(t not in normalize(row["name"]) for t in normalize(query).split()):
                continue
            if category_id is not None and int(row["category_id"]) != category_id:
                continue
            available = row["status"] == "active" and int(row["stock_quantity"]) > 0
            if available_only and not available:
                continue
            price = Decimal(row["price_brl"])
            discounts = [Decimal(p["discount_percent"]) for p in promotions
                         if p["product_id"] == row["product_id"] and p["is_active"] == "1"]
            discount = max(discounts, default=Decimal(0))
            effective = Decimal(money(price * (100 - discount) / 100))
            if ceiling is not None and effective > ceiling:
                continue
            results.append({"product_id": int(row["product_id"]), "name": row["name"],
                            "status": row["status"], "stock_quantity": int(row["stock_quantity"]),
                            "available": available, "list_price_brl": money(price),
                            "discount_percent": str(discount), "price_brl": money(effective),
                            "promotion_active": bool(discount),
                            "pix_price_brl": money(effective if discount else price * Decimal("0.95")),
                            "pix_discount_applied": not bool(discount),
                            "payment_rule": "PIX discount does not apply to promotional prices." if discount else "5% PIX discount available on list price.",
                            "description": row["description"]})
        if not results and query.strip() and category_id is not None:
            # A model may misclassify a named instrument. Exact name evidence wins.
            recovered = self.search_products(query=query, max_price=max_price,
                                             available_only=available_only)
            recovered["search_note"] = "No match in requested category; retried name across all categories."
            return recovered
        results.sort(key=lambda r: (Decimal(r["price_brl"]), r["product_id"]))
        return {"source": "products.csv + promotions.csv (provided snapshot, not a live ERP)",
                "queried_at_utc": datetime.now(timezone.utc).isoformat(),
                "total_matches": len(results), "products": results[:10],
                "truncated": len(results) > 10}

    def order_status(self, order_id, customer_id=None):
        # customer_id comes from the application, NEVER from model arguments or user claims.
        if customer_id is None:
            return {"error": "authentication_required", "message": "Use the store's authenticated channel. An order number alone does not establish ownership."}
        if type(order_id) is not int or order_id < 1:
            raise ValueError("order_id must be a positive integer")
        row = next((r for r in self.rows("orders") if int(r["order_id"]) == order_id
                    and int(r["customer_id"]) == customer_id), None)
        if row is None:
            return {"error": "not_found", "message": "Order unavailable for this authenticated customer."}
        return {"source": "orders.csv (provided snapshot)",
                **{k: row[k] or None for k in ("order_id", "status", "tracking_code", "estimated_delivery")},
                "warning": "Delivery date is an estimate, not actual receipt. No live carrier integration."}


class Policies:
    def __init__(self, path):
        from pypdf import PdfReader
        self.pages = [(i + 1, p.extract_text() or "") for i, p in enumerate(PdfReader(path).pages)]

    def search_policies(self, query):
        if not isinstance(query, str) or not query.strip() or len(query) > 300:
            raise ValueError("query must contain 1-300 characters")
        # English semantic hints map to the Portuguese source, without translating its facts.
        aliases = {
            "return": "arrependimento devolucao troca", "refund": "reembolso arrependimento",
            "hours": "horario funcionamento", "address": "endereco rua",
            "payment": "pagamento parcelamento", "installment": "parcelamento parcela",
            "shipping": "frete entrega", "warranty": "garantia defeito",
            "privacy": "privacidade dados", "contact": "telefone whatsapp email",
            "promotion": "promocoes desconto", "accessories": "acessorios",
        }
        normalized = normalize(query)
        expanded = normalized + " " + " ".join(v for k, v in aliases.items() if k in normalized)
        tokens = set(re.findall(r"[a-z0-9]{3,}", expanded)) - {"the", "and", "what", "how", "for", "can", "you", "are", "uma", "qual", "para", "que", "com"}
        ranked = sorted(((sum(min(normalize(t).count(w), 3) for w in tokens), n, t)
                         for n, t in self.pages), reverse=True)
        return {"source": "store_policies.pdf, v2.1 June 2025",
                "passages": [{"page": n, "text": t} for score, n, t in ranked[:3] if score > 0],
                "warning": "Internal policies may conflict. Do not adjudicate legal rights; escalate unclear cases."}
