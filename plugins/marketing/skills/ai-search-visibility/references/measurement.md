# Measuring AI search visibility

A page can lose its blue-link position and still be the source an AI answer cites, or hold
position one and never appear in an AI Overview. Rank is a leading indicator, not the
outcome.

## Contents

- The five metrics
- The prompt panel
- Free data sources
- Monthly review template
- When a number moves

## The five metrics

| Metric | Question it answers |
| --- | --- |
| **AI share of voice** | Across the target questions, in what share of AI answers does the business appear at all, cited or named? |
| **Citation share** | When it appears, how often is it a linked source rather than just a mention? |
| **Framing** | When it appears, is the description accurate, and is the tone positive, neutral or negative? |
| **Cited-source gap** | When a competitor is cited and the business is not, which URL won? This is the most actionable number: it names the page to beat or the directory to get listed in. |
| **AI-referred traffic** | Visits arriving from AI surfaces, from analytics referrers. |

## The prompt panel

The main instrument. A fixed list of 15 to 50 questions real buyers ask, run the same way on
a fixed set of surfaces, on a fixed schedule.

Building the panel:

- Mix question types: "best X for Y", "X vs Y", "how much does X cost", "how do I X",
  "is X worth it", and a couple that name the business directly.
- Source the wording from sales calls, support tickets, search suggestions and "People also
  ask" boxes.
- Keep it stable. Comparability over time is the whole value. Add questions sparingly and
  never silently swap them.

Running it:

- Use the same surfaces each time (for example ChatGPT with search, Perplexity, Google AI
  Overviews, Copilot, Claude with search).
- Use logged-out or fresh sessions where possible, since personalisation skews results.
- Record one row per question per surface.

Recording template:

```markdown
| Date | Surface | Question | Appears? | Cited (linked)? | Framing | Competitors cited | Top cited URL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-01 | Perplexity | best venue booking software for small venues | yes | no | neutral | A, B | example.com/compare |
```

AI answers vary between runs. For important questions, run them two or three times and
record the majority result. Do not read meaning into a one-question swing.

If a web search tool is available, it can stand in for some surfaces, but say which ones it
represents. If an SEO or brand-monitoring tool with AI citation tracking is connected, use
it to fill the same table at greater scale. The metrics do not change, only how much of the
panel you can run.

## Free data sources

- **Google Search Console.** Impressions, clicks and position for the index that feeds AI
  Overviews. As of October 2026 AI Overview and AI Mode traffic is counted inside the
  normal web search report rather than broken out separately; check for a dedicated report
  before assuming it is still absent.
- **Bing Webmaster Tools, AI Performance report.** Launched in public preview in February
  2026. Shows how often a site is cited in Copilot and Bing AI answers, which pages, and
  sample grounding queries. It counts citations, not clicks or prominence. Verify current
  availability at bing.com/webmasters.
- **Analytics referrers.** Filter sessions by AI surface referrer hosts (for example
  chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com, claude.ai). Many
  clicks arrive with no referrer at all, so treat this as a floor.
- **Server or CDN logs.** Requests from AI crawler user agents show which pages are being
  fetched for indexing or for live answers.
- **Manual reading.** For the highest-value questions, read the actual answers. Automated
  yes/no checks miss wrong facts and poor framing.

## Monthly review template

```markdown
# AI visibility review: <month>

## Headline
Share of voice across the <N>-question panel: X% (last month Y%, three months ago Z%).

## What moved
- <one line, with a number>

## By surface
| Surface | 3 months ago | Last month | This month |

## Strongest questions (we appear consistently)
## Weakest questions (we are consistently absent)

## Cited-source gap
| Source cited instead of us | Times cited | Are we listed there? | Action |

## Traffic
AI-referred sessions: N (last month M). Top landing page: <url>.

## Bing AI Performance (if set up)
| Page | Citations this month | Last month |

## The one action for next month
<Single highest-impact action, with the reason.>
```

Lead with the trend and the single most important action, not the full table.

## When a number moves

Before blaming or crediting content, check whether the surface changed: a new model, a new
search partner, a change in when AI Overviews appear. A surface change and a content problem
look identical on a dashboard. See `changes-ledger.md`.
