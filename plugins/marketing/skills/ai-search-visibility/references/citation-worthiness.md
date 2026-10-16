# Citation-worthiness

When an engine has retrieved five pages that all answer the same question, something
decides whose sentence gets the citation. This file is about winning that comparison.

## Contents

- How answer engines pick sources
- Original data
- Visible authority
- Specific beats general
- Freshness
- Agree on the basics, add something new
- Named entities
- Cite to be cited
- Evidence for this
- What rarely gets cited

## How answer engines pick sources

Most AI answer surfaces work in three stages:

1. **Retrieval.** The engine turns the question into one or more searches and pulls a set
   of candidate pages from a search index or a live crawl. Being in the index and ranking
   reasonably for related queries is the entry ticket.
2. **Grounding.** The model reads the candidates and uses the most answer-like passages as
   context. Content shape matters most here.
3. **Citation.** The model attributes claims to sources. A page can be read and still not
   cited, if another source had the more specific or quotable sentence.

The surfaces differ in emphasis:

| Surface | What it leans on |
| --- | --- |
| Conversational assistants with search (ChatGPT, Claude, Copilot) | Their own or a partner's search index, then the most direct answer passage. Freshness matters for anything time-sensitive. |
| Google AI Overviews and AI Mode | Google's own index. Pages that already rank well are much more likely to be cited, though it is not a guarantee in either direction. |
| Answer engines (Perplexity-style) | Live retrieval, crawlability, freshness and an exact match to the question. A specific page on a small site can beat a general one on a big site. |
| AI agents that browse to complete a task | Fast pages, key facts near the top, no interaction needed, structured data for products and prices. |

Four conditions must all hold for a page to be cited: it is in the index, it addresses the
exact question, its answer is extractable, and the source is trusted enough. Failing any
one removes it.

## Original data

A specific finding from a primary source beats a restatement of someone else's. Two
effects:

- Other writers cite and link to original data, which builds authority.
- Given two passages making the same point, a model prefers the one with a specific,
  attributed number ("a survey of 400 small venues found 62% take bookings by email") over
  the vague one ("most venues still use email").

Original data does not need a research budget. Your own anonymised customer data, an
analysis of a public dataset, or a careful count of something nobody has counted all
qualify.

## Visible authority

Signals a model can read directly:

- **A named author** with a short bio and a link to a real profile, also in `Article`
  structured data.
- **A real organisation behind the site**: an About page, contact details, legal name.
- **Topical focus.** A site that writes consistently about two or three topics is more
  credible on them than one that covers everything thinly.
- **Links from others** on the same topic. The classic SEO signal applies here too.

Google describes this as E-E-A-T (experience, expertise, authoritativeness,
trustworthiness). Treat it as the sum of trust signals, not a checklist.

## Specific beats general

- **Name the number.** "£10 to £12 per user per month" beats "pricing varies".
- **Name the condition.** "On annual billing" beats "depending on your plan".
- **Name the source.** "According to the ONS business survey (2025)" beats "research
  shows".

Accuracy comes first. A specific number that is wrong does more damage than a hedge that is
right.

## Freshness

For anything that changes (prices, features, regulations, platform behaviour), recency
matters. Make it machine-readable:

- `datePublished` and `dateModified` in JSON-LD.
- A visible "last updated" date on the page, ideally in a `<time datetime="...">` element.
- Dates on individual time-sensitive claims ("as of March 2026").

Separate evergreen sections (definitions, how something works) from tactical ones (prices,
comparisons) and review the tactical ones on a schedule.

## Agree on the basics, add something new

When several credible sources agree on a fact, models treat it as reliable. A page that
contradicts the consensus without evidence looks unreliable.

So state the established facts accurately, then add your own contribution on top: a sharper
number, a worked example, a finding nobody else has. If you genuinely disagree with the
common view, back it with data or a primary source. Evidenced disagreement is a citation
opportunity; unsupported disagreement is a trust risk.

## Named entities

- Name people, organisations, products and standards in each section where they matter.
- Use the canonical name, not a nickname, at least on first mention.
- Link claims to their primary source.
- Keep naming consistent across the site so the business is recognised as one entity.

## Cite to be cited

Linking out to credible sources makes a page look like a reliable intermediary rather than
an unsupported opinion. Do not hoard links.

## Evidence for this

The term "generative engine optimisation" comes from Aggarwal et al., "GEO: Generative
Engine Optimization" (2023, arxiv.org/abs/2311.09735, published at KDD 2024). In their
benchmark, adding citations, quotations and statistics to content raised its visibility in
generative answers by up to about 40%. Treat that as evidence for the direction, not a
promise of a figure; engines have changed since.

## What rarely gets cited

- Walls of text with no headings.
- Adjectives instead of numbers.
- Listicles with no original framing.
- Pages not updated in well over a year on a topic that moves.
- Thin, keyword-stuffed pages with no named expert behind them.
