"""Verify tool records/provenance against fixtures; this is not semantic LLM grading."""
import argparse
import csv
import hashlib
import json
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = json.loads(args.run.read_text())
    if "source_review" in run:
        immutable = [(s["id"], [(t["phase"], t["trusted_fixture_id"], t["message"], t["response"], t["trace"]) for t in s["turns"]]) for s in run["scenarios"]]
        digest = hashlib.sha256(json.dumps(immutable, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        assert digest == run["source_review"]["unchanged_messages_responses_traces_sha256"], "Reviewed response content changed"
    tables = {}
    for name in ("products", "promotions", "orders", "order_items", "customers"):
        with (ROOT / "data" / f"desafio_tecnico_ai_eng - {name}.csv").open(encoding="utf-8-sig", newline="") as f:
            tables[name] = list(csv.DictReader(f))
    products = {int(r["product_id"]): r for r in tables["products"]}
    orders = {int(r["order_id"]): r for r in tables["orders"]}
    commit = run["metadata"]["base_commit"]
    for file, expected in run["metadata"]["code_sha256"].items():
        committed = subprocess.check_output(["git", "show", f"{commit}:{file}"], cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest() == expected, f"Recorded source differs from commit: {file}"
    checked_products = checked_orders = turns = 0
    def cash(value):
        return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    for scenario in run["scenarios"]:
        for turn in scenario["turns"]:
            turns += 1
            answer = turn["response"]
            for customer in tables["customers"]:
                for field in ("name", "email", "phone"):
                    assert customer[field] not in answer, "A private customer field appeared in a response"
            for trace in turn["trace"]:
                result = trace["result"]
                for p in result.get("products", []):
                    original = products[p["product_id"]]
                    assert p["name"] == original["name"]
                    assert p["description"] == original["description"]
                    assert p["stock_quantity"] == int(original["stock_quantity"])
                    assert p["status"] == original["status"]
                    discounts = [Decimal(row["discount_percent"]) for row in tables["promotions"] if int(row["product_id"]) == p["product_id"] and row["is_active"] == "1"]
                    discount = max(discounts, default=Decimal(0))
                    price = Decimal(original["price_brl"])
                    effective = cash(price * (100 - discount) / 100)
                    assert p["list_price_brl"] == cash(price)
                    assert p["price_brl"] == effective
                    assert p["pix_price_brl"] == (effective if discounts else cash(price * Decimal("0.95")))
                    assert p["promotion_active"] == bool(discounts)
                    if "specs" in p:
                        assert p["specs"] == json.loads(original["specs"])
                    checked_products += 1
                if trace["tool"] == "order_status" and "status" in result:
                    original = orders[int(result["order_id"])]
                    assert int(original["customer_id"]) == turn["trusted_fixture_id"]
                    for key in ("status", "tracking_code", "estimated_delivery"):
                        assert result[key] == (original[key] or None)
                    expected_items = [{"product": products[int(r["product_id"])]["name"], "quantity": int(r["quantity"])} for r in tables["order_items"] if int(r["order_id"]) == int(result["order_id"])]
                    assert result["items"] == expected_items
                    checked_orders += 1
    print(json.dumps({"run": args.run.name, "source_commit_verified": commit,
                      "turns_checked_for_customer_field_leaks": turns,
                      "product_records_verified": checked_products,
                      "owned_order_records_verified": checked_orders,
                      "result": "PASS: record parity and provenance only; semantic review remains separate"}, indent=2))


if __name__ == "__main__":
    main()
