---
name: uk-deadlines
description: Builds a personal 12-month filing calendar for a small UK limited company from its year end, incorporation date and VAT stagger - Companies House accounts and confirmation statement, Corporation Tax payment and CT600, VAT returns, PAYE and year-end payroll dates, and the director's own Self Assessment. Flags anything due within 14 or 60 days and can write an .ics file or create calendar reminders. Use when someone asks "what's due", "when are my accounts due", "when is my confirmation statement due", "when is my VAT return due", "tax deadlines for my company", "filing calendar", "when do I pay Corporation Tax", "when is Self Assessment due", or "put my company deadlines in my calendar". Owns every deadline, due-date and calendar question. Not for how a tax or rule works, rates, or whether something applies; use uk-company-guide for those. Reference, not advice. It reminds, it never files.
---

# UK deadlines

Works out the dates a specific UK limited company has to hit over the next 12 months, in date order, with the nearest ones flagged. It reminds. It never files, pays or contacts HMRC or Companies House.

**Reference, not advice.** The rules are as of 16/10/2026. The dates that actually bind are the ones shown in the company's HMRC business tax account and on its Companies House page. Say this with every calendar you produce.

## What you need from the user

Ask for anything missing, **one question at a time**, in this order. Stop asking once you have enough for a useful calendar.

1. **Incorporation date.** On the company's Companies House page.
2. **Financial year end** (accounting reference date), as day and month. If they do not know: Companies House sets it by default to the last day of the month in which the incorporation anniversary falls, and shows it on the company's page.
3. **VAT.** Not registered, or registered with quarters ending in which months (Mar/Jun/Sep/Dec, Apr/Jul/Oct/Jan, or May/Aug/Nov/Feb), monthly, or on the Annual Accounting Scheme. The VAT online account shows the periods.
4. **Payroll.** Does the company run a payroll (including a director-only salary)?
5. **Director's Self Assessment.** Does the director file a personal return (usually yes if they take dividends above the allowances or have other untaxed income)?

Optional: the date the last confirmation statement was made up to, if it was filed early and moved the cycle.

## How to build it

**If you can run Python**, use the bundled script. It is standard library only and handles the awkward cases (first accounts over 12 months, split Corporation Tax periods, month-end arithmetic):

```bash
python3 scripts/deadlines.py --incorporated 2023-05-15 --year-end 31-03 --vat 1 --employer --director-sa
```

VAT flags: `--vat 1` for quarters ending Mar/Jun/Sep/Dec, `2` for Apr/Jul/Oct/Jan, `3` for May/Aug/Nov/Feb, `monthly`, `annual --vat-year-end DD-MM`, or `none`. Add `--ics deadlines.ics` to write a calendar file with a 14-day reminder on each event (`--remind-days` to change). `--today YYYY-MM-DD` sets the start date.

**If you cannot run code**, apply the rules below by hand. Read [the key deadlines calendar](references/key-deadlines-calendar.md) for the fixed dates and a worked example to check your arithmetic against.

## The rules (as of 16/10/2026)

| Obligation | Rule | Verify at |
|---|---|---|
| Annual accounts to Companies House | 9 months after the year end | gov.uk/file-your-company-annual-accounts |
| First accounts, if they cover more than 12 months | The later of 21 months after incorporation or 3 months after the period end | gov.uk/file-your-company-annual-accounts |
| Corporation Tax payment | 9 months and 1 day after the end of each Corporation Tax period (profits up to £1.5 million; larger companies pay quarterly instalments) | gov.uk/pay-corporation-tax |
| Company Tax Return (CT600) | 12 months after the end of the accounting period. A Corporation Tax period is at most 12 months, so accounts over 12 months need two returns, both due 12 months after the accounts end | gov.uk/corporation-tax-accounting-period |
| Confirmation statement | Within 14 days after each 12-month review period ends (from incorporation, or from the last statement's date) | gov.uk/guidance/filing-your-companys-confirmation-statement |
| VAT return and payment (quarterly or monthly) | 1 calendar month and 7 days after the period ends | gov.uk/submit-vat-return |
| VAT, Annual Accounting Scheme | Return and balance within 2 months of the VAT year end, with interim payments during the year | gov.uk/vat-annual-accounting-scheme |
| PAYE and NI | 22nd of the following tax month if paying electronically (quarterly payers: 22nd after each tax quarter) | gov.uk/pay-paye-tax |
| Payroll year end | Final FPS by the last payday before 05/04; P60s by 31/05; P11D and P11D(b) by 06/07; Class 1A NI by 22/07 (only if benefits were provided) | gov.uk/payroll-annual-reporting |
| Director's Self Assessment | Online return and balancing payment 31 January; second payment on account 31 July; paper return 31 October | gov.uk/self-assessment-tax-returns/deadlines |

A deadline that lands on a weekend or bank holiday does not move. HMRC needs the money to arrive by that date, so pay earlier.

## Output

A table in date order: date, days away, flag, what, and who it goes to. Flag anything within 14 days as **due soon** and anything within 60 days as **upcoming**. Under the table:

- one line naming the first accounting period end you used, and whether it came from the user or the Companies House default
- assumptions you made (profits under £1.5 million, no associated companies changing the instalment test, no change of year end)
- the line: "Reference, not advice. Confirm each date in your HMRC business tax account and on the company's Companies House page."

## Reminders

Offer reminders once, after the table. Do not create them without a yes.

- **If a calendar or reminders tool is connected** (Google Calendar, Outlook, Apple Calendar or Reminders), create one all-day event per deadline titled "DUE: ..." with a reminder 14 days before (or the lead time the user asks for). List what you created.
- **Otherwise**, generate the `.ics` file with the script (or write it by hand) and tell the user to import it into their calendar app.

Do not schedule recurring jobs. The calendar is a snapshot: suggest re-running it after a change of year end, VAT registration, starting payroll, or each April.

## Example

> **User:** Company incorporated 15 May 2023, year end 31 March, VAT quarters to end of Mar/Jun/Sep/Dec, I pay myself through payroll. What's due?
>
> **Claude** runs the script and returns, among others: VAT for the quarter to 30/09/2026 due 07/11/2026; accounts for the year to 31/03/2026 due 31/12/2026; Corporation Tax for that year due 01/01/2027; CT600 due 31/03/2027; confirmation statement due 29/05/2027 for the review period ending 15/05/2027; PAYE on the 22nd of each month. Then it offers to add them to the user's calendar with 14-day reminders.

## Configuration

Two things vary per user: **the reminder lead time** (default 14 days) and **whether to include the director's personal Self Assessment dates** alongside the company's.
