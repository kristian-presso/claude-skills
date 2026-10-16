# Clustering and gap analysis

Two steps that turn a flat keyword list into a content plan:

1. **Clustering**: group terms so each group maps to exactly one page.
2. **Gap analysis**: find which groups the site does not cover, or covers badly.

## Clustering

The goal is to stop two pages on the same site competing for the same search
(cannibalisation). One cluster, one page.

### First pass: shared head term

The head term is the core noun phrase: "email marketing" in "best email marketing tools for
small business".

1. Group terms sharing the same head term.
2. Merge near-synonyms if their results overlap (second pass below).
3. Split a group if its terms have different intent. "Email marketing guide" and "email
   marketing software" share a head term but need different pages.

Fast and cheap, but it misgroups terms that sound alike and mean different things.

### Second pass: results overlap

If two terms return many of the same top-ranking pages, the search engine treats them as
one need, and one page can rank for both.

1. Collect the top ten organic URLs for each term.
2. Compute overlap as shared URLs divided by all distinct URLs across both (Jaccard).
3. If overlap is 0.4 or more, put the terms in the same cluster.
4. Apply it transitively: if A goes with B and B with C, all three are one cluster.

`scripts/serp_cluster.py` does this from a `keyword<TAB>url` file.

0.4 is a starting point. Raise it to 0.5 if clusters come out too broad; lower it to 0.3 in
a thin niche where results naturally vary.

### Use both

Head-term grouping first to build candidate clusters and limit how many results pages you
need. Then results overlap on the boundaries that matter, to split and merge correctly.

### Cluster record

- `cluster`: a short slug from the head term, e.g. `charity-crm`.
- `terms`: the keywords in it.
- `main_term`: the one the page will be built around (usually highest demand).
- `intent`: the majority intent.
- `demand`: the tier.
- `target_page`: the URL that owns it, existing or planned.

## Gap analysis

### Demand set

Every cluster from the research.

### Coverage set

From Search Console: every query with impressions, clustered the same way, each tagged with
the page that gets most of its impressions.

Without Search Console, approximate it: check the sitemap and run a `site:example.com topic`
search for each cluster. Mark the result as lower confidence.

### Status per cluster

| Status | Meaning | Usual action |
| --- | --- | --- |
| covered | Average position 1 to 5 | Maintain. Refresh dates and facts. |
| under-ranked | Average position 6 to 20 | Improve or merge the existing page. Often the best return. |
| weak | Position over 20, or very few impressions | Decide: rebuild the page or start fresh. |
| gap | No page, no impressions | New page, if demand and intent justify it. |

### Prioritising

1. Demand tier.
2. Intent that converts for this business.
3. How beatable the top results are.
4. For under-ranked clusters: is the content weak (fix the content) or is the content good
   and the site lacks authority (a links and mentions problem, not a writing problem)?

## Cannibalisation

Once a cluster has a target page, no other page targets it.

- Two existing pages ranking for the same cluster: merge them into the stronger one and
  permanently redirect (301) the weaker.
- A new page planned for a cluster that already has one: improve the existing page instead.
