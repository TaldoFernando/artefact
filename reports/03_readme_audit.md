# Deliverable 3 - README Compliance Audit

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


## Method and result

Read the existing README in full and compared it with the actual Python modules,
packaging, CLI, data, unit suite and real model runs before editing. Preserved correct
information about local inference, Decimal pricing, four-turn memory, snapshot limits,
manual ambiguities and AI assistance. The complete corrected English document is
[`../README.md`](../README.md); no duplicate README copy is maintained here.

**Verdict: compliant for the documented local implementation, with delivery reservations.**
A public URL and baseline clone are verified; final local updates await push authorization, and Windows/Linux execution remain unverified. The actual
conversation outcomes, including failures before corrections, are separately documented.

## Requirement-by-requirement table

| Requirement | Status | Evidence / revision |
|---|---|---|
| Identification, objective and Artefact context | Met | Title and introduction identify the fictitious store and technical challenge |
| Entire README in English | Met | English authored prose; Portuguese proper names/source identifiers preserved |
| `Architecture` section | Met | Actual six-tool loop, prefetch, error handling, final rendering and Mermaid diagram |
| LLM interpretation and tool selection | Met | Native Ollama tool calls; explicit application-required evidence described separately |
| Structured data and PDF retrieval | Met | Fresh CSV reads, Decimal, lexical pages and hash-bound reviewed English notes |
| Final answer composition | Met | Numerical/order facts rendered from records; known policy notes rendered with source citations; unknown policy prose generated |
| `Tech Stack` section | Met | Python, standard library, pypdf, Ollama, unittest, Windows tzdata, optional ReportLab |
| `Getting Started` section | Met locally | Editable install, venv, data validation and CLI commands executed in a new environment |
| Public clone command | PASS | Real URL is present; anonymous clone of public revision 0421ec4 was installed and its 46 baseline tests passed |
| macOS/Linux and Windows instructions | Partial across platforms | macOS paths/behavior verified; PowerShell explicitly documented as untested |
| Environment configuration | Met | Safe `.env.example`; process-environment behavior and shell loading explained |
| Automatic `.env` loading not falsely claimed | Met | README explicitly states Python does not auto-load it; shell example checked |
| Data availability/setup | Met | Bundled six CSVs and policy PDF; no unimplemented import/migration step |
| `Model Configuration` section | Met | Ollama host/tag, no key, resource cost, model limits, timeout and failure behavior |
| Model choice and alternatives | Met | Candidate's actual Ollama choice recorded; only implemented protocol documented |
| `Technical Decisions` section | Met | Framework avoidance, hybrid approach, local model tradeoff, retrieval scale, deterministic facts, prompts, memory and data preparation |
| `Features` section | Met | Describes actual tools; CLI login and transaction limitations are explicit |
| `Usage Examples` section | Met | Real start command, labeled shortened excerpt and relative links to full exact transcripts |
| Relative links | Verified locally | Targets checked after report/example generation; external official references checked separately |
| `Testing` section | Met | Offline vs real-model tests separated; actual count 46; no invented coverage |
| Integration dependencies | Met | Running Ollama and pulled model required; provenance recorded in JSON |
| `Known Limitations` section | Met | Snapshot, no production auth/transactions, retrieval/model limits, policy conflicts, no platform/public-clone overclaim |
| `Future Improvements` section | Met | Prioritized evaluation, real identity, handoff, source APIs, context control and channels |
| `AI-Assisted Development` section | Met | Codex activities, observed errors, executed verification, explicit candidate choice and pending candidate endorsement |
| No invented candidate development history | Met | Only local Ollama choice is attributed to candidate; other design choices attributed to Codex assistance |
| Original-data use and unused fields | Met | All tables described; customer PII is validation-only and not exposed to the model |
| Scope and privacy limits | Met | No customer-list tool, no identity established by chat claims, trace warnings |
| Source ambiguities and assumptions | Met | Promotions, PIX, contacts, installments, exact BRL 500 boundary, returns and estimated dates |
| Submission requirements | Partial at project level | Public URL/clone verified; final local synchronization and candidate delivery remain pending |

## Technical inconsistencies corrected

1. The baseline README's three-tool description no longer matched the added tools. It
   now lists all six implemented interfaces and explains the separation of LLM tool
   selection from application prefetch.
2. The baseline described catalog rendering as an alternative to useful recommendations
   and deferred mixed questions. The current implementation supports source-based
   recommendations and preserves a separate policy explanation; the README matches it.
3. Source policy generation was described as entirely model-driven. It now documents
   reviewed English notes tied to the exact PDF hash, cited sections and disable-on-change
   behavior, with lexical/generated fallback for unrecognized topics.
4. New-environment installation, table validation and malformed-response tests were
   missing from the documented verification. Executed commands and current boundaries
   replace assumptions. `pyproject.toml` is the dependency source; an unnecessary duplicate
   `requirements.txt` was not introduced.
5. Missing `.env.example` is now supplied. Configuration instructions do not falsely
   imply a dotenv loader. Host defaults and a host without scheme are supported.
6. Previous examples were incomplete and lacked the requested QA structure. README links
   now point to exactly five full scenarios and their validation index.
7. The prior 21-test count is obsolete; the corrected suite has 46 executed tests. Scripted
   answers are not described as real model reasoning, and no coverage percentage is claimed.
8. AI disclosure now distinguishes the candidate's recorded provider choice from choices
   proposed/implemented by Codex. No human review or unaided authorship is invented.
9. The old 21-test PDF is replaced during final review using the executed validation record.
10. Public clone setup is verified on macOS; Windows/Linux platform execution is explicitly unverified.

## Command verification

Executed in a new Python 3.12.14 venv on macOS:

- `python -m pip install -e .`: succeeded (after approved network retry).
- `python -m pip check`: no broken requirements.
- `python -m unittest discover -s tests -v`: 46 passed.
- `python scripts/validate_data.py`: all six fixture tables passed.
- `emporio --help`: entry point registered and correct options displayed.
- `python -m emporio.cli` with `/reset` and `/quit`: start/reset/exit succeeded.
- Shell loading of `.env.example`: resolved `http://localhost:11434` and `qwen3:8b`.
- `python scripts/evaluate.py`: actual model calls and exact evidence recorded; rerun after
  correcting semantic defects. See conversation index for reviewed outcomes.
- Local Markdown link check: 20 references checked, none broken. All five transcript
  files contain the nine required sections. The four official Ollama reference URLs
  in the README were opened successfully.

Not executed: Windows/Linux platform execution, Windows PowerShell,
a different model tag, production authentication, a refund or external handoff. These
are not claimed as working features.

## Deliverable

The full, corrected [`README.md`](../README.md) is the deliverable. It preserves the
working project's simple architecture and documents actual behavior, supported by
source checks and executed tests. Candidate review, authorized synchronization and final
submission are still required for the complete recruitment delivery.
