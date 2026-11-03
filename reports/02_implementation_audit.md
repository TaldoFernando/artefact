# Deliverable 2 - Implementation and Validation Audit

This report records the earlier technical audit. Test counts and publication
observations below refer to that session; later checks are in the
[publication review](06_publication_review.md). Raw runs and execution records are unchanged.

## Scope and evidence

Audited the official Artefact brief from the supplied ZIP, all six CSV files, the
original policy PDF, all application modules, packaging, CLI, evaluation/PDF scripts,
offline tests, README and previous conversation examples. The baseline was commit
`dab31c0`. Code corrections are recorded incrementally in `2d40ba4` and `d11fc62`.
The targeted catalog-recovery correction is recorded in `8ebb7a8`.
The repository is now verified public; this review does not push updates or perform final submission.

All seven files under `data/` matched an original ZIP entry byte-for-byte by SHA-256.
Only the PDF filename was normalized. Source counts: 65 products, 9 categories,
50 customers, 20 orders, 22 order items and 25 promotions; the manual has eight pages.
No original operational record was changed to make a test pass.

## Architecture found and retained

The baseline CLI used local Ollama/Qwen3 8B, four-turn memory, read-only CSV tools,
Decimal prices and lexical PDF retrieval. Its 21-test suite passed, but real-model
runs exposed missing recommendations and policy conditions in combined answers.

The corrections retained this design. The [README](../README.md#architecture) describes
the current loop and module boundaries. Reviewed English notes are enabled only for
policy PDF SHA-256
`b7527f96896929f4ba929de117651c6717e25b7a3b92b34bc54d5ba32f6156f7`.
They return original source pages; a changed PDF disables the notes.

## Initial findings by severity

| Severity | Baseline problem | Disposition |
|---|---|---|
| High | Malformed tool names/functions could raise unhandled exceptions | Type/schema checks and malformed-payload regressions |
| High | Failed or empty lookups could still be followed by an unsupported final claim | Fail-closed finalization when only failed/empty evidence exists |
| High | Catalog rendering discarded policy text and beginner recommendations | Preserve both sources; source-filtered recommendation tool |
| High | Real model omitted PIX conditions, overstated customized-return exclusions and confused authentication | Source-bound policy notes, trusted-identity context and order prefetch |
| Medium | No dedicated details/active-promotion tools; specifications not parsed | Both tools implemented with parsed JSON and Decimal calculations |
| Medium | Six-table dates/keys/relationships were not validated | Startup validator and standalone validation command |
| Medium | English generic category words could hide Portuguese-named products | Normalize generic descriptors for explicitly selected guitar categories |
| Medium | Previous conversations lacked requested scenarios, source comparison and outcomes | Five exact real-run examples with review sections and raw records |
| Medium | README sections and environment example missing | English README restructured; safe `.env.example` added |
| Low | Last trace survived invalid input/reset | All session state cleared correctly |

## Corrections and files

- `emporio/model.py`: isolated Ollama adapter, host validation, useful HTTP/model errors,
  timeout handling, malformed-response checks and output token limit.
- `emporio/prompts.py`: preserved persona; clarified source use, no duplicate identity
  verification, conditions/exclusions, combined questions and no transaction claims.
- `emporio/store.py`: all-six-table validation, price range, details/specifications,
  active promotions, prior-candidate recommendations, authorized order-item joins,
  category descriptor normalization and reviewed-note/source-page retrieval.
- `emporio/policy_notes.py`: reviewed English rules tied to exact PDF hash, including
  nonstacking PIX, contact/installment conflicts, online returns and customization review.
- `emporio/agent.py`: malformed-call handling, trusted order prefetch, required-policy
  lookup, evidence checks, deterministic facts, combined answers and complete reset.
- `emporio/cli.py`: reset integration and clearer initialization failures.
- `tests/test_agent.py`, `tests/test_audit.py`: 46 executed offline regressions.
- `.env.example`, `pyproject.toml`, `.gitignore`: safe configuration, Windows time-zone
  dependency marker, optional PDF dependency, generated-file exclusions.
- `scripts/evaluate.py`, `scripts/validate_data.py`: real-run provenance and data checks.
- `README.md`, `examples/`, `reports/`: audited documentation and exact QA evidence.

## Commands and observed outcomes

Commands below assume an activated environment and the repository root. The audit
used a new temporary venv created with the bundled Python 3.12.14 executable.

| Command | Observed result |
|---|---|
| `python -m venv <new-venv>` | Created a new environment |
| `python -m pip install -e .` | Successful; installed package and pypdf 6.21.4; first sandboxed attempt was network-blocked and approved network retry succeeded |
| `python -m pip check` | No broken requirements found |
| `python -m unittest discover -s tests -v` | 46 tests passed |
| `python scripts/validate_data.py` | All six tables passed; original counts reported without customer records |
| `emporio --help` | Registered entry point and expected options |
| `python -m emporio.cli` with `/reset`, `/quit` | Started, reset and exited correctly |
| `python scripts/evaluate.py` | Five scenarios, 19 actual turns; first round exposed semantic defects, retained in raw record |
| Repeated `python scripts/evaluate.py` after fixes | Final reviewed outcomes in QA index and run record |
| Credential-pattern scan of code/docs/tests/examples | No OpenAI-style key, AWS access key or private-key header matched |
| `git diff --check` | No whitespace errors at verification |
| `python scripts/verify_run.py reports/runs/20261101T200602Z.json` | Source provenance, 19 product records, one owned-order record and 19 turns checked for fixture customer-field disclosure |
| `python scripts/verify_run.py reports/runs/20261101T201149Z.json` | Targeted rerun provenance, five product records and four turns checked; review integrity hash verified |

No external credentials are needed: Ollama serves the already-downloaded local model.
The loopback HTTP port and package downloads required sandbox escalation; neither an
API key nor a paid inference service was introduced.

## Remaining issues by severity

- Before production: customer authentication, session isolation, operational handoff
  and transaction processing are absent. The trusted test identity is an integration
  seam; the CLI cannot authenticate a customer.
- Retrieval: unfamiliar paraphrases still depend on lexical matches/generated prose.
  Malicious retrieved-text coverage is limited to the evaluated cases; an adversarial
  corpus would be needed to investigate novel payloads.
- Source rules: conflicting contacts, installment minimums, exchange/return provisions
  and the exact BRL 500 shipping boundary require staff clarification.
- Scale/reproducibility: recommendations use the returned page, memory is bounded by
  turn count, CSV reads are not transactional, and model/dependency versions are not locked.
- Delivery/platforms: this session did not push or submit. Its public baseline was
  `0421ec4`; later publication is recorded separately. Windows/Linux were not executed.

## Verdict

The 46-test suite passed in this audit. Later work added nine tests and a full-model
rerun, documented in the [final technical review](05_final_review.md).
Per-scenario results and earlier failures are in the [conversation audit](04_conversation_audit.md).
