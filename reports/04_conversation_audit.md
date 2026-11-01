# Deliverable 4 - Conversation Audit

The consolidated assessment, per-scenario results, issues, corrections, exact run
records and reproduction commands are in [`../examples/README.md`](../examples/README.md).
The five complete transcripts are linked there and each contains Scenario, Objective,
Execution details, Conversation, Tools used, Ground truth, Validation, Result and
Observations. No full transcript has been replaced with a polished hypothetical answer.

## Evaluation table

| Scenario | First audit round | After source-bound rules/evidence corrections | Final selected result |
|---|---|---|---|
| Product restrictions, recommendation and mixed sources | PARTIAL: PIX policy missing | PASS | PASS |
| Location, Saturday hours and payment | FAIL: missing address and PIX conditions | PASS | PASS |
| Order authorization and tracking | FAIL: trusted fixture order not queried | PASS | PASS at trusted integration seam |
| Online return, customization and inability to process | FAIL: overbroad exclusion/eligibility wording | PASS | PASS |
| Scope, attempted disclosure and recovery | FAIL: scope/recovery incomplete | FAIL: available guitars hidden by empty recommendation | PASS after targeted rerun |

## Evidence and limitations

Nineteen turns appear in the final five files. The complete first and second rounds
also contain 19 turns each; a final targeted four-turn rerun corrected scenario 5.
Original failed runs remain available. Test messages, responses and tool traces were
not edited when adding review annotations; their content hashes are recorded separately.

The order case intentionally contains an unauthenticated phase and a new trusted test
fixture phase. This proves the authorization seam and ownership filtering, not actual
login. The scope recovery correctly asks for a budget when source descriptions do not
support a beginner-specific recommendation. Numerical product/order records were checked
independently against the CSVs; policy conditions were compared with the original manual.
The source review was performed with Codex assistance; candidate endorsement remains pending.

## Verdict

**Approved with reservations for the requested local conversation deliverable.** All
five final scenarios meet their source/behavior criteria. This conclusion does not
establish universal language coverage, production authentication, prompt-injection
immunity or legal eligibility for an actual return. The prototype cannot execute any
transaction. The broader project still requires public publication and final delivery.
