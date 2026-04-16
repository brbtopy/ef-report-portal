from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_1 = db.Column(db.String(100), nullable=False)
    dob_1 = db.Column(db.Date, nullable=True)
    ssn_last4_1 = db.Column(db.String(4), nullable=True)
    name_2 = db.Column(db.String(100), nullable=True)
    dob_2 = db.Column(db.Date, nullable=True)
    ssn_last4_2 = db.Column(db.String(4), nullable=True)
    is_married = db.Column(db.Boolean, default=False)
    monthly_salary = db.Column(db.Float, nullable=True)
    monthly_expense_budget = db.Column(db.Float, nullable=True)
    insurance_deductibles = db.Column(db.Float, default=0)
    floor_balance = db.Column(db.Float, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = db.relationship('Account', backref='client', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='client', lazy=True, cascade='all, delete-orphan',
                              order_by='Report.created_at.desc()')

    @property
    def age_1(self):
        if self.dob_1:
            today = date.today()
            return today.year - self.dob_1.year - (
                (today.month, today.day) < (self.dob_1.month, self.dob_1.day)
            )
        return None

    @property
    def age_2(self):
        if self.dob_2:
            today = date.today()
            return today.year - self.dob_2.year - (
                (today.month, today.day) < (self.dob_2.month, self.dob_2.day)
            )
        return None

    @property
    def private_reserve_target(self):
        budget = self.monthly_expense_budget or 0
        deductibles = self.insurance_deductibles or 0
        return (6 * budget) + deductibles

    @property
    def excess_cashflow(self):
        salary = self.monthly_salary or 0
        budget = self.monthly_expense_budget or 0
        return salary - budget

    @property
    def last_report(self):
        if self.reports:
            return self.reports[0]
        return None

    def accounts_by_category(self, category):
        return [a for a in self.accounts if a.category == category]

    def retirement_accounts(self, owner=None):
        accts = self.accounts_by_category('retirement')
        if owner:
            return [a for a in accts if a.owner == owner]
        return accts

    def non_retirement_accounts(self):
        return self.accounts_by_category('non_retirement')

    def trust_accounts(self):
        return self.accounts_by_category('trust')

    def liability_accounts(self):
        return self.accounts_by_category('liability')


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    owner = db.Column(db.String(20), nullable=False, default='client_1')
    category = db.Column(db.String(20), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(100), nullable=True)
    account_number_last4 = db.Column(db.String(4), nullable=True)
    interest_rate = db.Column(db.Float, nullable=True)
    property_address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    balances = db.relationship('ReportBalance', backref='account', lazy=True)

    @property
    def display_name(self):
        name = self.account_type
        if self.account_name:
            name = f"{self.account_name} ({self.account_type})"
        return name


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    quarter = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    report_date = db.Column(db.Date, default=date.today)
    private_reserve_balance = db.Column(db.Float, default=0)
    schwab_balance = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    balances = db.relationship('ReportBalance', backref='report', lazy=True, cascade='all, delete-orphan')

    @property
    def label(self):
        return f"{self.quarter} {self.year}"

    def balance_for_account(self, account_id):
        for b in self.balances:
            if b.account_id == account_id:
                return b
        return None

    def total_retirement(self, client, owner=None):
        total = 0
        for acct in client.retirement_accounts(owner):
            b = self.balance_for_account(acct.id)
            if b:
                total += b.balance or 0
        return total

    def total_non_retirement(self, client):
        total = 0
        for acct in client.non_retirement_accounts():
            b = self.balance_for_account(acct.id)
            if b:
                total += b.balance or 0
        return total

    def total_trust(self, client):
        total = 0
        for acct in client.trust_accounts():
            b = self.balance_for_account(acct.id)
            if b:
                total += b.balance or 0
        return total

    def total_liabilities(self, client):
        total = 0
        for acct in client.liability_accounts():
            b = self.balance_for_account(acct.id)
            if b:
                total += b.balance or 0
        return total

    def grand_total(self, client):
        return (
            self.total_retirement(client, 'client_1')
            + self.total_retirement(client, 'client_2')
            + self.total_non_retirement(client)
            + self.total_trust(client)
        )


class ReportBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    balance = db.Column(db.Float, default=0)
    cash_balance = db.Column(db.Float, nullable=True)
