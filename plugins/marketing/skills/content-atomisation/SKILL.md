---
name: content-atomisation
description: Turns one long piece of content (a blog post, guide, report, talk transcript or podcast) into a sequenced, channel-by-channel plan of standalone derivative pieces, each with one claim, one link back and one call to action, then drafts them on request. Use when someone says "repurpose this", "atomise this post", "turn this into social posts", "content plan from this article", "break this into channel pieces", "derivative content", or "what can I get out of this one piece".
---

# Content atomisation

One good long piece can feed weeks of channels. Most repurposing fails in one of two ways:
the same point reworded six times, or fragments that only make sense if you read the
original. This skill avoids both by planning first and drafting second.

The output is an **atomisation map**: one row per piece, each with a distinct angle, one
core claim, one link and one call to action, in a publish order that never sends anyone to
a page that is not live yet.

## The four rules

1. **Standalone.** Every derivative teaches one thing and makes sense on its own. No "part
   1 of 3", no "as I said last week", no teaser that holds back the payoff.
2. **Distinct angles, not paraphrases.** Each piece answers a different reader question.
   If two rows say the same thing in different words, cut one.
3. **No padding.** If the source has one real point, the map has one derivative. Say so.
   A 600-word opinion piece might support one or two; a 3,000-word guide might support
   eight.
4. **Hub first.** The long-form piece (the hub) publishes before any derivative, and every
   derivative links back to it or to a page that links to it.

## Step 1: read the source

Accept pasted text, a file, or a URL (fetch it). Extract and show the person:

- **Title**
- **Core thesis** in one sentence
- **Hub URL**, or a placeholder slug if it is not live yet
- **Approximate length**
- **The distinct points**: every separate claim, number, example, story, framework or
  objection the piece contains. This list is the raw material. Number them.

Then ask one question if you need to: **which channels do they actually use?** Do not plan
for channels they do not run. If they do not say, default to the hub plus LinkedIn and
email.

## Step 2: build the map

One row per piece. Read `references/channel-formats.md` for what each channel needs and
`references/linking-and-ctas.md` for link and CTA rules.

| Field | Rule |
| --- | --- |
| `sequence` | 1 is the hub. Derivatives start at 2, in publish order. |
| `lag_days` | Days after the hub publishes. Hub is 0. Derivatives 1 or more, never going backwards. |
| `channel` | Where it goes: linkedin, x, email, newsletter, short-video, carousel, podcast, blog. |
| `format` | single post, thread, teaser, talking head, 8-slide carousel, and so on. |
| `angle` | The reader question this piece answers. Must differ from every other row. |
| `core_claim` | One sentence. The single claim this piece makes. |
| `link_target` | The one URL this piece sends people to: the hub, or a related page that links to the hub. |
| `cta` | One specific action, aligned with the link. |

Match each distinct point from Step 1 to the channel where it works best: a surprising
number suits a short post, a step-by-step suits a carousel or email, a story suits video or
audio. Not every point needs a piece.

Default pacing, from `references/sequencing.md`: social 1 day after the hub, email 3 to 5,
short video 5 to 7, carousel 7 to 10, audio 14 to 21, and no more than one piece per
channel per week from the same source.

## Step 3: validate the map

If you can run scripts, write the map as TSV (fields in the order `sequence`, `lag_days`,
`channel`, `format`, `core_claim`, `link_target`, `cta`) and run:

```bash
bash scripts/validate_map.sh map.tsv
```

It checks: one hub at day 0, at least one derivative, no empty fields, sequences 1..N with
no gaps, no duplicate claims, and no derivative scheduled before the one before it. Works
with the stock bash and awk on macOS and Linux.

If you cannot run scripts, check the same seven things by reading the table. Then do the
check the script cannot: **read the angles side by side and cut any that are paraphrases.**

## Step 4: present the plan

```markdown
# Atomisation plan: <title>

**Hub:** <url> | **Thesis:** <one sentence> | **Pieces:** <N> (1 hub + <N-1> derivatives)

| # | Day | Channel | Format | Angle | Core claim | Link | CTA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | blog | guide | - | <thesis> | <hub> | N/A |
| 2 | 1 | linkedin | single post | ... | ... | <hub> | ... |

**Left out:** <points from the source not used, and why>
**Before publishing:** hub must be live on day 0; check every link resolves.
```

If the person gives a start date, add actual dates. If not, keep day offsets.

## Step 5: draft (when asked)

Draft the pieces the person wants, one per section, each labelled with its row number.
For every draft:

- Open with the core claim or the most specific detail, not a preamble.
- Stay within the channel's norms in `references/channel-formats.md`.
- Use the source's facts only. Never add a statistic, quote or example that is not in the
  source; if a piece needs one, mark `[ADD: ...]`.
- End with the row's CTA. One.
- Keep the person's voice. If they have the `linkedin-post` skill from this plugin, use it
  for LinkedIn rows so the voice is learned from their own posts.

For visual formats (carousel, video), draft the slide text or script and a one-line visual
note per slide or scene.

## Example

> **User:** Repurpose this 2,200-word post on why small venues lose bookings to slow email
> replies. We use LinkedIn, a monthly newsletter and Instagram.
>
> **Claude:** Thesis: venues that reply to enquiries within an hour win roughly twice as
> many bookings as those replying next day. I found five distinct points; two are strong
> enough for their own pieces, one suits a carousel, two I would leave out because they
> repeat the thesis. Plan:
>
> | # | Day | Channel | Angle | Core claim |
> | --- | --- | --- | --- | --- |
> | 1 | 0 | blog | - | Reply speed decides most venue bookings |
> | 2 | 1 | linkedin | "Does reply time really matter?" | The one-hour reply figure from the post's own data |
> | 3 | 7 | instagram carousel | "How do I reply faster without hiring?" | Four templates that cover most enquiries |
> | 4 | 12 | newsletter | "What do fast venues do differently?" | One venue's before and after |
>
> Want me to draft rows 2 to 4?

## Configuration

Two things vary per person:

- **Channels and cadence.** Which channels they run and how often, so the plan fits their
  real schedule.
- **Link targets.** Their hub URL and any related pages a derivative could point to
  instead. If they have an internal-linking map, use it; otherwise link to the hub.
