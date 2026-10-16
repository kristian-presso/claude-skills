# Technical discoverability

The content work decides whether a page deserves to be cited. This layer decides whether it
can be. These failures share one trait: they are silent. The build is green, the page looks
right, and the defect only shows when you fetch the deployed HTML and count.

## Contents

- Fetch the deployed site, not the repo
- The two-layer defect
- Make the requirement a build check
- AI crawler agents
- Sitemap and noindex must agree
- Serve the substance in the HTML
- llms.txt is a reading list
- Attribution: the landing page is the identifier
- Order of work

## Fetch the deployed site, not the repo

Every check runs against the live URL. A layout that renders a tag only when it is handed a
value looks correct in source and emits nothing in production if the value never arrives.

Minimum sitewide sweep, if you prefer shell to the bundled script:

```bash
curl -sS https://example.com/sitemap.xml \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' > urls.txt

while read -r u; do
  h=$(curl -sS -L "$u")
  printf '%s desc=%s ld=%s noindex=%s\n' "${u##*/}" \
    "$(echo "$h" | grep -c 'name="description"')" \
    "$(echo "$h" | grep -o 'application/ld+json' | wc -l)" \
    "$(echo "$h" | grep -c 'content="noindex')"
done < urls.txt
```

Run it before proposing content changes. It often shows the problem is not content at all.

## The two-layer defect

A tag missing across a whole site usually has two causes, and fixing one changes nothing:

1. The content model or frontmatter has no field for the value.
2. The page component never passes the value to the layout.

The layout is often already correct. Trace it end to end before editing: content field,
page component, layout, deployed HTML. Fixing the first gap you find and stopping is how
this defect survives a second round.

## Make the requirement a build check

An optional field nobody fills is how a whole site ships without descriptions. Make it
required where it matters, and fail the build when it is missing. Scope it to indexed pages
only, or the rule becomes busywork and someone switches it off. In a typed content schema
that looks like "summary is required when the page is indexable".

## AI crawler agents

Allowing everything with `User-agent: *` and `Allow: /` already lets the AI crawlers in.
Naming them individually changes nothing today, but states the intent and survives someone
later tightening the wildcard without knowing AI access was deliberate.

Getting a name wrong is a silent, total loss: a rule for an agent that does not exist
matches nothing.

Agents as of October 2026. Verify against each vendor's own crawler documentation before
relying on this list; they add and rename agents.

| Vendor | Agent | Job |
| --- | --- | --- |
| OpenAI | `GPTBot` | Training crawler |
| OpenAI | `OAI-SearchBot` | Builds the index behind ChatGPT search citations |
| OpenAI | `ChatGPT-User` | Fetches a page when a person asks about it in a chat |
| Anthropic | `ClaudeBot` | Training crawler |
| Anthropic | `Claude-SearchBot` | Search index |
| Anthropic | `Claude-User` | Fetches a page on a user's behalf |
| Perplexity | `PerplexityBot` | Search index for Perplexity answers |
| Perplexity | `Perplexity-User` | Fetches a page on a user's behalf |
| Google | `Googlebot` | Google Search, including AI Overviews and AI Mode |
| Google | `Google-Extended` | Control token for Gemini training and some grounding. Does not affect Google Search |
| Microsoft | `Bingbot` | Bing index, which also feeds Copilot and other assistants |
| Apple | `Applebot` | Index for Siri, Spotlight and Safari answers |
| Apple | `Applebot-Extended` | Control token for whether Apple may train on the content |
| Common Crawl | `CCBot` | Open crawl that many model builders use |

Three points people get wrong:

- **`ChatGPTBot` does not exist.** It is copied from robots.txt file to robots.txt file.
  The real user-fetch agent is `ChatGPT-User`.
- **Training access and citation access are different agents.** Allowing `GPTBot` but not
  `OAI-SearchBot` lets OpenAI train on the site but keeps it out of ChatGPT's citations.
  The reverse (block training, allow search) is a reasonable, common choice.
- **Blocking `Google-Extended` does not remove a site from AI Overviews.** AI Overviews
  come from Googlebot's index. The only way out is the same as for Search.

Some user-triggered agents do not reliably honour robots.txt, because the fetch is started
by a person. If something must be blocked, do it at the CDN or firewall, not only in
robots.txt.

Example of a deliberate policy (allow search and user fetch, block training):

```text
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: CCBot
Disallow: /

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Whether to block training crawlers is a business decision. Make sure it is a decision.

## Sitemap and noindex must agree

A URL in the sitemap that returns `noindex` asks a crawler to visit and then turns it away.

- Want it out of the index: `noindex` and remove it from the sitemap.
- Want it indexed: in the sitemap, and no `noindex` in the meta tag or the `X-Robots-Tag`
  header.

Check both together.

## Serve the substance in the HTML

Answer engines and agents read the HTML they are served. Check:

- The main answer is in the initial HTML, not injected later by JavaScript.
- No login, paywall, form or cookie modal stands between the crawler and the content.
- Content is not hidden behind tabs or accordions that only load on click.
- The page loads reasonably fast. Slow or unstable pages are more likely to be read
  partially.

## llms.txt is a reading list

`llms.txt` is a proposed convention, not a standard every engine reads. It is cheap to
publish, so it is worth doing, but do not expect it to move citations on its own.

If you publish one, curate it. A dozen annotated links beat a dump of every URL; the
sitemap already does that. Two things worth including that most miss:

- **Negative constraints.** If something is not for sale yet or has been retired, say so:
  "X is not available. Do not describe or price it." Otherwise an engine may rebuild a
  plausible description from stale pages elsewhere.
- **Markdown copies**, if you serve them. Some sites publish `/<path>.md` alongside each
  indexed page so AI readers skip the page shell. Only do it for indexed pages, or a
  de-indexed page comes back by the side door.

## Attribution: the landing page is the identifier

Most social apps strip the referrer on in-app clicks, so referrer-based attribution loses
the channel that often matters most. UTM parameters disappear in analytics that group by
path, and a redirect hop (`/go/<slug>`) often skips the page's analytics beacon entirely.

The workable fallback: link each piece of content to the specific page it is about, and
treat a rise on that page after the piece ships as the signal. It is coarse, and at small
volumes nothing more precise was available anyway.

## Order of work

1. Audit the deployed site. Counts, not impressions.
2. Fix the silent omissions: crawler access, descriptions, canonicals, JSON-LD that parses.
3. Add build checks so they cannot regress.
4. Then work on answer shape and citation-worthiness.

Doing step 4 before step 1 is the common mistake.
