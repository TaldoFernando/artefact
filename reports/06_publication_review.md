# Publication and Artifact Checks

Repository: [TaldoFernando/artefact](https://github.com/TaldoFernando/artefact).
This report separates historical observations from the later editorial review.

## Publication observations

| Check | Observed state |
|---|---|
| Earlier anonymous clone | Revision `0421ec4` installed on macOS; its then-current 46 tests passed |
| Publication correction, 2026-11-02 context | Remote `main` returned `c078671f3f80fb404a2deebff89a621627e505d2`, including with credentials disabled; repository URL returned HTTP 200 |
| Editorial review, 2026-11-02 context | Remote `main` returned `78825552215a3679238def9ad5f251451ccee5d6`, including the publication/provenance corrections |

Both published revisions contain runtime `5dc7d6b6bd0ec5bbcc8050038559a24a2a29788b`,
the 55-test suite and five reviewed conversations (20 turns). Runtime, tests, data
and dependencies are unchanged in this editorial review. The new editorial changes
are local; this review does not push, submit a form or send email.

## Preserved snapshots

[final_validation.json](final_validation.json) is the original execution record.
[publication_sync.json](publication_sync.json) records the later publication check,
source hashes, data integrity, links, bounded credential scan and the PDF then reviewed.
Both JSON files remain unchanged. Their remote references and PDF hashes describe
those observations, not a moving current state. The editorial PDF hash and new checks
are recorded separately in [the editorial log](checks/editorial_validation.txt).

Earlier reports retain their technical outcomes and distinguish historical test counts.
Their previous prose is also available in commit `7882555`; real transcripts, raw runs
and command logs were not edited during the editorial pass.

## Publication-correction checks

These checks ran on Python 3.12.14 / macOS before the editorial review:

| Check | Recorded result | Evidence |
|---|---|---|
| `python -m pip check` | No broken requirements | [Dependency log](checks/sync_dependencies.txt) |
| `python -m unittest discover -s tests -v` | 55 passed, zero failed | [Test log](checks/sync_offline_tests.txt) |
| `python scripts/validate_data.py` | Six tables passed; existing snapshot warnings retained | [Data log](checks/sync_data.txt) |
| `python -m compileall -q emporio scripts tests` | Passed | [Syntax log](checks/sync_syntax.txt) |
| `python scripts/verify_run.py reports/runs/20261102T023230Z.json` | Source/hash parity; 20 turns, 22 product records, one owned order | [Run verification](checks/sync_run_verification.txt) |
| Original data | All seven files matched original ZIP bytes | Publication snapshot |
| Links, credentials and history | README targets/HTTP links checked; no matches for the bounded secret patterns; ancestry retained | Publication snapshot |
| PDF | Three pages opened and visually inspected; candidate, role, six tools, results and repository hyperlink checked | Historical PDF hash in publication snapshot |

Customer data provenance and the limits of the candidate's statement are documented in
[data_provenance.md](data_provenance.md). No original data or history was rewritten.

## Editorial review

The README, reports 02-06, provenance note and conversation index were edited for
clarity. Repeated publication narratives, duplicated feature/checklist tables and
self-approval conclusions were removed. Technical findings, test counts, failure
history, model metadata and AI disclosure remain. The PDF builder and submission PDF
were edited together; all final pages were inspected.

The [editorial log](checks/editorial_validation.txt) records the repeated offline suite,
dependency/data/syntax checks, CLI checks, Markdown links/formatting, commit resolution,
protected-file comparisons and final PDF verification. No new Ollama inference was
needed: runtime, data and recorded conversations are unchanged.

## Remaining actions

The candidate must review and publish the editorial changes, then complete recruitment
delivery. Windows/Linux execution, production authentication, transactions and universal
prompt-injection resistance remain outside the recorded prototype checks. Keep the
repository unchanged after submission.
