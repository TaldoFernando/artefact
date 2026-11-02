"""Build the submission overview from the final, executed validation record."""
import argparse
import json
import hashlib
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle, Spacer

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / 'output/pdf/Fernando dAvila Filho - AI Engineer - Full-Stack Generative AI Applications.pdf'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--validation', type=Path, default=ROOT / 'reports/final_validation.json')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    record = json.loads(args.validation.read_text())
    tests = record['offline_tests']
    if tests['failed'] or tests['passed'] != tests['total']:
        raise SystemExit('The validation record does not establish a passing offline suite.')
    run = json.loads((ROOT / record['llm_evaluation']['run_file']).read_text())
    if run['metadata']['base_commit'] != record['runtime_commit']:
        raise SystemExit('Runtime and evaluation provenance differ; refresh validation first.')
    for file, expected in run['metadata']['code_sha256'].items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Runtime changed after evaluation: {file}. Revalidate before building.')
    repo = record['repository']['url']
    if repo != 'https://github.com/TaldoFernando/artefact':
        raise SystemExit('Unexpected repository URL; review the validation record.')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleCustom', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=colors.HexColor('#103B43'), spaceAfter=16))
    styles.add(ParagraphStyle(name='SectionCustom', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=colors.HexColor('#103B43'), spaceBefore=13, spaceAfter=7))
    styles.add(ParagraphStyle(name='BodyCustom', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=8))
    styles.add(ParagraphStyle(name='CodeCustom', fontName='Courier', fontSize=8.8, leading=12, spaceAfter=4))
    story = []
    def p(text, style='BodyCustom'):
        story.append(Paragraph(text, styles[style]))
    def heading(text):
        p(text, 'SectionCustom')
    def table(rows, widths):
        cells = [[Paragraph(escape(str(c)), styles['BodyCustom']) for c in row] for row in rows]
        result = Table(cells, colWidths=widths, repeatRows=1)
        result.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E7F1F2')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), .4, colors.HexColor('#D6E0E2')), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
        story.append(result)
        story.append(Spacer(1, 8))
    p('ARTEFACT / AI ENGINEER TECHNICAL CASE', 'SectionCustom')
    p('Empório da Música<br/>AI Customer Support Agent', 'TitleCustom')
    p("<b>Fernando d'Ávila Filho</b><br/>AI Engineer - Full-Stack Generative AI Applications")
    p(f'<b>Public repository:</b> <link href="{repo}" color="#087D8A">{repo}</link>')
    p('Prepared for candidate review. The repository is public; the final local review commits require explicit push authorization before recruitment submission.')
    heading('Problem and solution')
    p('Mel helps the fictitious Campo Grande music store answer recurring questions about instruments, prices, availability, order status and store rules. The prototype is a Python command-line conversation using local Ollama/Qwen3 8B, six read-only tools and evidence from supplied CSVs and the original policy PDF.')
    heading('Architecture and implemented capabilities')
    table([
        ['Component', 'Role'],
        ['CLI and context', 'One local session; four complete turns; reset clears history and recommendation context.'],
        ['Ollama / Qwen3 8B', 'Interprets messages and calls allowlisted tools; no paid inference API or API key.'],
        ['Structured tools', 'Product search/details, active offers, source-based beginner recommendations and authorized order/item lookup.'],
        ['Policy retrieval', 'Lexical PDF pages plus reviewed English notes enabled only for the exact source PDF hash.'],
        ['Answer composition', 'Exact prices, stock and order facts; separate policy guidance; mixed questions preserve all verified components.'],
        ['Controls', 'Validated arguments, ownership checks, provider-error handling and bounded tool rounds.'],
    ], [118, 380])
    heading('Why this design')
    p('The eight-page manual and 65-product catalog do not require a vector database or orchestration framework. Python handles Decimal pricing, active-promotion flags, nonstacking PIX discounts and record ownership. The LLM handles interpretation; retrieved facts and reviewed policy conditions remain explicit and inspectable.')
    story.append(PageBreak())
    heading('Technology and execution')
    p('Python 3.11+, standard-library HTTP/CSV/JSON/Decimal tools, pypdf, Ollama and Qwen3 8B. Tests use unittest and unittest.mock. ReportLab builds this document. The model download is about 5.2 GB; runtime memory depends on hardware and context. Evaluation used a macOS host with 24 GiB RAM; no universal minimum is claimed.')
    p('From the repository root, with Python 3.11+ and Ollama installed:')
    for command in ['python3 -m venv .venv', 'source .venv/bin/activate', 'python -m pip install -e .', 'ollama serve  # separate terminal, if not already running', 'ollama pull qwen3:8b', 'python scripts/validate_data.py', 'python -m emporio.cli']:
        p(escape(command), 'CodeCustom')
    p('Configuration: OLLAMA_HOST=http://localhost:11434 and OLLAMA_MODEL=qwen3:8b. The app reads process environment and does not automatically load .env. Chat requires a running Ollama; /reset and /quit are CLI commands. Full setup and troubleshooting are in the README.')
    heading('Evidence, business rules and privacy')
    p('All six original CSVs and the policy PDF are preserved byte-for-byte. The candidate confirmed the operational records are fictional and do not represent real people. Customer names, emails and phones are not exposed by tools. No credentials were found by the documented repository/history scan.')
    p('Only active, stocked instruments are presented as available. Promotional prices use explicit active flags; a PIX discount never stacks with an active campaign. Follow-up recommendations remain within the original budget when source prices change. The source files are historical snapshots, not live inventory or carrier data.')
    p('Order details require identity supplied by trusted application code and an ownership check. The CLI has no login. The order example explicitly uses a test identity fixture, not real authentication. Estimated delivery is never treated as actual receipt.')
    p('The manual conflicts on contacts, installment minimums and exchange/warranty handling, and leaves local freight at exactly BRL 500 undefined. The assistant preserves uncertainty and requests team confirmation. Customized online returns require review; the prototype cannot approve, process or register a return.')
    heading('AI assistance')
    p('OpenAI Codex assisted with source inspection, implementation, regression tests, actual model evaluation and English documentation. The candidate chose local Ollama and confirmed fictitious data. Other choices were implemented with Codex assistance; no unaided authorship or unperformed human validation is claimed. Candidate review remains essential.')
    story.append(PageBreak())
    heading('Executed validation')
    p(f"<b>Offline suite: {tests['total']} executed, {tests['passed']} passed, {tests['failed']} failed.</b> Installation, dependency consistency, source validation and CLI smoke checks were executed on macOS. An anonymous clone of the published baseline passed its 46 tests; this local review has the updated suite.")
    p('Unit tests include unavailable products, active/inactive offers, PIX, budgets, owned/missing/foreign orders, mixed sources, follow-ups, malformed model output, connectivity failures, empty evidence and changed-PDF handling. Scripted model fixtures test the protocol; real model conversations are evaluated separately.')
    outcomes = record['llm_evaluation']['scenarios']
    table([['Actual local-model scenario', 'Reviewed result']] + [[s['title'], s['result']] for s in outcomes], [365, 133])
    p(f"The five examples contain {record['llm_evaluation']['turns']} exact application turns, with model digest, runtime commit, tool traces, source comparison and limitations. Failed earlier runs remain in the repository. Runtime revision: <b>{escape(record['runtime_commit'][:12])}</b>.")
    for command in ['python -m unittest discover -s tests -v', 'python scripts/evaluate.py', 'python scripts/verify_run.py PATH_TO_RUN_JSON']:
        p(escape(command), 'CodeCustom')
    heading('Relevant limitations')
    p('There is no production authentication, WhatsApp integration, live ERP/carrier connection, refund processor or operational handoff. Lexical topic matching may miss paraphrases; unknown policy prose can be imprecise. Reviewed notes are disabled when the PDF changes and must then be re-reviewed. Four turns do not guarantee token-budget fit. Dependency ranges and model tags are not a full reproducibility lock.')
    p('Beginner recommendations use explicit source descriptions. If no electric-guitar description establishes beginner suitability, Mel shows the real options and asks for a budget instead of inventing advice. Read-only tools and prompts reduce risk but do not prove universal prompt-injection resistance.')
    heading('Before submission')
    p('Review the local changes, authorize their push, confirm the public repository contains the reviewed revision, then upload this PDF and the repository link using the recruiting instructions. This review did not push, submit a form or send email. Freeze the repository after delivery.')
    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor('#D6E0E2'))
        canvas.line(48, 42, A4[0] - 48, 42)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#56686D'))
        canvas.drawString(48, 28, "Fernando d'Avila Filho | Artefact AI Engineer")
        canvas.drawRightString(A4[0] - 48, 28, str(doc.page))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(args.output), pagesize=A4, leftMargin=48, rightMargin=48, topMargin=35,
                      bottomMargin=56, title='Empório da Música - Artefact AI Engineer',
                      author="Fernando d'Ávila Filho").build(story, onFirstPage=footer, onLaterPages=footer)
    print(args.output)


if __name__ == '__main__':
    main()
