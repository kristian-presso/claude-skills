# uk-business

Running a small UK limited company with Claude: the rules, the deadlines, and knowing how much cash you really have.

Three skills for founders and directors of small UK companies (and sole traders, for the guide). They exist because once you run the books yourself, nobody else is watching the dates or reminding you that the VAT in your account is not yours.

> **Reference, not advice.** These skills explain the rules and do the arithmetic. They are not legal, tax or accounting advice, they never file or pay anything, and the figures change. Every rate, threshold and deadline carries the date it was checked and the official page to verify it at. For decisions with real money at stake, talk to an accountant.

## Skills

| Skill | Use it when |
|---|---|
| **uk-company-guide** | You have a question about UK company tax, VAT, Companies House, paying yourself, employing people, data protection or consumer law, and want a dated, sourced answer. |
| **uk-deadlines** | You want your company's own filing and payment calendar for the next 12 months, worked out from its year end, incorporation date and VAT quarters, and optionally put in your calendar. |
| **cash-runway** | You want to know how much cash is actually yours after VAT, Corporation Tax and PAYE, and how many months it lasts, from a bank export, typed numbers or a connected accounting tool. |

## Install

In Claude Code:

```bash
/plugin marketplace add kristian-presso/claude-skills
/plugin install uk-business@claude-skills
```

On claude.ai or the Claude desktop app, upload any single skill folder from `skills/` as a custom skill.

## How fresh is it

The reference material was researched against GOV.UK, HMRC, Companies House, the ICO and legislation.gov.uk on 06/10/2026. The figures most decisions hang on were re-checked on gov.uk on 16/10/2026 and all matched:

- VAT registration threshold: £90,000
- Corporation Tax: 19% up to £50,000, 25% over £250,000, Marginal Relief between
- Personal Allowance 2026-27: £12,570
- Dividend allowance 2026-27: £500; rates 10.75%, 35.75%, 39.35%
- Employer NI 2026-27: 15% above a £5,000 secondary threshold

Re-check by 06/01/2027, or sooner after a Budget. The full list of moving figures, with effective dates, is in `skills/uk-company-guide/references/changes-ledger.md`. Figures are for England, Wales and Northern Ireland; Scotland has its own income tax bands.

## Scripts

`uk-deadlines` and `cash-runway` each ship a small Python script (standard library only, no installs) for the date arithmetic and the bank CSV maths. The skills work without them: Claude falls back to doing the calculation by hand and showing the working.

## Feedback

Used one of these? [Tell me what worked and what broke](https://tally.so/r/7XlJbL?source=uk-business) - two minutes, every answer read.

## Licence

MIT.
