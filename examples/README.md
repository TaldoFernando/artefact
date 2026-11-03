# Recorded Conversations

Five scenarios contain **20 actual application turns** on runtime
`5dc7d6b6bd0ec5bbcc8050038559a24a2a29788b`. The
[raw run](../reports/runs/20261102T023230Z.json) contains exact responses, tool calls,
source hashes and review annotations. Prompts translate the requested scenarios into
English. Codex performed source comparison; candidate review is not assumed.

| Scenario | Purpose | Result | Transcript |
|---|---|---|---|
| Products and follow-ups | Budget/stock filtering, source-based recommendations, PIX follow-up and a mixed-source Takamine question | PASS | [Conversation 1](01_product_search.md) |
| Store information | Address, Saturday hours, payment methods, installment uncertainty and nonstacking PIX | PASS | [Conversation 2](02_store_information.md) |
| Orders | Unauthenticated denial, owned order 8, historical tracking/estimate and missing/foreign-order denial | PASS at trusted identity seam | [Conversation 3](03_order_tracking.md) |
| Returns | Online-return conditions, customization review and inability to process a return | PASS | [Conversation 4](04_return_policy.md) |
| Scope and recovery | Reject unrelated requests and disclosure attempts, then show actual guitars and ask for a budget | PASS with clarification | [Conversation 5](05_out_of_scope.md) |

The order fixture tests ownership filtering, not login. Electric-guitar descriptions
lack beginner labels, so the response asks for a budget rather than inventing suitability.
The PIX follow-up retains three recommended models and prices without repeating full
specifications. Earlier failures and corrections are in the
[conversation audit](../reports/04_conversation_audit.md).

## Reproduce and inspect

Recorded environment: `qwen3:8b`, digest
`500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`;
Ollama `0.40.13`; Python `3.12.14`; temperature 0; thinking disabled.
Python renders catalog/order facts and recognized policy notes; traces distinguish
model-selected calls from `application_prefetch`. UTC filenames identify execution times.

With the package installed and Ollama running:

```sh
python scripts/evaluate.py
```

A fresh run overwrites examples with new, unreviewed output. To render the recorded
examples without inference, then verify provenance and record parity:

```sh
python scripts/evaluate.py --render-run reports/runs/20261102T023230Z.json
python scripts/verify_run.py reports/runs/20261102T023230Z.json
```

Verification checked source hashes, review integrity, 22 product records, one owned
order and 20 turns for fixture customer-field disclosure. Policy meaning was reviewed
against the manual separately. The 55-test offline suite is separate from these runs.
Messages, responses, traces and historical failures remain unchanged. Scenario PASS
results do not establish production readiness or correctness for arbitrary prompts;
see the [README limits](../README.md#known-limitations).
