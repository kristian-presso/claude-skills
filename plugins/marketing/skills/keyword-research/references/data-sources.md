# Data sources and demand estimation

How to estimate search demand without paying for a keyword tool, what each free source
gives, and where it runs out. The honest summary: the free stack tells you whether a term
is roughly high, medium or low demand and which way it is trending. Exact monthly volume
needs a paid tool.

## Contents

- Google Search Console
- Google Keyword Planner
- Google Trends
- Live search results
- An optional paid SEO tool
- Triangulating
- The record for each term
- When sources are missing

## Google Search Console

**Gives:** real impressions, clicks, average position and click-through rate for every query
where the site appeared in Google results.

**Use it to:**

- Replace estimates with real impressions for any term it covers. Real beats estimated.
- Find under-ranked terms: high impressions, position 6 to 20, few clicks. These are
  usually the cheapest wins.
- Map which page currently ranks for which query, for gap analysis and cannibalisation
  checks.

**Limits:** only shows queries where the site already appears, so it cannot discover new
topics. Data lags two to three days. The interface keeps 16 months. Very rare queries are
hidden for privacy, so totals by query will not add up to totals by page.

**Getting the data:** a connected Search Console tool, or ask for an export: Performance,
Search results, last 3 to 12 months, Queries tab and Pages tab.

## Google Keyword Planner

**Gives:** monthly search volume ranges and related keyword ideas, with a low / medium / high
competition label (that label is about advertisers, not organic difficulty).

**Use it to:** expand seeds and sort candidates into rough tiers.

**Limits:** needs a Google Ads account. Accounts with little or no ad spend see wide ranges
(for example "100 to 1K"). It is a web interface; the API needs a full Google Ads API setup.
No trend direction or rising queries.

**Getting the data:** the person runs it at ads.google.com (Tools, Keyword Planner,
"Discover new keywords" and "Get search volume and forecasts") and pastes or uploads the
export.

## Google Trends

**Gives:** relative interest over time (0 to 100, where 100 is the peak in the chosen
window), by region, plus top and rising related queries.

**Use it to:**

- Check a term is stable or growing, not declining.
- Spot seasonality (a term that peaks every January).
- Compare two phrasings to see which people actually use.
- Find rising related queries to add to the candidate list.

**Limits:** relative only. An index of 80 does not convert to a search count without an
anchor from another source. Low-volume terms often show no data.

**Getting the data:** trends.google.com by hand, a connected tool, or an official API if the
person has access. The popular unofficial Python wrapper `pytrends` was archived in 2025 and
is unreliable; do not build on it.

## Live search results

**Gives:** autocomplete suggestions, "People also ask" questions, related searches, the
features present (featured snippet, AI Overview, local pack, shopping results, videos) and
the pages that rank.

**Use it to:**

- Expand seeds with the phrasing real people use.
- Read intent from what ranks (all product pages means transactional).
- Judge how beatable the current results are.
- Collect the top ten URLs per term for results-overlap clustering.

**Limits:** a point-in-time snapshot. Results vary by location, device and personalisation.
Layouts change often. Scraping search engines at volume can break their terms of service;
prefer an official search API, a licensed tool, or reading results by hand.

**Getting the data:** a web search tool or search API if connected, or the person pastes
what they see in a private window set to the right country.

## An optional paid SEO tool

If the person has one connected (an MCP server or API for a keyword or backlink tool), it
can supply exact volumes, keyword difficulty, competitor keywords and ranking history. Use
it to fill the same fields with higher confidence. Do not change the method, and do not
treat its absence as a failure.

## Triangulating

1. **Start broad** with Keyword Planner ranges (or autocomplete and "People also ask" if
   there is no Planner access) to sort candidates into tiers.
2. **Overwrite with Search Console** for any term it covers.
3. **Check direction with Trends** for the priority candidates. Drop or deprioritise
   declining terms.
4. **Read the results page** for the top candidates to confirm intent and how beatable it
   is.

Record for each term: tier, confidence, and which sources contributed.

## The record for each term

```text
term:        lower case, trimmed
tier:        high | medium | low | unknown
confidence:  exact | observed | range | relative | inferred
intent:      informational | commercial | transactional | navigational
sources:     list of what contributed
notes:       caveats, e.g. "Planner range 1K to 10K", "Trends rising +40%"
```

A paid tool's exact figure maps onto the same tiers.

## When sources are missing

- Continue with whatever is available.
- List every missing source at the top of the output, with what it means. For example:
  "No Search Console: cannot see current rankings, so coverage is estimated from the
  sitemap."
- Only stop if there is no source at all, and even then offer a clearly-labelled list
  built from the person's knowledge of customer questions.
