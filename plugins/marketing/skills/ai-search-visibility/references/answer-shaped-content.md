# Answer-shaped content

Answer engine optimisation (AEO) is writing so a model can lift a passage and use it as an
answer without needing the rest of the page. Every pattern here also helps human readers.
The difference is that the reader you are writing for may see one 150-word passage, out of
order, and nothing else.

## Contents

- Answer first
- Headings that match real questions
- Self-contained sections
- Explicit definitions
- Comparison tables
- Lists
- Semantic HTML
- Structured data as a reading aid
- Before and after: a full section

## Answer first

Put the answer to a heading's question in the first one or two sentences under it. Then
support it. Do not open with history, context or caveats.

This is the highest-value change. Retrieval systems tend to take the opening of a section
as the candidate answer to the question the heading implies.

Weak:

> Software pricing has been debated for years. Vendors have tried many approaches. Some
> charge per seat, others a flat fee. In general the industry has settled on per-seat.

Strong:

> Project management tools typically charge £8 to £15 per user per month on their standard
> plans (as of 2026). The range reflects storage limits and whether automation is included.

The strong version can be quoted as it stands. The weak one makes the model build the
answer itself.

For the page as a whole: the first 40 to 60 words after the title should answer the
title's question.

## Headings that match real questions

Write headings in the words people type or say. "How much does venue hire cost in Leeds?"
matches a query. "Venue hire: the ultimate guide" does not.

A heading does not need a question mark to work. "How team pricing works" and "How does
team pricing work?" are both fine. "Team pricing overview" is not.

Aim for at least two question-style headings on any page meant to be found. Pull the
wording from real sources: search suggestions, "People also ask" boxes, sales call notes,
support tickets.

## Self-contained sections

Each section must make sense if it is the only thing read.

- Define acronyms and key terms again in each section where they matter.
- Restate a figure rather than pointing at a table three sections up.
- No "as mentioned above", "see below" or pronouns whose subject sits in another section.
- Write a first sentence that could stand alone as the section's summary.

The unit to test is a heading plus the paragraphs directly under it.

## Explicit definitions

Models looking for a definition pick sentences of the form "X is Y".

Weak: "Progressive web apps are often installed on the home screen and work without an
app store."

Strong: "A progressive web app (PWA) is a website that can be installed on a phone's home
screen and work offline, without an app store download."

Define every term central to the topic that someone might ask about directly.

## Comparison tables

For any "X vs Y", "difference between" or "best X for Y" content, use a table:

- A clear header row naming what is compared.
- The things being compared as row or column labels, not buried in prose.
- Short, factual cells. No paragraphs inside cells.
- A heading above it that matches the comparison question.
- No merged cells and no abbreviations explained only in surrounding text.

Engines often lift well-formed tables almost verbatim.

## Lists

Numbered lists for steps that must happen in order. Bullets for parallel items. Each item
should be a complete thought. If one item needs three sentences and the rest need one,
restructure.

## Semantic HTML

- One H1 per page, matching the page's main topic.
- H2 for main sections, H3 inside them. Do not skip levels.
- Headings for structure, not for making text bigger.
- Short paragraphs. A wall of text gives no signal about where the answer is.

## Structured data as a reading aid

JSON-LD tells crawlers what a page is without parsing prose. It is not a ranking trick.
Useful types:

- `Article` or `BlogPosting` with `author`, `datePublished`, `dateModified`.
- `FAQPage` for genuine question and answer sections. Google narrowed FAQ rich results in
  2023, so do not expect the visual result, but the markup still describes the content.
- `HowTo` for genuine step-by-step content.
- `Product` or `Service` for what you sell.
- `Organization` once, sitewide, with consistent name, logo and profiles.
- `BreadcrumbList` for site structure.

Only mark up what is visible on the page. Use JSON-LD rather than Microdata. The
`seo-schema-gate` skill in this plugin checks it properly.

## Before and after: a full section

Before:

> **Our approach to onboarding**
>
> We know getting started can feel daunting. That's why we've built a process that puts
> you first. As mentioned on our pricing page, every plan includes support. Our team will
> walk you through everything.

After:

> **How long does onboarding take?**
>
> Onboarding takes about two working days for most teams of under 20 people: one call to
> import your data, and one to train the team. Every plan includes both calls at no extra
> cost. Larger teams usually need a third session for admin settings.

What changed: question heading, answer in the first sentence, a specific number, the
pricing fact restated instead of pointed at, no filler.
