"""Read-only, fresh-per-call CSV tools. Business arithmetic never belongs to the LLM."""
import csv
import json
import hashlib
import re
import unicodedata
from datetime import date, datetime, timezone
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
        if table not in {"products", "categories", "customers", "orders", "order_items", "promotions"}:
            raise ValueError("Unknown table")
        with (self.root / f"desafio_tecnico_ai_eng - {table}.csv").open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def search_products(self, query="", category_id=None, max_price=None, available_only=True, min_price=None):
        """AND token search by product name; optional category and effective price filters."""
        if not isinstance(query, str) or len(query) > 200:
            raise ValueError("query must be a string up to 200 characters")
        if type(available_only) is not bool:
            raise ValueError("available_only must be boolean")
        if category_id is not None and (type(category_id) is not int or not 1 <= category_id <= 9):
            raise ValueError("category_id must be an integer from 1 to 9")
        if category_id is not None:
            generic = {1: {"electric", "guitar", "guitars", "guitarra", "guitarras"},
                       5: {"acoustic", "guitar", "guitars", "violao", "violoes"}}.get(category_id, set())
            generic |= {"for", "a", "an", "beginner", "beginners", "iniciante", "iniciantes", "para"}
            query = " ".join(t for t in normalize(query).split() if t not in generic)
        ceiling = None if max_price is None else Decimal(str(max_price))
        if ceiling is not None and (not ceiling.is_finite() or ceiling < 0):
            raise ValueError("max_price must be a finite non-negative number")
        floor = None if min_price is None else Decimal(str(min_price))
        if floor is not None and (not floor.is_finite() or floor < 0):
            raise ValueError("min_price must be a finite non-negative number")
        if floor is not None and ceiling is not None and floor > ceiling:
            raise ValueError("min_price must not exceed max_price")
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
            promotion_active = bool(discounts)
            effective = Decimal(money(price * (100 - discount) / 100))
            if ceiling is not None and effective > ceiling:
                continue
            if floor is not None and effective < floor:
                continue
            results.append({"product_id": int(row["product_id"]), "name": row["name"],
                            "status": row["status"], "stock_quantity": int(row["stock_quantity"]),
                            "available": available, "list_price_brl": money(price),
                            "discount_percent": str(discount), "price_brl": money(effective),
                            "promotion_active": promotion_active,
                            "pix_price_brl": money(effective if promotion_active else price * Decimal("0.95")),
                            "pix_discount_applied": not promotion_active,
                            "payment_rule": "PIX discount does not apply to promotional prices." if promotion_active else "5% PIX discount available on list price.",
                            "description": row["description"]})
        if not results and query.strip() and category_id is not None:
            # A model may misclassify a named instrument. Exact name evidence wins.
            recovered = self.search_products(query=query, max_price=max_price,
                                             available_only=available_only, min_price=min_price)
            recovered["search_note"] = "No match in requested category; retried name across all categories."
            return recovered
        results.sort(key=lambda r: (Decimal(r["price_brl"]), r["product_id"]))
        return {"source": "products.csv + promotions.csv (provided snapshot, not a live ERP)",
                "queried_at_utc": datetime.now(timezone.utc).isoformat(),
                "total_matches": len(results), "products": results[:10],
                "truncated": len(results) > 10}

    def get_product_details(self, product_id):
        if type(product_id) is not int or product_id < 1:
            raise ValueError("product_id must be a positive integer")
        row = next((r for r in self.rows("products") if int(r["product_id"]) == product_id), None)
        if row is None:
            return {"error": "not_found", "message": "Product not found in the supplied catalog."}
        result = self.search_products(row["name"], available_only=False)
        product = next(p for p in result["products"] if p["product_id"] == product_id)
        product["specs"] = json.loads(row["specs"]) if row["specs"] else {}
        if not isinstance(product["specs"], dict):
            raise ValueError("Product specifications must be a JSON object")
        product["category_id"] = int(row["category_id"])
        product["created_at"] = date.fromisoformat(row["created_at"]).isoformat()
        result["products"] = [product]
        result["total_matches"] = 1
        result["truncated"] = False
        return result

    def get_active_promotions(self):
        ids = {int(r["product_id"]) for r in self.rows("promotions") if r["is_active"] == "1"}
        products = [self.get_product_details(i)["products"][0] for i in sorted(ids)]
        return {"source": "products.csv + promotions.csv (provided snapshot)",
                "products": products, "total_matches": len(products), "truncated": False,
                "warning": "Only explicit is_active flags are used; campaign dates are unavailable."}

    def recommend_products(self, candidate_ids, min_price=None, max_price=None):
        """Select only from a previous, budget-filtered result; recheck availability."""
        candidates = []
        for product_id in candidate_ids:
            result = self.get_product_details(product_id)
            if "products" not in result:
                continue
            p = result["products"][0]
            if min_price is not None and Decimal(p["price_brl"]) < Decimal(str(min_price)):
                continue
            if max_price is not None and Decimal(p["price_brl"]) > Decimal(str(max_price)):
                continue
            description = normalize(p["description"])
            if p["available"] and any(word in description for word in ("iniciante", "estudante", "comecando", "estudo")):
                p["recommendation_basis"] = "The source catalog describes this model for beginners, students, or starting practice."
                if p["specs"].get("strings") == "nylon":
                    p["recommendation_basis"] += " Its recorded string type is nylon."
                candidates.append(p)
        candidates.sort(key=lambda p: Decimal(p["price_brl"]))
        return {"source": "Descriptions and specifications of previous search results, rechecked from products.csv",
                "products": candidates[:3], "total_matches": len(candidates),
                "recommendation": True, "truncated": len(candidates) > 3}

    def order_status(self, order_id, customer_id=None):
        # customer_id comes from the application, NEVER from model arguments or user claims.
        if customer_id is None:
            return {"error": "authentication_required", "message": "Use the store's authenticated channel. An order number alone does not establish ownership."}
        if type(customer_id) is not int or customer_id < 1:
            raise ValueError("Trusted customer identity must be a positive integer")
        if type(order_id) is not int or order_id < 1:
            raise ValueError("order_id must be a positive integer")
        row = next((r for r in self.rows("orders") if int(r["order_id"]) == order_id
                    and int(r["customer_id"]) == customer_id), None)
        if row is None:
            return {"error": "not_found", "message": "Order unavailable for this authenticated customer."}
        products = {r["product_id"]: r["name"] for r in self.rows("products")}
        items = [{"product": products[r["product_id"]], "quantity": int(r["quantity"])}
                 for r in self.rows("order_items") if int(r["order_id"]) == order_id]
        return {"source": "orders.csv + order_items.csv + products.csv (provided snapshot)",
                **{k: row[k] or None for k in ("order_id", "status", "tracking_code", "estimated_delivery")},
                "items": items,
                "warning": "Delivery date is an estimate, not actual receipt. No live carrier integration."}

    def validate_data(self):
        """Validate all six fixtures without modifying originals or returning customer fields."""
        tables = {name: self.rows(name) for name in ("products", "categories", "customers", "orders", "order_items", "promotions")}
        keys = {"products": "product_id", "categories": "category_id", "customers": "customer_id", "orders": "order_id", "promotions": "promotion_id"}
        ids = {}
        for name, key in keys.items():
            values = [int(r[key]) for r in tables[name]]
            if any(v < 1 for v in values) or len(values) != len(set(values)):
                raise ValueError(f"Invalid or duplicate primary key in {name}")
            ids[name] = set(values)
        def foreign(rows, key, target):
            if any(int(row[key]) not in ids[target] for row in rows):
                raise ValueError(f"Broken relationship: {key} -> {target}")
        foreign(tables["products"], "category_id", "categories")
        foreign(tables["orders"], "customer_id", "customers")
        foreign(tables["order_items"], "order_id", "orders")
        foreign(tables["order_items"], "product_id", "products")
        foreign(tables["promotions"], "product_id", "products")
        for row in tables["products"]:
            price = Decimal(row["price_brl"])
            if not price.is_finite() or price < 0 or int(row["stock_quantity"]) < 0:
                raise ValueError("Invalid product price or stock")
            if row["status"] not in {"active", "discontinued", "coming_soon"}:
                raise ValueError("Unknown product status")
            if not isinstance(json.loads(row["specs"] or "{}"), dict):
                raise ValueError("Product specs must be a JSON object")
            date.fromisoformat(row["created_at"])
        for row in tables["orders"]:
            date.fromisoformat(row["order_date"])
            if row["estimated_delivery"]:
                date.fromisoformat(row["estimated_delivery"])
            total = Decimal(row["total_brl"])
            if not total.is_finite() or total < 0:
                raise ValueError("Invalid order total")
            if row["status"] not in {"pending", "confirmed", "shipped", "delivered", "cancelled"}:
                raise ValueError("Unknown order status")
        for row in tables["order_items"]:
            if int(row["quantity"]) < 1:
                raise ValueError("Invalid item quantity")
        for row in tables["promotions"]:
            discount = Decimal(row["discount_percent"])
            if row["is_active"] not in {"0", "1"} or not discount.is_finite() or not 0 <= discount <= 100:
                raise ValueError("Invalid promotion")
        return {"counts": {name: len(rows) for name, rows in tables.items()},
                "warnings": ["Estimated delivery is not receipt date.", "Historical totals are not reconstructed from current catalog prices."]}


class Policies:
    def __init__(self, path):
        from pypdf import PdfReader
        self.pages = [(i + 1, p.extract_text() or "") for i, p in enumerate(PdfReader(path).pages)]
        self.pdf_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def search_policies(self, query):
        if not isinstance(query, str) or not query.strip() or len(query) > 300:
            raise ValueError("query must contain 1-300 characters")
        from .policy_notes import reviewed_notes
        notes = reviewed_notes(query, self.pdf_hash)
        # English semantic hints map to the Portuguese source, without translating its facts.
        aliases = {
            "return": "arrependimento devolucao troca", "refund": "reembolso arrependimento",
            "hours": "horario funcionamento", "address": "endereco rua",
            "payment": "pagamento parcelamento", "installment": "parcelamento parcela",
            "shipping": "frete entrega", "warranty": "garantia defeito",
            "privacy": "privacidade dados", "contact": "telefone whatsapp email",
            "promotion": "promocoes desconto", "accessories": "acessorios",
            "saturday": "sabado horario", "pix": "pix desconto cumulatividade",
            "personaliz": "personalizacao setup elegiveis", "customiz": "personalizacao setup elegiveis",
            "exchange": "trocas preferencia defeito", "tracking": "rastreamento codigo",
            "freight": "frete entrega", "credit": "cartao credito parcela",
        }
        normalized = normalize(query)
        expanded = normalized + " " + " ".join(v for k, v in aliases.items() if k in normalized)
        tokens = set(re.findall(r"[a-z0-9]{3,}", expanded)) - {"the", "and", "what", "how", "for", "can", "you", "are", "uma", "qual", "para", "que", "com"}
        ranked = sorted(((sum(min(normalize(t).count(w), 3) for w in tokens), n, t)
                         for n, t in self.pages), reverse=True)
        chosen = {n: t for score, n, t in ranked[:3] if score > 0}
        for note in notes:
            for n, text in self.pages:
                if n in note["pages"]:
                    chosen[n] = text
        return {"source": "store_policies.pdf, v2.1 June 2025",
                "passages": [{"page": n, "text": t} for n, t in sorted(chosen.items())],
                "reviewed_notes": notes, "pdf_sha256": self.pdf_hash,
                "warning": "Internal policies may conflict. Do not adjudicate legal rights; escalate unclear cases."}
