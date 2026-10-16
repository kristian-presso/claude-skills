---
name: cash-runway
description: Works out how much cash a small UK limited company really has and how long it lasts - cash today, money already owed to HMRC (VAT, Corporation Tax, PAYE and NI set-asides) and other committed outgoings, true free cash, and runway in months. Works from a bank CSV export, from numbers the user types in, or from an accounting tool such as Xero, QuickBooks or FreeAgent if one is connected. Use when someone asks "what's my runway", "how much cash is actually mine", "can we afford this hire", "can we cover payroll", "how much do I need to keep for tax", "cash position" or "burn rate". Reference, not advice. It reads and computes only.
---

# Cash runway

Answers the question a small company owner asks most: how much of the money in the bank is actually mine, and how long does it last?

The headline is always **true free cash**: cash minus what is already owed to HMRC and already committed. Never lead with the raw bank balance. It flatters the position, and VAT collected from customers is the classic way founders spend money that was never theirs.

**Reference, not advice.** This is an estimate built from bank and accounting data. It reads and computes. It never moves money, pays HMRC, declares dividends or files anything. Close every answer with that line, and send decisions with real money at stake (hiring, dividends, a big purchase) to an accountant.

## Inputs, best first

Use the best source available. Say which one you used.

1. **An accounting tool, if connected** (Xero, QuickBooks, FreeAgent or similar). Read bank balances, the VAT liability for the open period, Corporation Tax due or the year-to-date profit, PAYE liabilities and the last 3 months of bank transactions. These are the most reliable set-aside figures. Read only; do not create or change anything.
2. **A bank statement CSV export.** Ask for the last 3 months at least (6 is better) for every business current account. Savings or "tax pot" accounts count as cash too: either include their balance or ask for it.
3. **Numbers the user types in.** Cash today, a typical month's money in and money out, and whatever they know about VAT, Corporation Tax and PAYE owed.

If a figure is missing, ask for it **one question at a time**, starting with the biggest likely set-aside (usually VAT if they are registered). If they do not know it, estimate it using [references/set-asides.md](references/set-asides.md) and label it an estimate. If it cannot be estimated, show it as **unknown, not zero**, and say the free cash figure is overstated by that amount.

## Steps

1. **Cash today.** Sum of all business bank balances on the latest date you have. Note the date.
2. **Monthly burn.** From the last 90 days (default): money out minus money in, scaled to a 30-day month. Leave out transfers between the company's own accounts, loans or capital paid in, and one-off items the user flags, and say what you left out. If money in exceeds money out, free cash is not being drawn down, but check step 5 first: an inflow does not help if true free cash is already negative.
3. **Set-asides.** VAT owed, Corporation Tax (unpaid for past periods plus accrued on this year's profit), PAYE and NI owed. Method and current rates are in [references/set-asides.md](references/set-asides.md). Read it before estimating any of these.
4. **Other committed outgoings.** Declared but unpaid dividends, loan repayments, anything the user names. Separate line.
5. **True free cash** = cash today minus set-asides minus committed outgoings. This is the headline.
6. **Runway** = true free cash divided by monthly net burn. Also show what the raw balance would have suggested, so the user sees the gap. **If true free cash is negative, there is no runway to count: the company already owes more than it holds.** Lead with a clear warning and the amount short, write runway as "already short by £X" (never "not applicable" or "cash-positive", even if more is coming in than going out), and suggest speaking to their accountant and, if a tax bill cannot be paid on time, contacting HMRC before it is due (gov.uk/difficulties-paying-hmrc). If free cash is exactly zero, runway is none.
7. **Next tax hits.** If you know the dates, list the next VAT, Corporation Tax and PAYE payments with amounts, so the user can see when the set-aside money leaves. The `uk-deadlines` skill in this plugin works out the dates.

**If you can run Python**, the bundled script does steps 1, 2, 5 and 6 from a bank CSV and prints the table. It detects common UK bank export layouts (single amount column, or separate paid in and paid out; newest or oldest first; £ signs and commas):

```bash
python3 scripts/cash_runway.py statement.csv --exclude "SAVINGS|TAX POT" \
    --vat-owed 4200 --ct-owed 9100 --paye-owed 1850 --committed 1200
python3 scripts/cash_runway.py --balance 52000 --monthly-in 18000 --monthly-out 23500 --vat-owed 3000
```

If a column is not detected, pass `--date-col`, `--amount-col`, `--in-col`, `--out-col`, `--balance-col` or `--desc-col`. Use `--balance` to add accounts not in the CSV. Without Python, do the same arithmetic by hand and show it.

## Output

```text
Cash position as of 30/09/2026 (source: bank CSV, 3 months)

Cash today                         £35,500
less VAT owed (estimate)            £4,200
less Corporation Tax set-aside      £9,100
less PAYE and NI owed               £1,500
less declared dividend              £3,000
True free cash                     £17,700

Monthly net burn                    £2,400
Runway on true free cash            7.4 months  (raw balance would suggest 14.8)

Next tax payments: VAT £4,200 on 07/11/2026; PAYE £1,500 on 22/10/2026.
Reference, not advice. Confirm tax figures in your accounting software or with your accountant.
```

Then one or two plain sentences on what the numbers mean: for example, that runway halves once tax is counted, or that the next VAT payment takes free cash below one month of payroll. Do not pad it out.

## What it must get right

- Headline is true free cash, never raw cash.
- Negative true free cash is a warning, not a footnote: "already short by £X", whatever the monthly trend.
- A missing figure is unavailable, never zero.
- Every rate used carries its "as of" date and where to verify it.
- Own-account transfers and money paid in by the director are not income. Leave them out of burn.
- Read only. No payments, transfers, journals or filings, even if a connected tool allows them.

## Example

> **User:** Here's my bank export for July to September. We're VAT registered on quarters to end of September and I pay myself a salary. How long can we last?
>
> **Claude** reads the CSV: balance £35,500 on 30/09, average £10,500 in and £12,900 out a month after leaving out two transfers to the savings pot. It asks one question: "Do you know the VAT figure for the quarter to 30 September? If not, I'll estimate it from the invoices in the statement." The user does not, so Claude estimates £4,200 from sales and purchases, flags it as an estimate, adds the PAYE the user gives (£1,500), a Corporation Tax accrual of 19% on profit to date (£9,100) and a £3,000 dividend the user declared last week, then returns the table above with runway of about 7 months against nearly 15 on the raw balance.

## Configuration

Two things vary per user: **which accounts count as cash** (include savings or tax pot accounts, or keep them separate) and **the window for averaging burn** (default 90 days; longer for seasonal businesses).
