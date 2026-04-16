# EF Report Portal

A client report portal for EF, a financial planning firm serving high-net-worth families. The team enters client financial data into a structured form and generates polished quarterly **SACS** (cashflow) and **TCC** (net worth) PDF reports in minutes instead of a full day.

## What It Does

- **Client profiles**: Store client info once — names, DOB, SSN (last 4), account structures, monthly salary, expense budgets, insurance deductibles
- **Account management**: Track retirement accounts, non-retirement accounts, trusts, and liabilities per client with support for both single and married households
- **Quarterly data entry**: Structured form pre-filled with static data; team enters current balances. All math is automatic and updates in real-time
- **PDF generation**: Produces two report types matching the firm's existing templates:
  - **SACS** (Simple Automated Cash Flow System) — monthly cashflow diagram with Inflow, Outflow, and Private Reserve
  - **TCC** (Total Client Chart) — net worth overview with retirement, non-retirement, trust, and liabilities sections
- **Report history**: Re-download any previous quarterly report

## Key Calculation Rules

| Rule | Formula |
|------|---------|
| Excess to Private Reserve | Inflow − Outflow |
| Private Reserve Target | (6 × monthly expenses) + insurance deductibles |
| Retirement Totals | Summed per spouse separately |
| Non-Retirement Total | Sum of non-retirement accounts only (trust excluded) |
| Grand Total Net Worth | C1 Retirement + C2 Retirement + Non-Retirement + Trust |
| Liabilities | Displayed separately — **not** subtracted from net worth |

## Tech Stack

| Layer | Tool |
|-------|------|
| Frontend | HTML + Tailwind CSS + vanilla JS |
| Backend | Python / Flask |
| Database | SQLite |
| PDF Generation | xhtml2pdf |
| Hosting | Railway |

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Gaps Identified & Decisions Made

- **No sample PDFs were provided** — SACS and TCC layouts were inferred from the PRD descriptions and screenshot references. A slight visual polish was applied per Maryann's comment ("a little polish would be nice").
- **Canva export deferred** — PRD noted ambiguity (Rebecca: "we don't want to do it in either Canva or Word, ideally"). PDF download is the primary output. Canva integration is ready to add if confirmed.
- **Dropbox auto-save and monthly email** — mentioned in transcript but not committed. Flagged as V2 features.
- **xhtml2pdf used instead of WeasyPrint** — WeasyPrint requires system-level GTK libraries. xhtml2pdf is pure Python and deploys cleanly everywhere with zero system dependencies.

## V2 Roadmap

- API integrations: RightCapital, Schwab, Pinnacle Bank, Zillow (auto-pull balances)
- Canva export via API
- Dropbox auto-save to client folders
- Plaid integration for bank account connectivity
- Client-facing monthly expense worksheet
