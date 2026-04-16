import os
os.environ['FLASK_SKIP_DOTENV'] = '1'

from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Client, Account, Report, ReportBalance

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ef-report-portal-dev-key')
db_path = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', app.instance_path)
os.makedirs(db_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', f"sqlite:///{os.path.join(db_path, 'ef_portal.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


ACCOUNT_TYPES = {
    'retirement': ['IRA', 'Roth IRA', '401(k)', '403(b)', 'Pension', 'SEP IRA', 'Simple IRA'],
    'non_retirement': ['Brokerage', 'Joint Brokerage', 'Savings', 'Checking', 'CD', 'Money Market'],
    'trust': ['Revocable Trust', 'Irrevocable Trust', 'Living Trust'],
    'liability': ['Mortgage', 'Auto Loan', 'Student Loan', 'Personal Loan', 'Credit Card', 'HELOC'],
}

QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']


def fmt_currency(value):
    if value is None:
        return "$0"
    return f"${value:,.0f}"


app.jinja_env.filters['currency'] = fmt_currency


# ── Dashboard ──────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    clients = Client.query.order_by(Client.name_1).all()
    return render_template('dashboard.html', clients=clients)


# ── Client CRUD ────────────────────────────────────────────────────────────

@app.route('/clients/new')
def new_client():
    return render_template('client_form.html', client=None, editing=False)


@app.route('/clients', methods=['POST'])
def create_client():
    client = Client(
        name_1=request.form['name_1'],
        dob_1=_parse_date(request.form.get('dob_1')),
        ssn_last4_1=request.form.get('ssn_last4_1', '').strip(),
        is_married=request.form.get('is_married') == 'on',
        name_2=request.form.get('name_2', '').strip() or None,
        dob_2=_parse_date(request.form.get('dob_2')),
        ssn_last4_2=request.form.get('ssn_last4_2', '').strip() or None,
        monthly_salary=_parse_float(request.form.get('monthly_salary')),
        monthly_expense_budget=_parse_float(request.form.get('monthly_expense_budget')),
        insurance_deductibles=_parse_float(request.form.get('insurance_deductibles')),
        floor_balance=_parse_float(request.form.get('floor_balance')) or 1000,
    )
    db.session.add(client)
    db.session.commit()
    flash(f'Client "{client.name_1}" created.', 'success')
    return redirect(url_for('client_detail', client_id=client.id))


@app.route('/clients/<int:client_id>')
def client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template(
        'client_detail.html',
        client=client,
        account_types=ACCOUNT_TYPES,
    )


@app.route('/clients/<int:client_id>/edit')
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_form.html', client=client, editing=True)


@app.route('/clients/<int:client_id>/update', methods=['POST'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    client.name_1 = request.form['name_1']
    client.dob_1 = _parse_date(request.form.get('dob_1'))
    client.ssn_last4_1 = request.form.get('ssn_last4_1', '').strip()
    client.is_married = request.form.get('is_married') == 'on'
    client.name_2 = request.form.get('name_2', '').strip() or None
    client.dob_2 = _parse_date(request.form.get('dob_2'))
    client.ssn_last4_2 = request.form.get('ssn_last4_2', '').strip() or None
    client.monthly_salary = _parse_float(request.form.get('monthly_salary'))
    client.monthly_expense_budget = _parse_float(request.form.get('monthly_expense_budget'))
    client.insurance_deductibles = _parse_float(request.form.get('insurance_deductibles'))
    client.floor_balance = _parse_float(request.form.get('floor_balance')) or 1000
    db.session.commit()
    flash(f'Client "{client.name_1}" updated.', 'success')
    return redirect(url_for('client_detail', client_id=client.id))


@app.route('/clients/<int:client_id>/delete', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    name = client.name_1
    db.session.delete(client)
    db.session.commit()
    flash(f'Client "{name}" deleted.', 'success')
    return redirect(url_for('dashboard'))


# ── Account Management ─────────────────────────────────────────────────────

@app.route('/clients/<int:client_id>/accounts', methods=['POST'])
def add_account(client_id):
    Client.query.get_or_404(client_id)
    account = Account(
        client_id=client_id,
        owner=request.form['owner'],
        category=request.form['category'],
        account_type=request.form['account_type'],
        account_name=request.form.get('account_name', '').strip() or None,
        account_number_last4=request.form.get('account_number_last4', '').strip() or None,
        interest_rate=_parse_float(request.form.get('interest_rate')),
        property_address=request.form.get('property_address', '').strip() or None,
    )
    db.session.add(account)
    db.session.commit()
    flash(f'Account "{account.display_name}" added.', 'success')
    return redirect(url_for('client_detail', client_id=client_id))


@app.route('/accounts/<int:account_id>/delete', methods=['POST'])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    cid = account.client_id
    db.session.delete(account)
    db.session.commit()
    flash('Account removed.', 'success')
    return redirect(url_for('client_detail', client_id=cid))


# ── Report Generation ──────────────────────────────────────────────────────

@app.route('/clients/<int:client_id>/reports/new')
def new_report(client_id):
    client = Client.query.get_or_404(client_id)
    now = date.today()
    current_quarter = f"Q{(now.month - 1) // 3 + 1}"
    current_year = now.year

    last_report = client.last_report
    previous_balances = {}
    if last_report:
        for b in last_report.balances:
            previous_balances[b.account_id] = {
                'balance': b.balance,
                'cash_balance': b.cash_balance,
            }

    return render_template(
        'report_form.html',
        client=client,
        quarters=QUARTERS,
        current_quarter=current_quarter,
        current_year=current_year,
        previous_balances=previous_balances,
        last_report=last_report,
    )


@app.route('/clients/<int:client_id>/reports', methods=['POST'])
def create_report(client_id):
    client = Client.query.get_or_404(client_id)
    report = Report(
        client_id=client_id,
        quarter=request.form['quarter'],
        year=int(request.form['year']),
        report_date=_parse_date(request.form.get('report_date')) or date.today(),
        private_reserve_balance=_parse_float(request.form.get('private_reserve_balance')),
        schwab_balance=_parse_float(request.form.get('schwab_balance')),
        notes=request.form.get('notes', '').strip() or None,
    )
    db.session.add(report)
    db.session.flush()

    for acct in client.accounts:
        bal_key = f"balance_{acct.id}"
        cash_key = f"cash_balance_{acct.id}"
        balance = _parse_float(request.form.get(bal_key))
        cash_balance = _parse_float(request.form.get(cash_key))
        rb = ReportBalance(
            report_id=report.id,
            account_id=acct.id,
            balance=balance or 0,
            cash_balance=cash_balance,
        )
        db.session.add(rb)

    db.session.commit()
    flash(f'Report {report.label} generated.', 'success')
    return redirect(url_for('view_report', report_id=report.id))


@app.route('/reports/<int:report_id>')
def view_report(report_id):
    report = Report.query.get_or_404(report_id)
    client = report.client
    return render_template('report_detail.html', report=report, client=client)


@app.route('/reports/<int:report_id>/sacs-pdf')
def download_sacs(report_id):
    report = Report.query.get_or_404(report_id)
    client = report.client
    from pdf_generator import generate_sacs_pdf
    pdf_bytes = generate_sacs_pdf(client, report)
    filename = f"SACS_{client.name_1.replace(' ', '_')}_{report.label.replace(' ', '_')}.pdf"
    return send_file(
        pdf_bytes,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename,
    )


@app.route('/reports/<int:report_id>/tcc-pdf')
def download_tcc(report_id):
    report = Report.query.get_or_404(report_id)
    client = report.client
    from pdf_generator import generate_tcc_pdf
    pdf_bytes = generate_tcc_pdf(client, report)
    filename = f"TCC_{client.name_1.replace(' ', '_')}_{report.label.replace(' ', '_')}.pdf"
    return send_file(
        pdf_bytes,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename,
    )


@app.route('/reports/<int:report_id>/delete', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    cid = report.client_id
    db.session.delete(report)
    db.session.commit()
    flash('Report deleted.', 'success')
    return redirect(url_for('client_detail', client_id=cid))


# ── Helpers ────────────────────────────────────────────────────────────────

def _parse_date(val):
    if not val:
        return None
    try:
        return date.fromisoformat(val)
    except (ValueError, TypeError):
        return None


def _parse_float(val):
    if not val:
        return None
    try:
        return float(str(val).replace(',', '').replace('$', ''))
    except (ValueError, TypeError):
        return None


if __name__ == '__main__':
    app.run(debug=True, port=5000)
