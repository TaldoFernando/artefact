# Deliverable 3 - README Checks

The README documents installation, architecture, model configuration, technical
decisions, features, examples, testing, limitations and AI assistance. This report
summarizes source checks and preserves the earlier audit results. Later execution
and publication observations are in the [publication review](06_publication_review.md).

## Documentation checks

| Area | Checked against |
|---|---|
| Architecture and diagram | Six allowlisted tools, model selection vs application prefetch, evidence checks and source-based response composition |
| Technology and setup | `pyproject.toml`, Python entry point, venv/editable install, bundled data and optional PDF dependencies |
| Configuration | `.env.example`, process environment, Ollama host/tag defaults, timeout/context/output settings and errors; Python does not auto-load `.env` |
| Technical decisions | Local provider choice, function schemas, CSV/Decimal rules, lexical pages, PDF-hash-bound notes and four-turn context |
| Features and examples | Implemented tools, labeled shortened excerpt and five exact transcripts; CLI login and transaction actions are absent |
| Testing | Offline tests separated from real-model evaluation; original 46-test audit distinguished from the later 55-test suite |
| Source assumptions | Active flags, multiple-promotion selection, nonstacking PIX, historical delivery estimates and manual contradictions |
| Privacy and scope | Customer fields used only for relationship validation; trusted identity cannot be established by chat; trace contents described |
| Limitations and future work | Snapshot data, retrieval/paraphrase limits, first-page recommendations, context size, platform coverage and unimplemented integrations |
| AI assistance | Codex activities and checks disclosed; only the recorded provider choice attributed to the candidate; candidate review not assumed |

## Corrections made during the earlier audit

The old three-tool/21-test description was updated to match the six-tool implementation
and then-current 46 tests. The README now distinguishes deterministic catalog/order
facts, reviewed policy notes and generated fallback prose. It describes mixed responses,
source-based recommendations, note disable-on-PDF-change behavior and application prefetch.

Setup gained `.env.example` and explicit shell loading rather than an implied dotenv
loader. Dependencies remain in `pyproject.toml` rather than a duplicate requirements
file. Incomplete examples were replaced with links to the five recorded scenarios.
The AI disclosure distinguishes assistance from documented candidate decisions.
The PDF was later rebuilt from execution evidence, replacing the old 21-test draft.

## Historical command results

The earlier audit used a new Python 3.12.14 environment on macOS:

| Check | Observed result |
|---|---|
| `python -m pip install -e .` | Succeeded after an approved network retry |
| `python -m pip check` | No broken requirements |
| `python -m unittest discover -s tests -v` | 46 passed at that audit stage |
| `python scripts/validate_data.py` | All six fixture tables passed |
| `emporio --help`; CLI `/reset`, `/quit` | Entry point, options, startup, reset and exit checked |
| Shell loading of `.env.example` | Resolved `http://localhost:11434` and `qwen3:8b` |
| `python scripts/evaluate.py` | Actual calls recorded; semantic defects corrected in later runs |
| Documentation links/sections | 20 local references checked; nine required sections in each transcript; four official Ollama URLs opened |

An anonymous clone at `0421ec4` was subsequently installed and its 46 tests passed.
The later suite has 55 tests; those results are linked from the publication review.
Windows/Linux, PowerShell, other model tags, production authentication, refunds and
external handoff were not executed. The editable [README](../README.md) is the single
setup reference; historical counts above are not claims about its current test count.
