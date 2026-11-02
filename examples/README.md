# Conversation Validation - Final Review

The final five examples contain **20 actual application turns**, all rerun against
runtime revision `5dc7d6b6bd0ec5bbcc8050038559a24a2a29788b`. Their exact responses, tool
calls and source comparison are recorded in
[the final real-model run](../reports/runs/20261102T023230Z.json). The UTC filename is an
execution timestamp, not an assertion about the candidate's local calendar date.

Prompts are English translations of the requested scenarios. This is local
Ollama/Qwen3 8B inference through the actual Agent implementation, not canned test
answers. Some facts and reviewed policy conditions are intentionally rendered by
Python; the metadata and traces distinguish model selection from application prefetch.
The source review was performed by Codex; candidate endorsement remains pending.

## Final outcomes

| Scenario | Verification | Result | Exact transcript |
|---|---|---|---|
| Products and follow-ups | Acoustic category, budget, stock, prior-candidate recommendations, PIX follow-up and Takamine mixed-source question | PASS | [Conversation 1](01_product_search.md) |
| Store and payment | Address, Saturday hours, four payment forms, installment uncertainty and nonstacking PIX | PASS | [Conversation 2](02_store_information.md) |
| Order privacy | Unauthenticated denial, owned order 8, historical tracking/estimate, missing and foreign orders denied | PASS at trusted identity seam | [Conversation 3](03_order_tracking.md) |
| Return rules | Five days vs seven calendar days; condition, freight/refund, customization review and no processing claim | PASS | [Conversation 4](04_return_policy.md) |
| Scope and recovery | No graphics cards or invented forecast/customer disclosure; recovery to real guitars with honest suitability limitation | PASS with clarification | [Conversation 5](05_out_of_scope.md) |

The PIX follow-up retains the three recommended models and exact prices without
repeating full specifications. The order fixture is explicitly a trusted application
identity test, not a real login. For electric guitars, source descriptions do not
identify beginner-specific models; the correct response offers the five actual options
and asks for a budget instead of inventing suitability.

## Preserved history

| Earlier run | Observed outcome | What changed |
|---|---|---|
| [First audit round](../reports/runs/20261101T195804Z.json), `2d40ba4` | Scenario 1 PARTIAL; scenarios 2-5 FAIL against all requested criteria | Missing mixed-source PIX evidence, address alias, authenticated order query, return conditions and topic recovery |
| [Second round](../reports/runs/20261101T200602Z.json), `d11fc62` | Scenarios 1-4 PASS; scenario 5 FAIL | Reviewed source-bound policy notes and required evidence corrected policies/orders; an empty recommendation still hid available guitars |
| [Targeted prior rerun](../reports/runs/20261101T201149Z.json), `8ebb7a8` | Scenario 5 PASS | Valid search results preserved when beginner labels are absent |
| [Current full rerun](../reports/runs/20261102T023230Z.json), `5dc7d6b` | All five PASS in 20 turns | Composed catalog/order/policy sections, preserved specific products alongside recommendations, budget recheck and shorter payment follow-ups |

Failed runs are not erased. Adding review annotations did not alter original messages,
answers or tool traces: the content integrity hash is recorded in `source_review` and
checked by the verification script. The current five files all use the same runtime
source version; no old execution is presented as a new one.

## Reproduce and inspect

Model `qwen3:8b`, digest
`500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`;
Ollama `0.40.13`; Python `3.12.14`; temperature 0; thinking disabled.
Each file identifies runtime commit, source hashes and exact lookup evidence.

With the installed package and running Ollama:

```sh
python scripts/evaluate.py
```

A fresh run overwrites examples with new, unreviewed output. To restore the reviewed
final examples without calling the model:

```sh
python scripts/evaluate.py --render-run reports/runs/20261102T023230Z.json
python scripts/verify_run.py reports/runs/20261102T023230Z.json
```

The verification command passed: source-commit hashes, 22 retrieved product records,
one owned-order record and 20 turns checked against fixture customer fields. These
checks establish provenance/record parity, not semantic grading. Policy wording was
also compared with the supplied manual. The offline suite separately passed 55 tests.

## Limitations and delivery status

A PASS is limited to these scenarios, not arbitrary prompts or production. There is no
real login, live ERP/carrier integration, refund action or operational handoff. Broad
scope notes can be repetitive and lexical matching can miss paraphrases. The dataset
was supplied for a fictional music-store challenge; original records are unchanged.
See the [data provenance note](../reports/data_provenance.md) for the candidate's exact
statement and the limits of that evidence.

The [repository is public](https://github.com/TaldoFernando/artefact). Remote `main`
was verified at `c078671`, which contains tested runtime `5dc7d6b`, these five examples
and their original raw run. The 55 offline tests passed again during the publication
check; runtime and data remain unchanged. No new model inference was needed.
Earlier audit statements that these implementation commits awaited publication are
historical. See the [publication review](../reports/06_publication_review.md) for
later documentation/PDF corrections prepared locally; no push, form submission or
email was performed in this correction session.
