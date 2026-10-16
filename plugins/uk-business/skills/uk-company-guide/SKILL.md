---
name: uk-company-guide
description: Answers practical questions about running a small UK business - sole trader or limited company - from a dated, sourced reference set covering legal forms, registration, Companies House compliance, Corporation Tax, VAT, Self Assessment, Making Tax Digital, personal tax and National Insurance, paying yourself as a director, employing people, data protection and marketing, and selling to consumers. Use when someone asks "do I need to register for VAT", "what Corporation Tax rate do I pay", "salary or dividends", "what do I have to file each year", "can I email this list", "do I need to pay holiday pay", or any UK small-business tax, filing or compliance question about how the rules work. Not for when something is due or a filing calendar ("when are my accounts due", "what's due this month"); use uk-deadlines for those. Reference, not advice.
---

# UK company guide

A routing skill over fifteen reference files on running a small UK business. Each file is plain English, carries the date it was checked and lists the official pages it used (GOV.UK, HMRC, Companies House, ICO, legislation.gov.uk).

**This is reference, not legal, tax or accounting advice.** Say so in every answer that involves a rate, a threshold, a deadline or a decision with real money at stake, and point the reader to an accountant or adviser for the decision itself.

## How to answer

1. **Route.** Find the question in the table below and read the matching reference file before answering. Read two if the question spans them (salary versus dividends touches both director pay and personal tax). Do not answer a figure from memory.
2. **Check the ledger for dated figures.** Before quoting any threshold, rate, fee, deadline or commencement date, read [references/changes-ledger.md](references/changes-ledger.md). It lists what moves, when it took effect and what to watch.
3. **Answer plainly.** Lead with the answer, then the rule behind it, then what to do. Use the reader's numbers if they gave them. Show the arithmetic for any tax figure.
4. **Date and source it.** Every figure you quote carries its tax year or "as of" date and the official page to verify it at. Example: "£90,000 (VAT registration threshold, in force since 01/04/2024; verify at gov.uk/register-for-vat)."
5. **Flag what is moving.** If the topic is mid-change (Making Tax Digital for Income Tax, the Employment Rights Act 2025, Companies House reforms, subscription rules), say so and name the date.
6. **Know the edge.** Figures are for the 2026-27 tax year and for England, Wales and Northern Ireland unless stated. Scotland sets its own income tax rates and bands on earnings and trading profit. If the reader is in Scotland, say so and point them at gov.uk/scottish-income-tax.

## Routing table

| Question is about | Read |
|---|---|
| Sole trader, partnership, LLP or limited company; when to incorporate | [references/legal-forms.md](references/legal-forms.md) |
| Registering with HMRC or Companies House, UTR, company number, identity verification, ICO fee, trade marks, business bank account | [references/registration-and-identifiers.md](references/registration-and-identifiers.md) |
| Annual accounts, confirmation statement, company size, late filing penalties, registers, directors' duties, director's loan account, striking off | [references/company-annual-compliance.md](references/company-annual-compliance.md) |
| Corporation Tax rates, Marginal Relief, associated companies, CT600, instalments, deductions, capital allowances, losses | [references/corporation-tax.md](references/corporation-tax.md) |
| Whether to register for VAT, the threshold, voluntary registration, VAT rates, selling digital services to the EU, reverse charge | [references/vat-registration-and-thresholds.md](references/vat-registration-and-thresholds.md) |
| Flat Rate, Cash or Annual Accounting schemes, MTD for VAT, return deadlines, VAT penalties and interest, VAT invoices | [references/vat-schemes-mtd-and-returns.md](references/vat-schemes-mtd-and-returns.md) |
| Who files Self Assessment, deadlines, payments on account, penalties, trading allowance, expenses, cash basis | [references/self-assessment.md](references/self-assessment.md) |
| Making Tax Digital for Income Tax: who is in scope from 2026, 2027, 2028, quarterly updates, exemptions | [references/making-tax-digital-income-tax.md](references/making-tax-digital-income-tax.md) |
| Salary, dividends, pension, PAYE for a director, Employment Allowance, expenses and benefits | [references/paying-yourself-as-a-director.md](references/paying-yourself-as-a-director.md) |
| Personal Allowance, income tax bands, dividend and savings tax, Class 2 and Class 4 National Insurance | [references/personal-tax-and-national-insurance.md](references/personal-tax-and-national-insurance.md) |
| Freelancer or employee, IR35, first employee, minimum wage, holiday, sick pay, auto-enrolment, Employment Rights Act 2025 | [references/employing-people.md](references/employing-people.md) |
| UK GDPR, lawful basis, breaches, email and text marketing (PECR), cold calling, cookies, ICO fines | [references/data-protection-and-marketing.md](references/data-protection-and-marketing.md) |
| Consumer rights, refunds, 14-day cancellation, drip pricing, fake reviews, subscriptions | [references/selling-to-consumers.md](references/selling-to-consumers.md) |
| What is due when, month by month, and how to work out a company's own dates | [references/key-deadlines-calendar.md](references/key-deadlines-calendar.md) |
| Anything with a date or a number that moves | [references/changes-ledger.md](references/changes-ledger.md) |

Questions about when something is due, or a filing calendar from a company's own year end and VAT quarters, belong to the `uk-deadlines` skill in this plugin. The calendar reference above is the single copy both skills use. For "how much of my cash is actually mine", use `cash-runway`.

## Confidence

Three files are marked medium confidence and each says why at the top: registration and identifiers, employing people, and data protection and marketing. When you answer from one of them, tell the reader and point at the primary source cited in that file.

## Staleness

The references were researched on 06/10/2026, and the most load-bearing figures were re-checked on gov.uk on 16/10/2026 (the list is in the changes ledger). Re-check by 06/01/2027, or sooner after a Budget, a Spring Statement or new commencement regulations.

If today's date is past 06/01/2027, or a new tax year has started since 06/04/2026, say plainly that the figures may be out of date. If you have web search, check the figure on the GOV.UK page cited in the reference before quoting it, and say which date you checked it. If you do not, quote the reference figure with its date and tell the reader to verify it.

## What this skill does not do

- It does not give personal tax, legal or accounting advice, file anything, or contact HMRC or Companies House.
- It does not decide for the reader. It sets out the rule, the trade-off and the next step, and names the decision that needs an accountant.
- It does not cover Scotland's income tax bands in detail, R&D relief in depth, or sector-specific regulation (financial services, food hygiene, alcohol licensing).

## Example

> **User:** My company made £120,000 profit. What Corporation Tax will it pay?
>
> **Answer:** About **£28,050**, assuming a 12-month accounting period and no associated companies. Profit between £50,000 and £250,000 is charged at the 25% main rate less Marginal Relief:
>
> - 25% of £120,000 = £30,000
> - Marginal Relief = 3/200 x (£250,000 minus £120,000) = £1,950
> - £30,000 minus £1,950 = £28,050
>
> Each extra pound in this band is effectively taxed at 26.5%. Rates as of the financial year starting 01/04/2026, unchanged since 01/04/2023; verify at gov.uk/corporation-tax-rates. If you own another company, the £50,000 and £250,000 limits are divided between them, which changes the answer. Reference, not advice: check with your accountant before relying on it.

## Configuration

One thing varies: **where the business is**. The references assume England, Wales or Northern Ireland. For a Scottish taxpayer, income tax on salary and trading profit uses Scottish bands; dividends, savings and National Insurance do not change.
