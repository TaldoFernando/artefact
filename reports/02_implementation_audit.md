# Deliverable 2 - Implementation and Validation Audit

> Final-review update (candidate-local date: 2026-11-01): the public repository is https://github.com/TaldoFernando/artefact and its published revision 0421ec4 was anonymously cloned, installed and tested (46 baseline tests passed). The current local final review has 55 passing tests and new full-model validation. New local commits have NOT been pushed. See [final review](05_final_review.md) for current outcomes; earlier counts and runs below are historical evidence.


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

The baseline was already a functional Python CLI using an Ollama/Qwen3 8B function-call
loop, read-only CSV tools and lexical retrieval of PDF pages. It retained four complete
turns in process, calculated prices with Decimal, required application-supplied identity
for orders, and had 21 passing offline tests. However, its final catalog rendering
replaced recommendations and dropped policy explanations in combined questions.

The corrected architecture keeps that design and separates the model adapter
(`emporio/model.py`), persona/prompt (`emporio/prompts.py`), six store tools and policy
retrieval (`emporio/store.py`), reviewed policy summaries (`emporio/policy_notes.py`),
orchestration (`emporio/agent.py`) and CLI (`emporio/cli.py`). This is simpler than
introducing a framework or database for a small fixture set. The LLM chooses tools;
application prefetch also enforces explicit order lookups and missing policy evidence.
Catalog/order facts and source-bound policy notes are rendered deterministically;
other policy questions retain generated prose with retrieved page citations.

Reviewed notes are English summaries of specific original sections, enabled only for
SHA-256 `b7527f96896929f4ba929de117651c6717e25b7a3b92b34bc54d5ba32f6156f7`.
Their cited source pages are returned with the lexical passages. A changed PDF disables
the notes instead of silently reusing stale rules. No claims of independent legal
interpretation or automatic refund approval are made.

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

## Conformity table

Statuses refer to the corrected local prototype, not production readiness.

| Requirement | Status | Evidence | Remaining action |
|---|---|---|---|
| Python as principal language | Met | `emporio/`, `pyproject.toml` | None |
| Store-compatible persona | Met | `emporio/prompts.py`, actual examples | Continue broader evaluation |
| Separation of interface, model, prompt and tools | Met | `cli.py`, `model.py`, `prompts.py`, `agent.py`, `store.py` | No framework required |
| Read all six CSVs and preserve originals | Met | `validate_data`, ZIP SHA-256 comparison | None for supplied fixture |
| Types, dates, blanks, keys and relationships | Met | Validator; range/FK/specification tests | Broaden validation for new source schemas |
| Product name/category/price/availability search | Met | `search_products`; budget/range/unavailable tests | Lexical synonyms remain limited |
| Product details, description and specifications | Met | `get_product_details`; JSON-spec test | Source strings remain in their original language |
| Active promotion lookup and exact arithmetic | Met | `get_active_promotions`; active/inactive and PIX tests | Campaign validity dates absent in source |
| Beginner follow-up grounded in prior results | Met | `recommend_products`; candidate-subset test | Only first returned result page is eligible |
| Authorized order status and items | Met at integration seam | Owned order 8; item join; deterministic rendering | Production login absent |
| Unknown and another customer's order denied | Met | Same `not_found` response; ownership tests | None at this seam |
| CLI customer authentication | Partial | CLI never accepts claimed identity | Add a real authenticated channel before deployment |
| Address, hours and payments from PDF | Met for reviewed topics | Source-bound notes and original cited pages | Confirm conflicting manual details with team |
| Returns, exchanges, exclusions and warranty | Met for reviewed topics | Sections 4/8/10 notes, source page evidence | Ambiguous eligibility requires human review |
| Local/national freight and tracking guidance | Met for reviewed topics | Sections 5.1-5.3 notes | No live quotation or carrier API |
| Multiple-source question | Met | Product facts plus PIX rule; regression test | Broader paraphrase evaluation |
| Scope and malicious-user-message handling | Met for evaluated scenarios | No customer-list tool; scope/privacy notes; recovery example | No universal prompt-injection guarantee |
| Malicious retrieved text | Partial | Prompt treats evidence as data; no arbitrary execution tools | Add an adversarial corpus for novel payloads |
| Environment configuration without embedded secrets | Met | Process environment; `.env.example`; scan | `.env` is not auto-loaded |
| Reproducible package install and CLI | Met locally | New venv, editable install, pip check, CLI smoke test | Public baseline clone verified; Windows/Linux not executed |
| Session continuity and reset | Met | Four-turn memory, candidates, reset test | No multiuser server or context-token budgeting |
| Automated tests actually executed | Met | 46 tests in new environment | No coverage percentage claimed |
| Real integration tests separate from mocks | Met | `scripts/evaluate.py`, exact JSON and Markdown | Semantic outcomes in `examples/README.md` |
| Full English README with AI disclosure | Met locally | README and deliverable 3 audit | Candidate must review/endorse decisions |
| Three to five varied reviewed conversations | See QA report | Five files under `examples/` | Do not equate execution with PASS |
| Public repository and final submission | Partial | Public URL and revision 0421ec4 verified | Final local updates require push authorization; submission pending |

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

1. **High before production:** no real customer authentication, operational handoff,
   transaction processor or production session isolation. The CLI safely denies private
   lookup; trusted test identity is not a login implementation.
2. **Medium:** unknown policy paraphrases still rely on lexical retrieval/generated prose.
   Reviewed topic matching and the exact-PDF guard require maintenance when policies change.
3. **Medium:** source ambiguities (contacts, installment minimums, shipping exactly BRL 500,
   exchanges versus rights) cannot be resolved from the supplied files. Escalate to staff.
4. **Medium:** first-page recommendations, count-based context limits, nontransactional CSV
   reads, mutable model tags and unlocked dependency ranges constrain reproducibility/scale.
5. **Delivery step:** the public repository and baseline clone are verified. Final local commits await explicit push authorization, followed by candidate submission. Windows/Linux remain untested. The current PDF is rebuilt during final review.

## Verdict

**Approved with reservations for the local technical prototype.** Full submission
compliance is still pending authorized synchronization and candidate review. This is not a
production approval. Per-scenario semantic verdicts are in `examples/README.md`.
