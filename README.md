# Empório da Música - grounded customer support agent

Python prototype for the Artefact AI Engineer technical challenge. Mel helps customers
find instruments and answers store questions using the supplied CSV files and policy PDF.
All authored documentation and evaluation answers are in English; original Portuguese
source data are preserved unchanged.

## Run locally

Requires Python 3.11+, [Ollama](https://docs.ollama.com/quickstart), and a machine capable
of running [Qwen3 8B](https://ollama.com/library/qwen3:8b). The model download is about
5.2 GB; runtime memory depends on context and hardware. No paid API or API key is used.

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
ollama pull qwen3:8b
ollama serve
```

If Ollama already runs in the background, skip `ollama serve`. In another terminal,
activate the same environment and run:

```sh
python -m emporio.cli
# Optional local debugging: show tool calls, sources and retrieved passages.
python -m emporio.cli --trace
```

Type `/reset` to clear memory or `/quit` to exit. Examples:

```text
Which acoustic guitars are available for up to BRL 1,000?
How much is the Takamine GD20?
What is the store address?
I received an online purchase five days ago. Can I return it?
```

The application defaults to `OLLAMA_HOST=http://localhost:11434` and
`OLLAMA_MODEL=qwen3:8b`. Override these environment variables if needed. Use a trusted
local Ollama host: requests contain user messages and retrieved internal policy text.
The CLI intentionally has no customer identity override. A model-not-found response
means the model needs to be pulled; connection errors usually mean Ollama is not running.
Run from the repository root or pass `--data-dir /absolute/path/to/data`.

## Design and tradeoffs

```text
CLI -> Agent (persona + last four complete turns)
         -> local Ollama /api/chat (Qwen3 8B, temperature 0)
         -> bounded tool loop (five rounds, max four calls per round)
             -> search_products: fresh CSV reads + Decimal pricing
             -> search_policies: ranked original PDF pages with page citations
             -> order_status: application identity + ownership check
         -> customer answer
```

**Function calling instead of a framework or unrestricted SQL agent.** Three explicit
read-only Python tools make the trust boundary visible. The model chooses tools; Python
validates arguments, filters rows and computes prices. The model never receives an SQL
execution interface or filesystem tool. The small dataset does not justify a database,
vector service or orchestration framework. See [Ollama's tool-calling protocol](https://docs.ollama.com/capabilities/tool-calling)
and [chat API](https://docs.ollama.com/api/chat).

**Hybrid structured lookup and lexical RAG.** Structured data answer stock, price,
promotion and order questions. Product search matches all normalized name tokens and
supports category, effective price and availability filters. Category IDs are in the tool
description; the model maps natural language to them. Results include truncation metadata
and are limited to ten items. A named unavailable product can be inspected explicitly.
Policy retrieval ranks the eight original PDF pages by normalized term coverage, with
small English-to-Portuguese keyword aliases. It returns the three highest-scoring pages
and page numbers. Full pages preserve nearby caveats and conflicting sections. This is
simple and inspectable, but less robust to paraphrases than multilingual embeddings.

**Local LLM.** Qwen3 8B supports tool calling and Portuguese/English. Local inference
avoids API fees and sending the internal manual to a hosted inference provider. It also
requires a model download and suitable hardware. Temperature zero improves repeatability
but does not guarantee identical or correct answers. The model is configurable; a tag is
not an immutable model version. Record `ollama list` and the Ollama version when evaluating.

**Persona and grounding.** Mel is a welcoming, practical music-store assistant, following
the manual's informal but professional tone. The system prompt requires fresh tool
evidence for factual store answers, cites policy pages, distinguishes snapshots from
live integrations, and redirects out-of-scope requests. Tool results are treated as
untrusted data. These instructions reduce risk; they are not a proof of LLM compliance.

**Memory.** Only the last four complete turns are retained in process. There is no disk
chat log, cross-session memory or analytics. `/reset` and process exit discard history.
This enables follow-up questions while limiting retained conversation data and context.

## Data decisions and ambiguities

- All six original CSVs and the policy PDF are retained under `data/`. The PDF filename
  was normalized to `store_policies.pdf`; its contents are unchanged. The 65 products
  include active, discontinued and coming-soon records. Only active items with positive
  stock appear by default. Historical orders are not evidence of current availability.
- Every product call reopens products and promotions, so file updates are reflected on
  the next call. This is **fresh access to a supplied snapshot**, not a production ERP or
  inventory guarantee. Multiple files are not read as a transactional snapshot.
- Monetary operations use `Decimal` and two-place half-up rounding. A promotion applies
  only if `is_active == 1`; campaign names do not establish current calendar validity.
  There are no promotion dates. If several active rows applied to one product, use the
  highest discount, never stack. That is an explicit prototype assumption.
- PIX gets 5% off list price only when no active promotion applies. A promotional product
  displays list price, discount and final price. `max_price` filters the promotional or
  list price **before** any payment-specific PIX discount.
- Order lookup is denied unless trusted application code supplies an authenticated
  customer ID. A supplied email, order number or claimed customer ID is not authentication.
  The CLI deliberately cannot authenticate; it directs users to an authenticated store
  channel. Unit tests exercise the trusted integration seam, including ownership denial.
  Returned order fields omit customer records, free-text notes and totals.
- Orders have `estimated_delivery`, not actual receipt date or purchase channel. The
  assistant must ask for actual receipt date and channel before discussing an online
  regret-return window; it cannot infer eligibility from the order estimate.
- The manual's payment summary and section 3.1 have different installment minimums.
  Section 5.1 leaves exactly BRL 500 undefined. Section 1.2 and section 7 list different
  WhatsApp numbers, and the email spelling also varies. These need human confirmation.
- Defect exchanges (section 4.2), warranty (section 8) and return exclusions may overlap.
  The assistant reports the manual as store guidance, avoids deciding legal rights, and
  refers ambiguous cases to the team. It cannot approve, reject or process a refund.
- Opening times are regular Campo Grande times (`America/Campo_Grande`). There is no
  holiday calendar, so the assistant cannot guarantee the store is open on a given date.
- Complaints are not persisted and handoff is advisory: the assistant cannot claim a
  ticket was registered or a person notified. No transaction or write tools exist.

The fixtures were supplied for a fictitious store. Do not substitute real customer data
in a public repository. Customer and order-item CSVs are retained for provenance but are
not sent to the model. Do not enable `--trace` in a public customer-facing deployment.

## Validation

```sh
python -m unittest discover -s tests -v
python scripts/evaluate.py
```

The unit suite covers catalog filters, fresh file reads, active vs inactive promotions,
nonstacking PIX, unavailable instruments, policy retrieval, authentication and ownership,
tool argument rejection, loop bounds, memory bounds and provider failure. Scripted model
fixtures test orchestration, **not the real model's reasoning**. `scripts/evaluate.py`
requires a running Ollama and writes actual transcripts to `examples/`. Review the
transcripts manually against source data; tool use alone does not establish answer quality.

## Limitations and next steps

This is a CLI prototype, not a deployed WhatsApp integration. There is no production
authentication, refund workflow, complaint queue, carrier lookup, inventory reservation,
formal legal review or price guarantee. Lexical retrieval and name-token matching can
miss synonyms. Policy language and factual correctness rely partly on the model; prompt
injection remains possible despite a read-only tool allowlist. Trace output contains
internal policy excerpts. Local files can be malformed or edited outside this app.

With more time: evaluate paraphrases and adversarial prompts on a labeled dataset;
introduce multilingual retrieval only if it improves measured recall; add schema and
referential-integrity validation; pin dependency and model versions; replace CSVs with
transactional read-only APIs; integrate real identity, redacted observability and an
auditable human handoff. Add a web UI only after the core support behavior is evaluated.

## AI-assisted workflow

OpenAI Codex was used to inspect the supplied files, draft the Python implementation,
identify policy ambiguities, write regression tests and prepare English documentation.
The code and tests were generated with AI assistance; source lookups and test runs were
used to check the resulting behavior. Scripted fixtures are explicitly separated from
real-model transcripts. The candidate must review the code, run it locally and be able to
explain its assumptions and limitations. No claim is made that the work was unaided.

## Submission

The attached brief asks for a public GitHub repository with genuine incremental commits
and 3-5 example conversations. The recruiting email additionally asks for an English PDF
uploaded to its Google Form. Preserve the repository after the submission timestamp;
do not rewrite the history or alter it after delivery. Follow the recruiting email's
submission instructions and include the repository URL in the final PDF.
