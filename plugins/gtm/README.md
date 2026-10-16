# gtm

Outbound for founders and small teams selling B2B. Two skills that cover the path from
"who should I contact, and why now?" to "the first sequence is live and landing in inboxes".

They are written for people doing the selling themselves, not for a sales team with a
tooling budget. Each works with no integrations; where a tool such as web search helps,
the skill uses it if present and falls back to working from what you give it.

## Skills

| Skill | Use it when |
| --- | --- |
| **signal-prospecting** | You need a short list of accounts with a real, recent reason to contact each one, the right person there, and a sourced use case. |
| **outbound-sequences** | You are designing or fixing a cold outreach sequence, or setting up a sending domain and want to check it will not end up in spam. |

Run them in that order, or use either on its own.

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
- `signal-prospecting` uses public business information only, cites a source and date for
  every claim, and respects opt-outs.

## Licence

MIT.
