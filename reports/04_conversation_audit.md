# Deliverable 4 - Conversation Audit

The five delivery transcripts contain **20 actual turns** on runtime `5dc7d6b`.
The [run record](runs/20261102T023230Z.json) stores exact messages, responses, tool
traces, model metadata, source hashes and review annotations. Codex compared outputs
with the CSVs and policy manual; candidate endorsement is not assumed.

## Scenario results

| Scenario | First audit | After policy/evidence fixes | Current result | Transcript |
|---|---|---|---|---|
| Product restrictions, recommendation and PIX | PARTIAL: PIX evidence missing | PASS | PASS, including recommendation-to-PIX follow-up | [Products](../examples/01_product_search.md) |
| Address, Saturday hours and payments | FAIL: address/PIX omitted | PASS | PASS | [Store information](../examples/02_store_information.md) |
| Order ownership and tracking | FAIL: trusted fixture not queried | PASS | PASS at trusted identity seam | [Orders](../examples/03_order_tracking.md) |
| Online return and customized products | FAIL: exclusions overstated | PASS | PASS; conditions and processing limit retained | [Returns](../examples/04_return_policy.md) |
| Scope, attempted disclosure and recovery | FAIL: incomplete recovery | FAIL: empty recommendation hid guitars | PASS with clarification: show actual options and ask budget | [Scope](../examples/05_out_of_scope.md) |

## Run history

| Raw record | Runtime | Outcome and correction |
|---|---|---|
| [First audit](runs/20261101T195804Z.json) | `2d40ba4` | 19 turns; scenario 1 PARTIAL, scenarios 2-5 FAIL. Missing mixed-source PIX, address alias, trusted order query, return conditions and recovery. |
| [Second audit](runs/20261101T200602Z.json) | `d11fc62` | 19 turns; scenarios 1-4 PASS, scenario 5 FAIL. Source-bound notes and required evidence improved policies/orders; empty recommendations still hid guitars. |
| [Targeted rerun](runs/20261101T201149Z.json) | `8ebb7a8` | Four turns; scenario 5 PASS after preserving search results when beginner labels are absent. |
| [Full rerun](runs/20261102T023230Z.json) | `5dc7d6b` | 20 turns; all five PASS. Composed sources, preserved specific products and budget constraints, and retained recommendations in shorter payment follow-ups. |

The earlier selected set combined runs into 19 turns. The current set uses one runtime
and adds a payment follow-up. Original failures remain in the raw records. Adding
review annotations did not change the recorded messages, responses or traces; their
integrity hashes are checked by `scripts/verify_run.py`.

## Verification boundaries

The verifier checked 22 retrieved product records, one owned-order record and 20 turns
for fixture customer-field disclosure. Policy conditions were compared separately with
the original manual; record parity is not semantic grading.

The order example has unauthenticated and trusted-fixture phases. It tests ownership
filtering, not a real login. Electric-guitar descriptions do not identify beginner
models, so the response offers real options and asks for a budget. The read-only
prototype cannot process returns or execute a handoff. These scenario outcomes do not
establish arbitrary-language coverage, universal injection resistance or actual return
eligibility. Reproduction commands and model settings are in the
[conversation index](../examples/README.md).
