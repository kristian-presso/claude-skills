# Search intent

Why someone searches decides what page can win. Classify intent before committing to a
cluster, and confirm the business can build the right page type. A strong article aimed at
a transactional query ranks badly or converts badly, usually both.

## The four classes

### Informational

The person wants to learn or find an answer. No purchase is close.

Tokens: how, what, why, when, where, who, which, is, are, does, can, should, guide,
tutorial, tips, ideas, examples, definition, meaning, difference, explained, learn,
overview, introduction, beginner, basics, checklist, template.

Results page signs: featured snippets, "People also ask", AI Overviews, reference sites.

Build: article, guide, how-to, FAQ, glossary entry.

### Commercial

The person is researching before a purchase.

Tokens: best, top, review, reviews, comparison, compare, vs, versus, alternative,
alternatives, recommended, rated, ranking, roundup, pros and cons, worth it.

Results page signs: listicles, comparison tables, review sites and software directories.

Build: comparison page, "best X for Y", alternatives page, review page.

### Transactional

The person wants to act: buy, book, sign up, get a quote.

Tokens: buy, purchase, order, download, subscribe, book, booking, register, hire, quote,
price, pricing, cost, cheap, cheapest, discount, deal, coupon, offer, sale, affordable,
demo, checkout, near me, for sale, low cost, how much, free trial, sign up.

Results page signs: product and pricing pages, shopping results, ads above the fold, a local
map pack.

Build: product page, pricing page, landing page, booking or sign-up page, local service
page.

### Navigational

The person wants a specific site.

Tokens: a brand or domain name, login, sign in, account, dashboard.

Build: usually nothing beyond being the brand. The exception: "[competitor] alternative" or
"[competitor] vs [you]" is commercial, and worth a comparison page.

## Precedence

When several classes match, the bundled classifier picks in this order: navigational (your
own brand terms) > transactional > commercial > informational, and defaults to
informational when nothing matches.

"Best price for X" matches both commercial and transactional; transactional wins, because a
page with a clear price and a clear action serves both.

## Where tokens mislead

- **"vs" and "review"** can be informational when comparing concepts ("react vs vue") and
  commercial when comparing products ("best payroll software review").
- **"how much"** is usually transactional ("how much does a bookkeeper cost") but can be
  informational ("how much VAT do I pay").
- **"free"** is ambiguous: "free invoice template" is informational, "free trial" is
  transactional.
- **Local terms**: "near me" and a place name usually mean transactional local intent.

When in doubt, look at the results page. Whatever page type dominates the top ten is the
intent the search engine has settled on.

## Why intent gates the plan

- Transactional and commercial terms convert; informational terms build awareness.
- An informational cluster dominated by large reference sites is hard to win; one dominated
  by forum threads is often easy.
- Commercial clusters reward comparison content that takes time to earn trust.
- Your own brand terms are won by being the brand; do not spend content effort there.
