# Skills that run my business, for Claude

Skills from the agents that run my business, for Claude Code and the Claude app.

I run a small software business with AI agents doing most of the work: inbox triage, content, sales research, tax deadlines, shipping code. Every time something worked, I wrote down the judgement behind it as a skill, so I never had to explain it twice. These are the ones that work outside my own setup. Free, MIT licensed, no sign-up.

```bash
/plugin marketplace add kristian-presso/claude-skills
/plugin install operator-discipline@claude-skills
```

Swap `operator-discipline` for any plugin below, or install all five. `pushback` and `solutions-shape` work best always-on: the operator-discipline README has a few lines to paste into your `CLAUDE.md`.

## What is in it

### operator-discipline

How an agent behaves when it is doing real work for a busy person. **Start here.**

| Skill | Use it when |
| --- | --- |
| [pushback](plugins/operator-discipline/skills/pushback/SKILL.md) | A brief is vague, contradicts an earlier decision, or has one expensive wrong reading. One focused question, before any work starts. |
| [solutions-shape](plugins/operator-discipline/skills/solutions-shape/SKILL.md) | The agent is about to report a problem. It hands back finding, recommendation, action instead. |
| [setup-guide](plugins/operator-discipline/skills/setup-guide/SKILL.md) | You need a setup guide a stranger can follow first time, proven by running it. |
| [write-playbook](plugins/operator-discipline/skills/write-playbook/SKILL.md) | A recurring process lives in someone's head and needs writing down with an owner and a done-check. |
| [meeting-notes](plugins/operator-discipline/skills/meeting-notes/SKILL.md) | A transcript or notes need turning into decisions, owned actions, open questions and a follow-up email. |
| [level-up](plugins/operator-discipline/skills/level-up/SKILL.md) | You want the single next thing worth automating, not a list of twenty. |

### agent-builder

For people building with Claude and MCP.

| Skill | Use it when |
| --- | --- |
| [mcp-server-builder](plugins/agent-builder/skills/mcp-server-builder/SKILL.md) | Building or auditing an MCP server: outcome-shaped tools, auth at the boundary, tests, deployment and directory listing. Includes a tested Python starter. |
| [mcp-app-builder](plugins/agent-builder/skills/mcp-app-builder/SKILL.md) | Building an MCP App (interactive UI inside the chat) and proving it works before you ship it. |
| [agent-security](plugins/agent-builder/skills/agent-security/SKILL.md) | Giving an agent a new tool, credentials or untrusted input. Checks for the lethal trifecta and removes a leg rather than adding warnings. |
| [ship-with-agents](plugins/agent-builder/skills/ship-with-agents/SKILL.md) | Running real work through coding agents: discuss, plan, execute, verify blind, ship. |
| [skill-builder](plugins/agent-builder/skills/skill-builder/SKILL.md) | Turning a process you do by hand into a reusable skill, with a validator. |

### gtm

Go-to-market for anyone selling B2B - founders, account executives with a named territory, account managers growing a book.

| Skill | Use it when |
| --- | --- |
| [gtm-motion](plugins/gtm/skills/gtm-motion/SKILL.md) | Designing the motion: ICP, tiered accounts, weighted buying signals, personas and a weekly routine. |
| [account-play](plugins/gtm/skills/account-play/SKILL.md) | Planning one account: who decides, two or three proposed use cases, a multi-person play and first-touch drafts. |
| [signal-prospecting](plugins/gtm/skills/signal-prospecting/SKILL.md) | Finding prospects from public signals (funding, hiring, launches) with a sourced, dated reason to contact each one. |
| [outbound-sequences](plugins/gtm/skills/outbound-sequences/SKILL.md) | Designing an outbound sequence, with a deliverability pre-flight before a single email goes out. |

### marketing

Content and search, built to get you cited by AI answer engines as well as ranked by Google.

| Skill | Use it when |
| --- | --- |
| [ai-search-visibility](plugins/marketing/skills/ai-search-visibility/SKILL.md) | Checking whether ChatGPT, Claude and Perplexity can find and cite your site, and rewriting pages so they get cited. |
| [keyword-research](plugins/marketing/skills/keyword-research/SKILL.md) | Turning seed terms into a clustered keyword map on a free stack. |
| [content-atomisation](plugins/marketing/skills/content-atomisation/SKILL.md) | Turning one long piece into a week of channel-specific posts. |
| [linkedin-post](plugins/marketing/skills/linkedin-post/SKILL.md) | Drafting LinkedIn posts that sound like you, learned from your own past posts. |
| [seo-schema-gate](plugins/marketing/skills/seo-schema-gate/SKILL.md) | Checking structured data and meta tags before a page publishes, and the live URL after. |

### uk-business

Running a small UK limited company. Reference, not advice: every figure carries the date it was checked and the official page to verify it.

| Skill | Use it when |
| --- | --- |
| [uk-company-guide](plugins/uk-business/skills/uk-company-guide/SKILL.md) | You have a question about Corporation Tax, VAT, Companies House, paying yourself, employing people or data protection. |
| [uk-deadlines](plugins/uk-business/skills/uk-deadlines/SKILL.md) | You want your company's own filing calendar for the next 12 months. |
| [cash-runway](plugins/uk-business/skills/cash-runway/SKILL.md) | You want to know how much cash is yours after VAT, Corporation Tax and PAYE, and how long it lasts. |

## Using them in the Claude app

On claude.ai or the Claude desktop app, download this repository as a zip (Code, then Download ZIP), take the folder of the skill you want (the one containing `SKILL.md`), zip that folder on its own and upload it in your skills settings. Each skill works on its own.

## How they are built

A skill is not documentation. It is the judgement you would give a capable new hire on their first day: which check to run first, when to stop and ask, what done actually means. If a skill only said what you would find in public docs, it is not here.

Every skill in this repo passed the same test: it works in your setup with nothing but Claude. No accounts, no config files, no paid tools. Where a connected tool helps (web search, an SEO tool, an accounting package, a calendar) the skill uses it if it is there and falls back to a manual path if it is not. Scripts are standard-library Python or plain shell, and optional.

Facts that change - tax rates, API behaviour, platform limits, directory rules - carry an "as of" date and the source to re-check them against.

What is deliberately not here: skills bound to my own repos, memory layout or tone of voice, and anything that is really someone else's work. Vendor skills belong to their vendors, and book frameworks belong to their authors.

## Contributing

Issues are the most useful thing you can send. If a skill fired when it should not have, did not fire when it should, or produced the wrong thing, tell me what you typed and what happened. That is exactly the judgement the skill was missing.

## All of it in one install

These skills are a slice of a larger system I use to run my business. If you would rather have the whole library in one install that already knows your business, remembers it between chats and keeps itself up to date, that is [Corey](https://getcorey.ai). It is free for individuals.

## Licence

[MIT](LICENSE). Take them, fork them, strip the parts you disagree with.

How these were built, and why, is written up at [kristianpapadakis.com/guides](https://kristianpapadakis.com/guides).
