---
name: seo-schema-gate
description: Checks that a page or draft ships correct JSON-LD structured data and complete SEO meta before it publishes, and audits the live URL after it does. Use when drafting, reviewing or publishing any public web page, and when writing or checking schema.org markup, meta title and description, Open Graph, Twitter Card or canonical URLs. Two modes - write the frontmatter and JSON-LD a draft needs, or validate a draft file, a built HTML file or a live URL against the checklist.
---

# SEO and schema gate

A page with broken structured data looks completely fine. That is the whole problem: every
local check passes, the page renders, and the failure only exists in someone else's parser.

This skill is the check that runs before publishing, and again against the live URL after.

## Two modes

**Write.** Given a draft or brief, produce the SEO frontmatter (title, meta description,
slug, dates, social image, author) and, when the content genuinely warrants it, the raw
`FAQPage` or `HowTo` JSON-LD block.

**Validate.** Given a draft file, check its frontmatter and content shape. Given a built
HTML file or a live URL, check the rendered `<head>` and every JSON-LD block:

```bash
python3 scripts/check_head.py https://example.com/blog/post
python3 scripts/check_head.py dist/blog/post/index.html
```

Standard library only. Prints PASS, WARN or FAIL per item and exits non-zero on any FAIL, so
it can sit in CI. If you cannot run scripts, fetch the page and apply the checklist by
reading; the parse step below is the one you must not skip.

## The checklist

### Meta

- **One `<title>`,** 50 to 60 characters, main term near the front. Longer gets truncated
  in results.
- **Meta description,** 150 to 160 characters, written as a **standalone sentence**. Never
  a truncation of the opening paragraph. Count it before you write it into the file rather
  than trimming afterwards.
- **One self-referencing canonical,** absolute, with the host you actually publish on.
- **Open Graph:** `og:type`, `og:url`, `og:title`, `og:description`, `og:image`. The image
  URL must be **absolute**; a relative one silently fails on every platform that fetches
  it. 1200 by 630 is the safe size.
- **Twitter Card:** `summary_large_image`, with title, description and image.
- **No `noindex`** on a page that is meant to rank, in the meta tag or the `X-Robots-Tag`
  header.
- **A visible modified date** that reflects the content, generated from the entry rather
  than hardcoded.

### Structured data

- Every `<script type="application/ld+json">` block **parses as JSON**. Check it, do not
  eyeball it. A trailing comma takes the whole block out and nothing on the page changes.
- The `@type` matches the surface (table below).
- **No duplicate singletons.** Two top-level `Organization` or two `WebSite` nodes on one
  page, usually one from the theme and one from your own code. Nested references (an
  article's `publisher`) are fine.
- **Stable `@id`s** on the main nodes (for example `https://example.com/#org`,
  `<page-url>#article`) so nodes can reference each other instead of repeating.
- `datePublished` and `dateModified` are generated from the entry, never hardcoded.
- An `author` node with a real name, ideally a `Person` with a `url` to a profile page.
- A `FAQPage` or `HowTo` block only when the content genuinely is questions and answers or
  step by step, and only for what is visible on the page.

### Which type for which surface

| Surface | Main type | Notes |
| --- | --- | --- |
| Blog post or article | `BlogPosting` or `Article` | With `author` (`Person`), `publisher` (`Organization` by `@id`), both dates |
| Technical guide | `TechArticle` | Same fields as `Article` |
| Ordinary page (about, contact) | `WebPage` | Plus `BreadcrumbList` if the site has hierarchy |
| Product or service page | `Product` or `Service` | Only include price if it is on the page and kept current |
| Event page | `Event` | Dates, location, offers if tickets are sold |
| Sitewide, once | `Organization`, `WebSite` | One of each, usually in the layout |
| A social post | None | Not your page, nothing to mark up |

### Content shape, for generative and answer engines

Structured data tells a machine what the page is. The content still has to be quotable:

- The first 40 to 60 words after the title answer the title's question directly. That
  opening is the chunk a model extracts.
- At least two headings phrased as real questions someone would type.
- Every section quotable on its own. No "as discussed above" or "see the next section",
  because retrieval returns passages, not pages.
- Any X-versus-Y comparison rendered as a table. Tables get extracted close to verbatim.
- Statistics carry a named source and a date.
- Nothing important behind a form. Crawlers cannot fill forms.

The `ai-search-visibility` skill in this plugin goes deeper on this half.

## Write mode: frontmatter

Most frameworks generate JSON-LD at build time from frontmatter, so the real job on a draft
is making sure the **frontmatter feeding that layer** is complete. Match the key names the
site's own content schema expects; the SEO label and the field name often differ (for
example `meta_description` rather than `description`).

A generic shape:

```yaml
title: "How to price a small conference: a worked example"
meta_title: "How to price a small conference (worked example)"
meta_description: "A worked example of pricing a 150-person conference: fixed costs, break-even ticket price, early-bird tiers and the margin to aim for."
slug: "price-a-small-conference"
published_at: "2026-10-01"
updated_at: "2026-10-10"
author: "Sam Lee"
og_image: "https://example.com/og/price-a-small-conference.png"
```

**Quote every date.** Strict YAML loaders turn a bare `2026-10-01` into a date object, and
some content validators reject it outright, so the build fails on a field that looks fine.

Hand-written JSON-LD should be limited to the `FAQPage` or `HowTo` block an individual entry
needs, carried in its own frontmatter field. Example:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much should I charge per ticket?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Start from fixed costs divided by expected attendance, then add your target margin."
      }
    }
  ]
}
```

Run it through `python3 -m json.tool` before saving.

## Validating a live URL

1. Fetch the page (the script, `curl`, or any fetch tool).
2. Check the `<head>` against the meta list above.
3. Extract every JSON-LD block and **parse each one**. Without the script:

   ```bash
   curl -s "$URL" | python3 -c "
   import sys, re, json
   h = sys.stdin.read()
   for b in re.findall(r'application/ld\+json[^>]*>(.*?)</script>', h, re.S):
       d = json.loads(b)                      # raises on malformed JSON
       print('VALID', d.get('@type') or [n.get('@type') for n in d.get('@graph', [])])
   "
   ```

4. Report pass or fail per item.

For the authoritative check, run the URL through Google's Rich Results Test
(search.google.com/test/rich-results) and the Schema.org validator (validator.schema.org).
Your parse proves the JSON is well-formed; theirs proves the vocabulary is right.

## Verify the delivery, not just the artefact

A static build can write the right bytes to disk and still serve them wrongly. Response
headers set in a route handler are commonly dropped when the page is prerendered, so the
host types the file from its extension instead.

So check the served response, not only the build output:

```bash
curl -s -o /dev/null -w '%{http_code} %{content_type}\n' "$URL"
```

And when re-checking after a fix, use the **clean URL**. A cache-busting query string is a
different cache key and can return a stale copy of the old object while the real URL is
already correct, which reads exactly like the fix having failed. Equally, a CDN may serve
the old version of the clean URL for a while; purge it or wait before concluding the fix
did not work.

## Common mistakes

- Marking up content that is not visible on the page. Schema mirrors what a user sees.
- Truncating the body for the meta description.
- Two singleton nodes from theme plus custom code.
- A relative social image or canonical URL.
- Hardcoded dates that never move.
- Unquoted dates in YAML frontmatter.
- Expecting FAQ rich results. Google restricted them in 2023 to a small set of
  authoritative sites; the markup still describes the page, but do not promise the visual
  result. Verify current eligibility in Google Search Central's structured data
  documentation.
- Adding schema for a surface you do not own, like a social post. There is no page, so
  there is nothing to mark up.

## Configuration

**Where schema is composed** varies by project. Find it once and record it next to this
skill: usually a layout or SEO component that reads frontmatter at build time. On a draft,
the job is then making sure that frontmatter is complete, using the field names that
project's content schema expects.
