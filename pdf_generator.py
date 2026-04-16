import io
from flask import render_template
from xhtml2pdf import pisa


def _render_pdf(html_string):
    """Convert an HTML string to a PDF using xhtml2pdf, returned as a BytesIO."""
    buf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=buf)
    if pisa_status.err:
        raise RuntimeError(f"PDF generation failed: {pisa_status.err}")
    buf.seek(0)
    return buf


def generate_sacs_pdf(client, report):
    html = render_template(
        'pdf/sacs.html',
        client=client,
        report=report,
    )
    return _render_pdf(html)


def generate_tcc_pdf(client, report):
    retirement_c1 = client.retirement_accounts('client_1')
    retirement_c2 = client.retirement_accounts('client_2')
    non_retirement = client.non_retirement_accounts()
    trust_accounts = client.trust_accounts()
    liabilities = client.liability_accounts()

    html = render_template(
        'pdf/tcc.html',
        client=client,
        report=report,
        retirement_c1=retirement_c1,
        retirement_c2=retirement_c2,
        non_retirement=non_retirement,
        trust_accounts=trust_accounts,
        liabilities=liabilities,
    )
    return _render_pdf(html)
