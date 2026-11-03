# Final Review and Submission Preparation

This report records the earlier technical audit. Test counts and publication
observations below refer to that session; later checks are in the
[publication review](06_publication_review.md). Raw runs and execution records are unchanged.

Candidate-local context date: 2026-11-01. Raw model runs retain their precise UTC
timestamps. Application runtime reviewed: `5dc7d6b6bd0ec5bbcc8050038559a24a2a29788b`.
Public repository: [TaldoFernando/artefact](https://github.com/TaldoFernando/artefact).

## A. Results

The final audit executed **55 offline tests: 55 passed, zero failed**, then reviewed
five real-model scenarios across 20 turns on runtime `5dc7d6b`. All five met their
recorded source/behavior criteria. These are prototype results, not production claims.

At that session, an anonymous clone of `0421ec4` passed its 46-test suite. No push,
form submission or email was performed. Later publication is recorded in report 06.

## B. Changes made

| File | Issue | Fix | Validation |
|---|---|---|---|
| `emporio/agent.py` | Order rendering could hide catalog facts | Compose independent catalog/order/policy sections | New mixed-order/catalog regression passed |
| `emporio/agent.py` | Recommendations could hide a specifically requested product | Preserve separate detail/narrow-search results alongside recommended models | Two regression variants passed |
| `emporio/agent.py` | Payment follow-up could discard useful recommendations | Refresh the prior recommendation context and retain its exact prices/reasons | Mock regression and actual conversation 1 turn 3 passed |
| `emporio/agent.py` | Repeated specifications and closing blocks | Compact repeated product sets; show full specs for details requests | Actual follow-up preserves information with shorter output |
| `emporio/store.py`, `agent.py` | Recommendation price refresh could exceed original budget | Carry and reapply original minimum/maximum price limits | Repriced temporary-copy fixture excluded the now-over-budget model |
| `emporio/store.py` | Zero-percent active campaign could be mistaken for no campaign | Determine activity from explicit flags, separately from percentage | Temporary-copy promotion regression passed |
| `emporio/store.py` | Runtime malformed specification object could reach renderer | Require JSON object before returning details | Runtime malformed-spec regression passed |
| `emporio/model.py` | Host paths, query strings, fragments or invalid ports were ambiguous | Accept only an http(s) origin, no embedded credentials, valid port | URL-boundary regression passed |
| `tests/test_final_review.py` | Missing final composition/security cases | Nine new offline regressions, including injection/identity/code-execution attempts | Final suite 55/55 |
| `scripts/evaluate.py` | Older examples lacked the new payment-follow-up behavior | Added one real follow-up and reran all five scenarios | 20 exact application turns on one runtime commit |
| `scripts/verify_run.py` | Promotion verification coupled activity to nonzero percentage | Independently verify explicit campaign flags | Current run provenance and source parity passed |
| Documentation, examples, PDF builder and Git attributes | Stale counts, mixed example versions, missing durable evidence and possible data/PDF text conversion | Updated artifacts and actual logs; marked PDFs binary and preserved CSV bytes | Five same-runtime examples, three-page PDF inspection, link/hash/attribute checks and `final_validation.json` |

## C. Executed tests and checks

### Offline results

- Total: **55**. Passed: **55**. Failed: **0**.
- The initial independent check first reconfirmed the prior 46-test baseline.
- Nine new regression tests then passed alongside the original suite.
- Final output is saved in [the offline test log](checks/final_offline_tests.txt).
- Scripted model responses are protocol/data tests, not evidence of real LLM reasoning.
- No coverage percentage was measured or claimed.

Executed with the installed Python 3.12.14 environment on macOS:

```sh
python -m pip install -e .
python -m pip install -e '.[pdf]'
python -m pip check
python -m unittest discover -s tests -v
python scripts/validate_data.py
python -m compileall -q emporio scripts tests
emporio --help
python -m emporio.cli
```

CLI start/reset/exit were exercised with `/reset` and `/quit`. Dependency consistency
and compilation succeeded. An actual refused loopback connection was also exercised
without stopping the user's Ollama service; the adapter returned its controlled
ModelError. The Windows/Linux command variants were not platform-tested.

### Actual local LLM evaluation

```sh
python scripts/evaluate.py
python scripts/verify_run.py reports/runs/20261102T023230Z.json
```

| Scenario | Turns | Result | Material verification |
|---|---:|---|---|
| Product restrictions, recommendation, PIX follow-up and mixed sources | 4 | PASS | Category, budget, stock, exact amounts, no stacked discount, retained recommendation reasons |
| Store information and payment | 4 | PASS | PDF address, Saturday hours, payment methods and PIX caveat; installment ambiguity preserved |
| Orders and privacy | 5 | PASS at trusted identity seam | Unauthenticated denial, owned order 8, missing/foreign order denial, exact historical tracking/estimate |
| Return rules and customization | 3 | PASS | Seven-calendar-day rule, all conditions, store-paid return freight, original-payment refund in 10 business days, review/no transaction claims |
| Scope, manipulation and recovery | 4 | PASS with clarification | No invented weather/products/private fields; real guitar options with honest missing beginner labels |

Model: `qwen3:8b`; digest
`500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`;
Ollama `0.40.13`. All five examples use the same runtime hash set. Source verification
checked 22 retrieved product records, one owned-order record and all 20 turns for fixture
customer-field disclosure. Review integrity checks establish that annotations did not
change the actual messages, responses or tool traces. Semantic conditions were compared
with the original manual; a successful HTTP call alone was never classified as PASS.

Earlier failures remain in `reports/runs/` and are summarized in
[the conversation index](../examples/README.md). The final review was performed with
Codex assistance; candidate review/endorsement is still pending.

### Source data, privacy and security

All seven data files matched original ZIP bytes. Customer names, phones and emails
were neither authentication credentials nor tool output. The customer CSV first
appears in `eff9ae8`; no history rewrite was performed. The candidate statement about
fictional data and its limits are documented in [data provenance](data_provenance.md).

A scoped scan inspected 68 historical Git blobs and the current relevant files for
OpenAI-style secret keys, AWS access-key IDs and private-key headers. No match was found;
there is no `.env` file with secrets. These bounded pattern checks are not a proof
against every secret format. Model tools expose no shell, Python execution, arbitrary
SQL or environment reconfiguration capability. Identity is supplied by trusted
application code, never by a model argument or chat claim.

### PDF

The previous three-tool/21-test draft was replaced. The updated English PDF includes
candidate/role, project, six-tool architecture, technologies, actual results, limits,
public URL and concise execution instructions. Three rendered pages were visually
inspected for legibility, clipping, overlap, table spacing and page numbering. The
repository hyperlink was checked in the PDF annotations. The builder reads the final
validation record instead of accepting an unchecked claim that evaluation passed.

## D. Limits and delivery

The documented tests passed for the implemented features. Production authentication,
transactions, WhatsApp, ERP/carrier access, multiuser serving and operational handoff
are not implemented. Lexical matching can miss paraphrases, generated policy prose may
be inaccurate and broad scope notes can repeat. Notes require review when the PDF
changes. Four-turn memory does not bound token size; dependency ranges/model tags
are not locked. Manual contradictions require staff confirmation.

Windows/Linux and universal prompt-injection resistance were not verified. The
[README](../README.md#known-limitations) consolidates the operational limits.
The candidate must review the code, AI disclosure, transcripts and PDF, publish approved
changes, and complete recruitment delivery. Keep the repository unchanged afterward.
