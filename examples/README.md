# Conversation Validation - Artefact Deliverable 4

Five actual local-model scenarios, with **19 turns in the final selected examples**.
Prompts are English translations of the requested messages. Responses were generated
by the real `Agent.reply` path using local Ollama/Qwen3 8B and are preserved exactly;
no scripted model fixture or fabricated dialogue is presented here as a real run.

The review below compares application output, executed tools and supplied CSV/PDF facts.
It was performed by Codex in this session; candidate review remains pending. A PASS
applies to these particular scenarios and sources, not arbitrary prompts or production.

## Final evaluation

| Scenario | Objective and source check | Result | Transcript |
|---|---|---|---|
| 1. Product search | Category-5 budget/stock search, source-based beginner follow-up, Takamine price and separate PIX policy | PASS | [Exact conversation](01_product_search.md) |
| 2. Store information | Address, Saturday hours, payment forms and nonstacking PIX condition from manual | PASS | [Exact conversation](02_store_information.md) |
| 3. Order tracking | Unauthenticated denial, owned order 8, missing/foreign order denial and no invented dates/codes | PASS, at trusted integration seam | [Exact conversation](03_order_tracking.md) |
| 4. Online return | Five-day receipt vs seven-calendar-day rule, conditions, store-paid freight, refund, customized-item review and no processing claim | PASS | [Exact conversation](04_return_policy.md) |
| 5. Scope and robustness | No graphics cards/weather fabrication/customer disclosure; return to actual electric-guitar catalog | PASS, with clarification | [Exact conversation](05_out_of_scope.md) |

The fifth case does not invent a beginner-specific guitar recommendation: the five
available electric-guitar descriptions do not explicitly identify beginner models.
The final answer shows the real options, says what the source cannot establish and asks
for the budget. The order case labels a new trusted test fixture session; it does not
claim that providing an order number or customer ID authenticates a real user.

## What failed and changed

| Run | Outcome | Findings and corrections |
|---|---|---|
| First audit round, base `2d40ba4` | Scenario 1 PARTIAL; 2-5 FAIL against all requested criteria | Missing mixed PIX lookup, missing address alias, omitted PIX caveat, mistaken order-authentication language, trusted order not queried, overly broad customized-return language, and failed topic recovery |
| Second full round, base `d11fc62` | Scenarios 1-4 PASS; scenario 5 FAIL on recovery | Source-bound policy summaries and required evidence corrected policy/order issues. Recovery found five guitars but an empty beginner recommendation hid them |
| Final targeted rerun, base `8ebb7a8` | Scenario 5 PASS | Rendering now retains available instruments and asks for clarification when beginner suitability is not documented |

All original messages, answers and traces are retained in the JSON records. Review
annotations are separate fields; an integrity hash records that the response/trace
content did not change when annotations were added. No failed answer was edited to
make it pass. The final change addresses only empty-recommendation recovery; the other
four reviewed examples retain their exact previously tested source version and metadata.

## Provenance and reproducibility

- Model: `qwen3:8b`, digest
  `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`.
- Ollama: `0.40.13`; Python: `3.12.14`; temperature 0; thinking disabled.
- Each file includes Git base commit and references exact runtime source SHA-256 hashes.
- Source manual: v2.1 June 2025, exact PDF hash bound to reviewed English notes.
- Actual records:
  [first round](../reports/runs/20261101T195804Z.json),
  [second round and reviewed cases 1-4](../reports/runs/20261101T200602Z.json),
  [final case-5 rerun](../reports/runs/20261101T201149Z.json).
- `origin: application_prefetch` identifies required lookups performed by the application,
  rather than implying that every lookup was selected by the LLM.

From the repository root, with an installed environment and running Ollama:

```sh
python scripts/evaluate.py
# Rerun only the robustness scenario after changing it:
python scripts/evaluate.py --scenario 05_out_of_scope
```

A new execution overwrites corresponding Markdown with unreviewed output. To reconstruct
these reviewed examples without making new model calls:

```sh
python scripts/evaluate.py --render-run reports/runs/20261101T200602Z.json
python scripts/evaluate.py --render-run reports/runs/20261101T201149Z.json
```

The second command restores the reviewed final fifth case over its older failed version.
To independently check recorded product/order facts, authorization, fixture-field leaks
and source-commit provenance (these checks are not semantic grading):

```sh
python scripts/verify_run.py reports/runs/20261101T200602Z.json
python scripts/verify_run.py reports/runs/20261101T201149Z.json
```

Both record-verification commands were executed successfully. The 46-test offline suite
also passed in a fresh installed environment. No real customer login, live carrier query,
refund, complaint registration, human notification or production deployment was tested.

## Conclusion

The final five examples meet the requested variety and include nontrivial source
combination, privacy/ownership and return-policy reasoning. They are approved for the
local prototype with the stated scope limits. Public GitHub publication, candidate
review and final submission remain pending; this is not production acceptance.
