# Prospect sources

Where new companies come from. The `prospect-radar` skill turns your ideal customer
profile into the feeds below and saves them in `feeds.md`, then reads them on each run.

## 1. Google News search feeds (no setup, works straight away)

Any news search can be read as a feed. Build one per trigger:

```text
https://news.google.com/rss/search?q=<query>&hl=en-GB&gl=GB&ceid=GB:en
```

- URL-encode the query: spaces as `+`, quotes as `%22`, colon as `%3A`.
- Add `when:7d` to keep only the last week.
- Use `-word` to exclude noise and `site:` to restrict to one publisher.
- Match `hl`, `gl` and `ceid` to the territory, for example `de`, `DE`, `DE:de` for
  Germany. Keep all three consistent or results come back empty.
- A feed returns about 100 items at most. Narrow queries beat broad ones.
- Google does not document this format; if a feed returns nothing for a week, rebuild it.

Fetch with `curl -sL -A "Mozilla/5.0" "<url>"` and read the `<item>` titles, links and
dates.

## 2. Trigger queries to build from the ICP

Replace the words in angle brackets with your industries, regions and products.

| Trigger | Example query |
| --- | --- |
| Funding | `"raises" ("Series A" OR "Series B" OR "Series C") <industry> when:7d` |
| New digital product | `"launches" ("app" OR "platform") <industry> <region> when:7d` |
| New leader in the buying team | `("appoints" OR "hires" OR "joins as") ("Chief Product Officer" OR "VP Product" OR "Head of Growth" OR "Chief Digital Officer") when:7d` |
| Expansion | `"expands into" <region> <industry> when:7d` |
| Competitor or incumbent change | `("migrating from" OR "replaced" OR "moved off") <competitor tool> when:30d` |
| Problem in public | `<industry> ("app outage" OR "conversion" OR "churn") when:7d` |

## 3. Hiring signals

Teams hiring for the roles the product serves are often about to buy. Search job boards
through ordinary web search, never by scraping a site that forbids it:

```text
site:boards.greenhouse.io ("product analyst" OR "growth" OR "experimentation") <region>
site:jobs.lever.co ("product analytics" OR "data product manager") <region>
site:jobs.ashbyhq.com ("growth" OR "experimentation") <industry>
```

A job post naming a competitor tool ("experience with [tool]") is also a displacement
signal.

## 4. Google Alerts (optional, for terms you care about personally)

1. Go to google.com/alerts and type the search, for example a competitor's name with
   "migration".
2. Click **Show options**, set **Deliver to** to **RSS feed**, click **Create Alert**.
3. Click the RSS icon next to the alert and copy the link into `feeds.md`.

## 5. Publisher feeds

Funding and startup news publishers usually offer RSS. Add the ones that cover the
territory to `feeds.md`, and check each link returns items before relying on it.

## 6. Connected data tools

If you have them connected, these beat public searching:

| Tool type | Use for |
| --- | --- |
| Intent data (for example 6sense, G2) | companies researching the product's topics this week |
| Contact and company data (for example ZoomInfo, Apollo, Lusha) | firmographics, named contacts, verified email |
| Partner overlap (for example Crossbeam) | prospects a partner already works with: a warm route in |
| Community signals (for example Common Room) | people engaging with the company's community or content |

## Rules

- Every prospect needs a dated, linked reason. A company name in a feed is not a reason
  until the item says something that matters for the product.
- Keep a list of every company already looked at (`prospects/_seen.csv`) so the same one
  is not researched twice in a month.
