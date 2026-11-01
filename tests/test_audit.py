"""Audit regressions. Scripted models verify protocol, never real-LLM reasoning."""
import csv
import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from shutil import copytree
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from emporio.agent import Agent, ModelError, Ollama
from emporio.store import Store
from test_agent import DATA, ScriptedModel, tool


class DataAndToolsTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(DATA)

    def test_all_six_fixtures_and_relationships(self):
        self.assertEqual(self.store.validate_data()["counts"], {
            "products": 65, "categories": 9, "customers": 50,
            "orders": 20, "order_items": 22, "promotions": 25})

    def test_invalid_foreign_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "data"
            copytree(DATA, root)
            file = root / "desafio_tecnico_ai_eng - products.csv"
            rows = self.store.rows("products")
            rows[0]["category_id"] = "999"
            with file.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0])
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "Broken relationship"):
                Store(root).validate_data()

    def test_details_include_json_specs_and_description(self):
        p = self.store.get_product_details(81)["products"][0]
        self.assertEqual(p["specs"]["strings"], "nylon")
        self.assertEqual(p["category_id"], 5)
        self.assertTrue(p["description"])
        self.assertEqual(self.store.get_product_details(99999)["error"], "not_found")

    def test_active_promotions_exactly_match_flags(self):
        expected = {int(r["product_id"]) for r in self.store.rows("promotions") if r["is_active"] == "1"}
        result = self.store.get_active_promotions()
        self.assertEqual({p["product_id"] for p in result["products"]}, expected)
        self.assertTrue(all(p["promotion_active"] for p in result["products"]))

    def test_price_range(self):
        result = self.store.search_products(category_id=5, min_price=600, max_price=800)
        self.assertTrue(result["products"])
        self.assertTrue(all(600 <= float(p["price_brl"]) <= 800 for p in result["products"]))
        with self.assertRaises(ValueError):
            self.store.search_products(min_price=800, max_price=600)

    def test_unknown_and_foreign_orders_are_indistinguishable(self):
        self.assertEqual(self.store.order_status(99999, 2), self.store.order_status(1, 2))

    def test_valid_order_joins_items_without_customer_fields(self):
        result = self.store.order_status(8, 2)
        self.assertEqual(result["status"], "shipped")
        self.assertEqual(result["tracking_code"], "BRJL5544332BR")
        self.assertEqual(len(result["items"]), 1)
        for field in ("email", "phone", "customer_id", "name", "notes"):
            self.assertNotIn(field, result)
        with self.assertRaises(ValueError):
            self.store.order_status(8, True)

    def test_recommendations_stay_in_prior_results(self):
        prior = self.store.search_products(category_id=5, max_price=1000)["products"]
        ids = {p["product_id"] for p in prior}
        recommended = self.store.recommend_products(ids)["products"]
        self.assertTrue(recommended)
        self.assertTrue(all(p["product_id"] in ids and float(p["price_brl"]) <= 1000 for p in recommended))
        self.assertTrue(all("source catalog" in p["recommendation_basis"] for p in recommended))


class OrchestrationRegressions(unittest.TestCase):
    def test_malformed_tool_name_and_function_do_not_crash(self):
        model = ScriptedModel({"tool_calls": [{"function": None}, {"function": {"name": [], "arguments": {}}}]},
                              {"content": "Invented answer"})
        agent = Agent(DATA, model)
        self.assertIn("couldn't verify", agent.reply("Find a product"))
        self.assertTrue(all("error" in t["result"] for t in agent.last_trace))

    def test_malformed_model_message(self):
        agent = Agent(DATA, ScriptedModel({"content": {"unexpected": "object"}}))
        self.assertIn("invalid response", agent.reply("Hi"))

    def test_failed_lookup_does_not_license_final_claim(self):
        agent = Agent(DATA, ScriptedModel(tool("search_products", query="x", max_price=-1),
                                         {"content": "This costs BRL 10."}))
        self.assertNotIn("BRL 10", agent.reply("Price?"))

    def test_two_sources_both_reach_final_answer(self):
        model = ScriptedModel(tool("search_products", query="Takamine GD20"),
                              tool("search_policies", query="PIX payment discount"),
                              {"content": "PIX has a 5% discount on nonpromotional list prices."})
        agent = Agent(DATA, model)
        answer = agent.reply("How much is the Takamine GD20 and what is the PIX policy?")
        self.assertIn("2199.00", answer)
        self.assertIn("PIX has a 5%", answer)
        self.assertIn("Policy evidence", answer)
        self.assertEqual({t["tool"] for t in agent.last_trace}, {"search_products", "search_policies"})

    def test_recommendation_tool_uses_agent_context(self):
        model = ScriptedModel(tool("search_products", category_id=5, max_price=1000),
                              {"content": "Here are options"}, tool("recommend_products"),
                              {"content": "Recommendation"})
        agent = Agent(DATA, model)
        agent.reply("Acoustic guitars up to 1000?")
        answer = agent.reply("Which of those is suitable for beginners?")
        self.assertIn("Why it fits", answer)
        agent.reset()
        self.assertEqual(agent.history, [])
        self.assertEqual(agent.last_trace, [])
        self.assertEqual(agent.catalog_candidates, [])

    def test_return_policy_retrieved_and_passed_to_model(self):
        model = ScriptedModel(tool("search_policies", query="online return refund personalized"),
                              {"content": "The store pays return freight; refund uses the original payment method within 10 business days. Human review is required for a customized instrument."})
        agent = Agent(DATA, model)
        answer = agent.reply("Online purchase received five days ago: can I return it?")
        self.assertIn("10 business days", answer)
        evidence = json.loads(model.requests[1][-1]["content"])
        self.assertTrue(any(p["page"] == 4 and "reembolso" in p["text"].lower() for p in evidence["passages"]))

    def test_out_of_scope_uses_no_private_data_tool(self):
        model = ScriptedModel(tool("search_policies", query="store scope instruments accessories"),
                              {"content": "We sell musical instruments, not graphics cards. I cannot provide weather forecasts."})
        agent = Agent(DATA, model)
        self.assertIn("not graphics cards", agent.reply("Do you sell graphics cards?"))
        self.assertTrue(all(t["tool"] == "search_policies" for t in agent.last_trace))

    def test_order_rendering_and_missing_fields(self):
        model = ScriptedModel(tool("order_status", order_id=8), {"content": "Fake tracking number"})
        agent = Agent(DATA, model, authenticated_customer_id=2)
        answer = agent.reply("Status of order 8?")
        self.assertIn("BRJL5544332BR", answer)
        self.assertNotIn("Fake", answer)
        model2 = ScriptedModel(tool("order_status", order_id=9), {"content": "Delivery tomorrow"})
        answer2 = Agent(DATA, model2, authenticated_customer_id=6).reply("Status of order 9?")
        self.assertNotIn("tomorrow", answer2)
        self.assertNotIn("Recorded tracking", answer2)

    def test_invalid_input_clears_old_trace(self):
        agent = Agent(DATA, ScriptedModel())
        agent.last_trace = [{"tool": "old"}]
        agent.reply("")
        self.assertEqual(agent.last_trace, [])


class ProviderTests(unittest.TestCase):
    def test_transport_error_timeout_and_invalid_json(self):
        for exc in [URLError("offline"), TimeoutError(), ValueError("bad JSON")]:
            with patch("emporio.model.urllib.request.urlopen", side_effect=exc):
                with self.assertRaises(ModelError):
                    Ollama().chat([], [])

    def test_http_model_not_found(self):
        exc = HTTPError("http://localhost:11434/api/chat", 404, "missing", {}, None)
        with patch("emporio.model.urllib.request.urlopen", side_effect=exc):
            with self.assertRaisesRegex(ModelError, "Model not found"):
                Ollama().chat([], [])

    def test_host_without_scheme_and_payload(self):
        stream = BytesIO(json.dumps({"message": {"role": "assistant", "content": "Hello"}}).encode())
        with patch("emporio.model.urllib.request.urlopen", return_value=stream) as send:
            self.assertEqual(Ollama(base_url="127.0.0.1:11434").chat([], [])["content"], "Hello")
            payload = json.loads(send.call_args.args[0].data)
            self.assertFalse(payload["stream"])
            self.assertEqual(payload["options"]["num_predict"], 1600)


if __name__ == "__main__":
    unittest.main()
