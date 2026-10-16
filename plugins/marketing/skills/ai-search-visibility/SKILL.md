---
name: ai-search-visibility
description: Audits a site or page for how well AI assistants and answer engines (ChatGPT, Claude, Perplexity, Google AI Overviews, Copilot) can find, read and cite it, and rewrites content so it is answer-shaped and quotable. Use when someone asks why AI tools do not mention their business, wants a GEO or AEO audit, asks about llms.txt or AI crawler access in robots.txt, wants a page made more citable, or wants to track AI share of voice. Triggers on "AI search visibility", "GEO audit", "AEO", "get cited by ChatGPT", "show up in AI Overviews", "answer engine optimisation", "make this page answer-shaped", "AI share of voice".
---

# AI search visibility

More buyers now ask an assistant before they search. Being cited in that answer is a
different job from ranking a blue link, and most of the failures are silent: the page looks
fine in a browser, nothing errors, and the crawler that feeds the answer was never let in.

This skill works in a fixed order. **Crawlable before quotable.** Better content on a page
no AI crawler can read changes nothing.

## Pick the mode

| The person wants | Mode |
| --- | --- |
| "Why are we not showing up in AI answers?" / an audit of a site or URL | **Audit** |
| A draft or live page made more citable | **Rewrite** |
| A repeatable way to track whether it is working | **Measure** |

If they give a URL with no other instruction, run Audit. If they paste prose, run Rewrite.

If they ask for a rewrite but you can see a crawl blocker (robots.txt, `noindex`, content
behind JavaScript), the first line of your answer names the blocker and says the rewrite
changes nothing until it is fixed. Then do the rewrite.

## Mode 1: Audit

Work through the four layers in order and stop to report if a lower layer is broken. A
blocked crawler makes every finding above it moot.

### Layer 1: can the AI crawlers get in?

Run the bundled script against the live site, not the repo:

```bash
python3 scripts/ai_visibility_audit.py https://example.com --max 25
```

It reports, for each main AI agent, whether `robots.txt` allows it at the root, whether the
agent is named explicitly, any rules written for agent names that do not exist, whether
`llms.txt` exists, and per-page meta, headings and JSON-LD health. Standard library only, no
install. Use `--single` for one URL and `--json` for machine-readable output.

If you cannot run scripts (for example on claude.ai), fetch `/robots.txt`, `/llms.txt`,
`/sitemap.xml` and a few key pages with whatever fetch tool you have and apply the same
checks by reading. Read `references/technical-discoverability.md` for the agent table and
the checks in full.

The findings that matter most, in order:

1. **Search and user-fetch agents blocked.** Blocking a training crawler is a business
   choice. Blocking the agent that builds the citation index (for example `OAI-SearchBot`,
   `Claude-SearchBot`, `PerplexityBot`, `Bingbot`) means no citations from that engine.
   Say which is which; do not tell anyone to unblock training crawlers.
2. **Rules for agents that do not exist.** `ChatGPTBot` is the common one. It matches
   nothing.
3. **Key pages missing a meta description, canonical or parseable JSON-LD.** When this is
   sitewide, trace it end to end (content field, page component, layout, deployed HTML)
   before fixing; it is usually two missing links, not one.
4. **Sitemap and `noindex` disagreeing.** A page in the sitemap that says `noindex`.
5. **Substance behind JavaScript, logins, forms or cookie walls.** Fetch the raw HTML and
   check the main answer is in it.

### Layer 2: is the content answer-shaped?

For the five to ten pages that matter commercially (pricing, the main service pages, the
best guides), check each against the answer-shape list below. Read
`references/answer-shaped-content.md` for the patterns and examples.

### Layer 3: is it worth citing over a competitor?

Search the person's top three target questions yourself (web search tool if you have one)
and look at which pages get cited. For each, compare: original data, named author, dated
claims, specificity, sources linked. Read `references/citation-worthiness.md`.

### Layer 4: does the wider web agree about them?

Answer engines lean on third-party sources: directories, review sites, comparison articles,
forum threads. Note where competitors are listed and the business is not, and where the
business is listed with an inconsistent name or description.

### Audit output

```markdown
# AI search visibility audit: <site>, <date>

## Verdict
<One paragraph. The single biggest blocker and what fixing it changes.>

## Fix first (silent failures)
| # | Finding | Evidence | Fix | Effort |

## Then (content and authority)
| # | Page | What is missing | Fix |

## Off-site gaps
| Source | Competitors listed? | You listed? | Action |

## Not checked
<Anything you could not see, and why. Never leave this out.>
```

Lead with a recommendation, not a menu. Order fixes by impact over effort.

## Mode 2: Rewrite

Take a draft or a live page and return a rewritten version plus a short list of what
changed. Keep the person's voice and facts. Never invent a statistic, quote, date or source
to satisfy the checklist; where one is missing, leave a marked placeholder like
`[SOURCE NEEDED: average setup time]` and list it at the end.

The answer-shape checklist:

- [ ] The first 40 to 60 words after the title answer the title's question directly.
- [ ] Each section opens with its answer in one or two sentences, then supports it.
- [ ] At least two headings phrased the way someone would type or say the question.
- [ ] Every section makes sense alone. No "as mentioned above", no pronouns pointing out of
      the section, acronyms defined again where they are used.
- [ ] Key terms defined in the form "X is Y".
- [ ] Any X versus Y comparison is a table with short cells.
- [ ] Specific numbers with a named source and a date, not "many" or "most".
- [ ] A named author and a visible last-updated date.
- [ ] Time-sensitive claims dated ("as of March 2026").
- [ ] Nothing important behind a form, login or click-to-reveal.
- [ ] A `FAQPage` or `HowTo` block suggested only if the page genuinely is Q and A or steps,
      and only marking up what is visible on the page.

Return: the rewritten text, then a "Changed" list (one line each), then any placeholders
the person must fill.

## Mode 3: Measure

Rank tracking misses this entirely. The useful metrics are share of voice in AI answers,
citation share, how the business is described, which competitor URLs get cited instead, and
AI-referred traffic.

Set up a **prompt panel**: 15 to 50 real questions buyers ask, run the same way on the same
surfaces each month, recorded in a table. Read `references/measurement.md` for the panel
method, the free data sources (Google Search Console, Bing Webmaster Tools AI Performance,
analytics referrers, server logs) and a monthly review template.

If the person has an SEO or AI-visibility tool connected (an MCP server or API with brand
or AI-citation tracking), use it to populate the same metrics. If not, run the panel
manually or with a web search tool and say which surfaces you could and could not query.

## Rules

- **Fetch the deployed site.** Templates lie. Count what is served.
- **Report what you could not check.** A clean report that skipped three layers is worse
  than an honest partial one.
- **No invented evidence.** Placeholders, not plausible-sounding numbers.
- **Facts about engines drift.** Agent names, report availability and surface behaviour
  change. Check `references/changes-ledger.md` and the vendor's own docs before stating
  one as current.
- **No guarantees.** Nobody controls whether a model cites a page. Say "more likely", not
  "will".

## Example

> **User:** Why does ChatGPT never mention us? We're a small venue-hire company. Site is
> example-venues.co.uk.
>
> **Claude:** *(runs the audit script)* The main blocker is in robots.txt: it has a rule for
> `ChatGPTBot`, which is not a real agent, and a `Disallow: /` under a wildcard for
> anything not named. So `OAI-SearchBot`, the crawler behind ChatGPT's citations, is
> blocked, and so are Perplexity's and Claude's search crawlers. Nothing else matters until
> that is fixed. Second, 14 of 22 pages have no meta description, and the pricing page's
> JSON-LD block has a trailing comma, so it does not parse. Fix those three, then I will
> rewrite the pricing and "how to book" pages so the first paragraph answers the question.

## Configuration

Two things vary per person:

- **The target questions.** The 15 to 50 buyer questions used for Layer 3 and the prompt
  panel. Ask for them, or draft a list from their site and confirm it.
- **The crawler policy.** Whether they want to allow AI training crawlers as well as search
  crawlers. That is their call; this skill only makes sure the choice is deliberate.
