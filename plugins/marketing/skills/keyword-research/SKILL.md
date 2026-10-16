---
name: keyword-research
description: Turns a handful of seed topics into a clustered keyword map - expanded terms, a demand tier, search intent, one target page per cluster, and where the gaps are - on a free stack with no paid SEO tool required. Uses Google Search Console, Keyword Planner, Google Trends and live search results when available, and any connected SEO tool if there is one. Use when someone asks "what should we write about", "keyword research", "build a keyword map", "what keywords should we target", "find content gaps", "which topics have demand", "two of our pages compete for the same keyword", "should we write another post for this term", or wants to plan a blog or landing pages around search or fix keyword cannibalisation.
---

# Keyword research

The output is a **keyword map**: every candidate term with its cluster, intent, a demand
tier, where that number came from, and whether the site already covers it. One cluster maps
to one page. That map is what content planning runs on.

The free stack gets you a reliable high / medium / low read on demand and the direction it
is heading. It does not get you exact monthly volumes. Say so in the output rather than
dressing ranges up as precision.

## Step 0: what you need from the person

Ask in one message, then start:

1. **Seeds.** Three to ten topics or phrases. "What do you sell and who buys it?" is enough
   to draft seeds yourself; confirm them.
2. **Site URL**, so you can check what already exists.
3. **Market.** Country and language. Demand and results differ by market.
4. **Brand terms.** Their own brand and product names, so branded searches are separated.

Optional: a Search Console export (Performance report, last 3 to 12 months, by query and by
page). It is the best free data there is.

## Step 1: check what data you can actually get

Before any research, list the sources and mark each available or not. Read
`references/data-sources.md` for what each gives and its limits.

| Source | Gives | How you get it |
| --- | --- | --- |
| Google Search Console | Real impressions, clicks, position for terms the site already shows for | A connected Search Console tool, or an export the person pastes |
| Google Keyword Planner | Volume ranges and related terms | The person runs it in a free Google Ads account and pastes the export |
| Google Trends | Relative interest over time, rising related queries | trends.google.com by hand, or a connected tool |
| Live search results | Autocomplete, "People also ask", related searches, the top-ranking pages | A web search or scraping tool, or the person pastes what they see |
| A connected SEO tool (optional) | Exact volumes, difficulty, competitor keywords | Any MCP server or API the person has connected, for example Ahrefs, Semrush or similar |

Rules:

- **A missing source is not an error.** Continue with what you have.
- **Report every gap at the top of the output.** No Search Console means you cannot tell
  what the site already ranks for; say that plainly.
- **Zero sources is the only stop.** Even then, offer to work from the person's own
  knowledge of customer questions and mark everything as unverified.
- **A paid tool improves confidence, it does not change the method.** If one is connected,
  use it to fill the same fields.

## Step 2: expand the seeds

For each seed, collect candidate terms from:

- Autocomplete suggestions (try the seed plus a to z, and with "how", "best", "vs",
  "for").
- "People also ask" questions and the related searches at the bottom of the results.
- Keyword Planner related terms, if available.
- Rising related queries in Google Trends.
- The connected SEO tool's related and matching terms, if available.
- Questions customers actually ask: sales calls, support tickets, reviews, forums.

Deduplicate and normalise (lower case, trimmed). Drop terms that are clearly off-market.
Aim for 50 to 300 candidates. More is rarely useful at this stage.

## Step 3: attach a demand tier

For each term give a **tier** and say how confident you are. Read
`references/data-sources.md` for how to triangulate.

| Tier | Default threshold (monthly searches) |
| --- | --- |
| high | 10,000 or more |
| medium | 1,000 to 9,999 |
| low | under 1,000 |
| unknown | no source covered it |

Recalibrate for a niche. In a narrow B2B market, 500 a month may be "high". Say which scale
you used.

Confidence: `exact` (paid tool), `range` (Keyword Planner bracket), `observed` (Search
Console impressions), `relative` (Trends index only), `inferred` (appears in autocomplete
or "People also ask", no number).

Search Console beats estimates for terms it covers. Never present the midpoint of a
Keyword Planner range as a fact.

## Step 4: classify intent

Intent decides the page type. Getting it wrong wastes the work even if the page ranks.

| Intent | Signal | Build |
| --- | --- | --- |
| informational | how, what, why, guide, examples | Article, guide, glossary entry |
| commercial | best, vs, alternatives, review | Comparison page, "best X for Y", alternatives page |
| transactional | price, buy, book, demo, free trial, near me | Product, pricing, booking or landing page |
| navigational | a brand name, login | Usually nothing. Competitor brand plus "alternative" is the exception: that is commercial. |

Run the bundled classifier for a first pass:

```bash
python3 scripts/classify_intent.py keywords.txt --brand "yourbrand,yourproduct" --header
```

It is deterministic and token-based, standard library only. Then check the clusters that
matter against the live results page: if the top ten are all product pages, the intent is
transactional whatever the words say. Read `references/search-intent.md` for the token
lists and edge cases.

## Step 5: cluster

One cluster is one page. Two pages aimed at the same cluster compete with each other.

1. **First pass, shared head term.** Group terms that share the core noun phrase ("crm for
   charities", "charity crm software"). Split a group if its terms have different intent.
2. **Second pass, results overlap.** For the boundaries that matter, compare the top ten
   results. If two terms share a lot of the same ranking pages, the search engine treats
   them as one need.

If you have the top results per term (from a search tool, a connected SEO tool, or pasted),
the bundled script does the second pass:

```bash
python3 scripts/serp_cluster.py serps.tsv --threshold 0.4
```

Input is `keyword<TAB>url`, one row per result. Read `references/clustering-and-gaps.md`
for the method and how to tune the threshold.

## Step 6: find the gaps

For each cluster, compare demand with what the site already has:

- `covered`: the site ranks in the top 5 for the cluster's main terms.
- `under-ranked`: the site ranks 6 to 20. Often the best return: improve or merge the
  existing page.
- `gap`: nothing ranks. A new page is needed.
- `unknown`: no Search Console data and no obvious matching page.

Without Search Console, check the sitemap and a `site:` search for an existing page on the
cluster topic, and mark the result as lower confidence.

Then prioritise: demand tier, then intent that converts for this business, then how beatable
the current top results look (forums and thin pages are beatable; big reference sites
usually are not), then effort.

## Step 7: write the keyword map

```markdown
# Keyword map: <site or topic>, <date>

## Sources
- Used: <list>
- Missing: <list, and what that means for confidence>
- Demand scale: <default or recalibrated, and why>

## Top 5 opportunities
| Cluster | Intent | Demand | Status | Recommended page | Why now |

## Clusters
| Cluster | Main term | Terms | Intent | Demand | Status | Target page |

## Full keyword list
| Term | Cluster | Intent | Demand | Confidence | Source | Status |

## Cannibalisation warnings
<Clusters where two existing pages compete, and which one should own it.>
```

Lead with the top five and a recommendation. The full list is for reference.

Offer a CSV of the full list if the person wants it in a spreadsheet.

## Rules

- **No invented numbers.** If no source gave a figure, the tier is `unknown`.
- **Market matters.** Do not apply US volumes to a UK business.
- **One cluster, one page.** If a new page would overlap an existing one, recommend
  improving the existing page instead.
- **AI answers change the value of informational terms.** Simple definitional questions
  are increasingly answered on the results page or in an assistant. Weight them for
  citation potential, not only clicks; the `ai-search-visibility` skill covers that side.
- Tool limits drift. Check `references/changes-ledger.md` before relying on one.

## Example

> **User:** Keyword research for my bookkeeping practice in Bristol. Seeds: bookkeeping,
> VAT returns, Xero setup. No paid tools.
>
> **Claude:** No Search Console connected, so I cannot see what you already rank for; I
> will check your sitemap instead and mark coverage as lower confidence. Using autocomplete,
> "People also ask" and Trends. *(...)* Top opportunity: "bookkeeper Bristol" and five
> close variants form one transactional cluster with medium local demand, and your services
> page does not mention Bristol in the title or headings. That is a fix to an existing page,
> not a new one. Second: a "how to do a VAT return in Xero" cluster, informational, medium
> demand, where the top results are forum threads. A clear step-by-step guide can beat
> those.

## Configuration

Two things vary per person:

- **Market and demand scale.** Country, language, and whether the default tiers suit their
  niche.
- **Which data sources they have.** Search Console access, a Google Ads account for Keyword
  Planner, and any connected SEO tool. The skill works with none of them, but says how much
  less it can see.
