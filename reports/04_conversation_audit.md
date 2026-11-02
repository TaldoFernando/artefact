# Deliverable 4 - Conversation Audit

> Publication correction (2026-11-02): remote `main` is now verified at
> `c078671f3f80fb404a2deebff89a621627e505d2`, including runtime `5dc7d6b`, its
> 55-test suite and five reviewed conversations (20 turns). The tested implementation
> is public. The audit below records an earlier session: its statements about no push,
> pending synchronization and older public revisions describe that historical state,
> not the current remote. Later documentation/PDF corrections are local only.
> See [current publication review](06_publication_review.md) and
> [data provenance](data_provenance.md). The original
> [execution record](final_validation.json) remains byte-for-byte unchanged.

## Historical audit (superseded publication status)

> Historical final-review update (candidate-local date: 2026-11-01): the public repository is https://github.com/TaldoFernando/artefact and its published revision 0421ec4 was anonymously cloned, installed and tested (46 baseline tests passed). The current local final review has 55 passing tests and new full-model validation. New local commits have NOT been pushed. See [final review](05_final_review.md) for current outcomes; earlier counts and runs below are historical evidence.


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
transaction. The repository is public; new local review commits require authorized synchronization before final delivery.

## Current full-version validation

All five examples were rerun on runtime 5dc7d6b in reports/runs/20261102T023230Z.json. The final set has 20 actual turns (including the new recommendation-to-PIX follow-up), all reviewed PASS against source records and the original manual. The older 19-turn mixed-version set above is retained only as development history. See examples/README.md for the current table and limitations.
