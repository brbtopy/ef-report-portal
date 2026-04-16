# EF Report Portal — How It All Works

A plain-English guide to the demo data, the two PDF reports, and every calculation the portal performs.

---

## 1. The Demo Accounts — John & Jane Smith

### What is a "Client" in this portal?

A client is a wealthy family that EF (the financial planning firm) advises. The portal stores all their financial information in one place so the team can generate polished quarterly reports in minutes instead of spending a full day pulling data from spreadsheets and bank emails.

### Client Profile (set up once, edited when things change)

These fields are entered **once during onboarding** and only updated when something changes (new job, raise, new account opened, etc.):

| Field | Demo Value | What It Means |
|-------|------------|---------------|
| **Primary Client** | John Smith | The main person in the household |
| **DOB** | June 15, 1975 | Date of birth — age (50) is auto-calculated |
| **SSN (last 4)** | 1234 | For identification on reports — only last 4 digits stored |
| **Married** | Yes | Determines whether the portal shows a second person |
| **Spouse** | Jane Smith | The second person in the household |
| **Spouse DOB** | March 22, 1978 | Age (48) auto-calculated |
| **Spouse SSN (last 4)** | 5678 | For identification on reports |
| **Monthly Salary** | $15,000 | After-tax take-home pay deposited into checking each month |
| **Monthly Expense Budget** | $11,000 | The agreed-upon amount the family spends per month |
| **Insurance Deductibles** | $5,000 | Total of all insurance deductibles (home, auto, health, etc.) |
| **Floor Balance** | $1,000 | Minimum balance kept in each bank account as a buffer |

### Accounts (set up once per account the family has)

Each account the family owns is added to their profile with a **category**, **type**, **owner**, and optional details. Here's what was set up for the Smiths:

#### Retirement Accounts
These are tax-advantaged accounts for retirement savings.

| Account | Owner | Type | Last 4 of Acct # | What It Is |
|---------|-------|------|-------------------|------------|
| Schwab Roth IRA | John (Client 1) | Roth IRA | 9012 | John's Roth IRA at Charles Schwab. Contributions were taxed going in; grows tax-free. |
| Schwab IRA | Jane (Client 2) | IRA | 3456 | Jane's Traditional IRA at Schwab. Contributions were tax-deductible; taxed on withdrawal. |

#### Non-Retirement Accounts
Regular investment/bank accounts — no special tax treatment.

| Account | Owner | Type | Last 4 of Acct # | What It Is |
|---------|-------|------|-------------------|------------|
| Schwab Joint | Joint | Joint Brokerage | 7890 | A joint investment account at Schwab that both John and Jane own together. |

#### Trust
A trust is a legal entity that holds assets (usually the family home).

| Account | Owner | Type | Property Address | What It Is |
|---------|-------|------|------------------|------------|
| Revocable Trust | Joint | Revocable Trust | 123 Peachtree St, Atlanta, GA | The family's primary residence, held in a trust. Value is updated quarterly from Zillow's Zestimate. |

#### Liabilities (Debts)
What the family owes.

| Account | Owner | Type | Interest Rate | What It Is |
|---------|-------|------|---------------|------------|
| Mortgage | Joint | Mortgage | 6.5% | The home loan on their Peachtree St property. |

---

## 2. The Two PDF Reports — What's In Each One

### SACS — Simple Automated Cash Flow System

**Purpose:** Shows how the family's money flows each month — what comes in, what goes out, and what's left over.

Think of it as a monthly money pipeline:

```
PAYCHECK → CHECKING ACCOUNT → EXPENSES → LEFTOVER → SAVINGS
```

#### Page 1: The Cash Flow Diagram

Three bubbles connected by arrows:

| Element | Demo Value | Where It Comes From |
|---------|------------|---------------------|
| **Inflow (green bubble)** | $15,000 | The client's monthly take-home salary. Set during onboarding in the client profile. This is the after-tax paycheck deposited into their primary checking account. |
| **Outflow (red bubble)** | $11,000 | The agreed monthly expense budget. Set during onboarding. This is a rounded-up number (the actual expenses might be ~$10,500, but it's rounded to $11,000 to create a safety buffer). |
| **Arrow between Inflow → Outflow** | "Checking Account" | Money flows from the paycheck into checking, then the expense budget is transferred to a spending account. |
| **Excess (blue arrow label)** | $4,000/mo | **Calculated automatically:** Inflow minus Outflow = $15,000 - $11,000 = $4,000. This is the money left over each month. |
| **Private Reserve (blue bubble)** | $45,000 | The current balance of the family's high-yield savings account. **Entered manually** each quarter (the team checks with Pinnacle Bank via email). |

#### Page 2: Private Reserve & Investment Details

Three cards showing the savings picture:

| Element | Demo Value | Where It Comes From |
|---------|------------|---------------------|
| **Private Reserve Balance** | $45,000 | Current balance of the high-yield savings account. Entered manually each quarter by the team. |
| **Schwab Investment Balance** | $125,000 | Current value of the Schwab investment account. Entered manually (Rebecca logs into Schwab to check). |
| **Monthly Excess** | $4,000 | Calculated: Inflow - Outflow (same as page 1). |
| **Private Reserve Target** | $71,000 | **Calculated automatically:** (6 × monthly expenses) + insurance deductibles = (6 × $11,000) + $5,000 = $66,000 + $5,000 = $71,000. This is how much the family should have saved as an emergency fund. |
| **Progress Bar** | 63% | Calculated: current PR balance / PR target = $45,000 / $71,000 = 63%. Shows how close they are to their savings goal. |

---

### TCC — Total Client Chart

**Purpose:** A snapshot of everything the family owns (and owes) — their total net worth, organized by account type.

#### Client Info Pills (top of page)

| Element | Demo Value | Source |
|---------|------------|--------|
| **Client 1 pill** | John Smith, Age 50, DOB 06/15/1975, SSN ***-**-1234 | From client profile (onboarding) |
| **Client 2 pill** | Jane Smith, Age 48, DOB 03/22/1978, SSN ***-**-5678 | From client profile (onboarding) |

#### Left Column: John's Retirement + Non-Retirement

**John Smith — Retirement:**

| Account | Balance | Source |
|---------|---------|--------|
| Roth IRA (****9012) | $15,000 | Entered manually each quarter (team checks Schwab) |
| **John Retirement Total** | **$15,000** | **Calculated:** sum of all John's retirement account balances |

**Non-Retirement Accounts:**

| Account | Balance | Cash Balance | Source |
|---------|---------|-------------|--------|
| Joint Brokerage (****7890) | $50,000 | $5,000 | Entered manually (Schwab). Cash balance = uninvested cash sitting in the account. |
| **Non-Retirement Total** | **$50,000** | | **Calculated:** sum of non-retirement balances only. **Trust is NOT included here** (per EF's rules). |

#### Center Column: Trust

| Account | Balance | Source |
|---------|---------|--------|
| Revocable Trust (123 Peachtree St, Atlanta, GA) | $450,000 | Entered manually each quarter — team goes to Zillow, types in the address, and uses the Zestimate (estimated home value). |
| **Trust Total** | **$450,000** | **Calculated:** sum of trust account values |

#### Right Column: Jane's Retirement + Liabilities

**Jane Smith — Retirement:**

| Account | Balance | Source |
|---------|---------|--------|
| IRA (****3456) | $11,000 | Entered manually each quarter (team checks Schwab) |
| **Jane Retirement Total** | **$11,000** | **Calculated:** sum of all Jane's retirement account balances |

**Liabilities (Debts):**

| Account | Interest Rate | Balance | Source |
|---------|---------------|---------|--------|
| Mortgage | 6.5% | $200,000 | Entered manually (team checks with Pinnacle Bank) |
| **Liabilities Total** | | **$200,000** | **Calculated:** sum of all liability balances |

> **Important rule:** Liabilities are displayed **separately** — they are **NOT subtracted** from net worth. EF shows clients what they own and what they owe as distinct numbers.

#### Grand Total (bottom bar)

| Element | Value | Calculation |
|---------|-------|-------------|
| **Grand Total Net Worth** | **$526,000** | John Retirement ($15,000) + Jane Retirement ($11,000) + Non-Retirement ($50,000) + Trust ($450,000) = **$526,000** |

> **Note:** The mortgage ($200,000) is NOT subtracted. Grand Total = assets only. Liabilities are shown separately.

---

## 3. Every Calculation the Portal Performs

### What's entered once (onboarding) vs. what's entered each quarter

#### Onboarding (one-time setup)

These are entered when a new client is first added and only changed if their life changes:

| Data Point | Example | When It Changes |
|------------|---------|-----------------|
| Client name(s), DOB, SSN last 4 | John Smith, 06/15/1975, 1234 | Rarely (name change, etc.) |
| Married / spouse info | Yes, Jane Smith | Rarely |
| Monthly salary (after tax) | $15,000 | When they get a raise or change jobs |
| Monthly expense budget | $11,000 | Reviewed annually or when spending habits change |
| Insurance deductibles (total) | $5,000 | When policies renew |
| Floor balance | $1,000 | Essentially never — always $1,000 |
| Account structure | Which accounts they have, types, account numbers | When they open/close accounts |

#### Quarterly (entered before each client meeting)

These change every quarter and are entered manually by the team:

| Data Point | Example | Where the team gets it |
|------------|---------|----------------------|
| Private Reserve balance | $45,000 | Pinnacle Bank (requested via secure email 2 days before the meeting) |
| Schwab investment balance | $125,000 | Rebecca logs into Schwab manually |
| Each account balance | Roth IRA: $15,000, IRA: $11,000, etc. | Schwab for investments, Pinnacle Bank for bank accounts |
| Cash balances (for investment accounts) | Joint Brokerage cash: $5,000 | Schwab (shows how much is uninvested) |
| Trust/home value | $450,000 | Team goes to Zillow.com, types in the address, reads the Zestimate |
| Liability balances | Mortgage: $200,000 | Pinnacle Bank or loan servicer |

### The formulas

Every calculation is **deterministic math** — no AI, no estimation, no rounding tricks. Just addition and subtraction:

```
┌─────────────────────────────────────────────────────────────────┐
│ SACS CALCULATIONS                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Excess = Inflow − Outflow                                       │
│        = $15,000 − $11,000                                      │
│        = $4,000/month                                           │
│                                                                 │
│ Private Reserve Target = (6 × Monthly Expenses) + Deductibles   │
│                        = (6 × $11,000) + $5,000                 │
│                        = $66,000 + $5,000                       │
│                        = $71,000                                │
│                                                                 │
│ PR Progress = PR Balance / PR Target × 100                      │
│             = $45,000 / $71,000 × 100                           │
│             = 63%                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TCC CALCULATIONS                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Client 1 Retirement Total = sum of Client 1's retirement accts  │
│                           = Roth IRA                            │
│                           = $15,000                             │
│                                                                 │
│ Client 2 Retirement Total = sum of Client 2's retirement accts  │
│                           = IRA                                 │
│                           = $11,000                             │
│                                                                 │
│ Non-Retirement Total = sum of non-retirement accounts ONLY      │
│                      = Joint Brokerage                          │
│                      = $50,000                                  │
│                      ⚠ Trust is NOT included here               │
│                                                                 │
│ Trust Total = sum of trust values                               │
│             = Revocable Trust (home)                            │
│             = $450,000                                          │
│                                                                 │
│ Liabilities Total = sum of all debts                            │
│                   = Mortgage                                    │
│                   = $200,000                                    │
│                   ⚠ Shown separately, NOT subtracted            │
│                                                                 │
│ Grand Total Net Worth = C1 Retirement + C2 Retirement           │
│                       + Non-Retirement + Trust                  │
│                       = $15,000 + $11,000 + $50,000 + $450,000  │
│                       = $526,000                                │
│                       ⚠ Liabilities NOT subtracted              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key business rules (from the PRD)

1. **Liabilities are never subtracted from net worth.** They're shown as a separate section so the client sees what they owe, but the Grand Total only counts assets.

2. **Trust is NOT included in the Non-Retirement Total.** Non-retirement total only includes brokerage/bank accounts. Trust (the house) is its own category.

3. **Trust total IS included in the Grand Total.** Even though it's separate from non-retirement, the home value does count toward overall net worth.

4. **Private Reserve Target uses 6 months of expenses**, not income. It's a safety net: if all income stopped, this covers 6 months of living expenses plus every insurance deductible they'd need to pay out-of-pocket.

5. **Floor balance ($1,000)** is a minimum balance kept in each bank account. It never changes. It's stored in the profile but doesn't factor into the SACS or TCC calculations directly.

6. **Outflow is rounded up** from actual spending. If the family actually spends ~$10,500/month, the budget is set at $11,000 to create a buffer. This number is agreed upon during onboarding.

7. **All quarterly data is entered manually.** No bank APIs, no automatic data pulling. The team contacts Pinnacle Bank via email, logs into Schwab manually, and checks Zillow by hand. This is intentional for V1 due to compliance restrictions and data reliability concerns.
