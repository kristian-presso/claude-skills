# gtm

Go-to-market for anyone selling B2B: founders doing their own sales, account executives
with a named territory, account managers growing a book, consultants. Six skills that
cover the path from "who should I go after, and in what order?" to "the first messages
are drafted and landing in inboxes".

They are written for people doing the selling themselves, not for a sales team with a
tooling budget. Each works with no integrations; where a tool such as web search helps,
the skill uses it if present and falls back to working from what you give it.

## Skills

| Skill | Use it when |
| --- | --- |
| **gtm-motion** | You want a repeatable motion: which accounts, which signals, which personas, and a weekly routine. Start here. |
| **prospect-radar** | You want new companies found for you every day or week: it builds and tests news, hiring and competitor-change feeds, then turns each run into a short sourced list with drafts. |
| **signal-prospecting** | You need a short list of accounts with a real, recent reason to contact each one, the right person there, and a sourced use case. |
| **account-play** | One account deserves real effort: map who decides, propose two or three use cases, plan a multi-person play and draft the first touches. |
| **pre-send-check** | Before any outreach goes out: eight checks (already in touch, meeting coming up, whose account, opted out and more) that turn a plausible draft into a sendable one. |
| **outbound-sequences** | You are designing or fixing a cold outreach sequence, or setting up a sending domain and want to check it will not end up in spam. |

Run them in that order, or use any one on its own.

## Install

In Claude Code:

```bash
/plugin marketplace add kristian-presso/claude-skills
/plugin install gtm@claude-skills
```

## Notes

- Benchmarks and thresholds in these skills (reply rates, sending limits, legal
  penalties) are dated and say where to verify them. Vendor-reported numbers are labelled
  as such.
- The legal summary in `outbound-sequences` is reference, not legal advice.
- `gtm-motion` asks employed sellers whether their employer allows customer data in
  outside AI tools, and runs on public information when it does not.
- `signal-prospecting` and `account-play` use public business information only, cites a source and date for
  every claim, and respects opt-outs.

## Licence

MIT.
