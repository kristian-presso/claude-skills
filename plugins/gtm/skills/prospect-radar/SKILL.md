---
name: prospect-radar
description: A standing prospecting radar for B2B sellers. Turns who you sell to into tested news, hiring and competitor-change feeds (Google News search feeds, job-board searches, optional Google Alerts), then on each run reads them, pulls out new companies with a reason to talk this week, scores fit, finds the right person and drafts first touches after pre-send checks. Use when someone says "find me new companies to contact", "set up my prospecting feeds", "build me Google Alerts for prospects", "run my radar", "who's new this week", or wants prospecting on a daily or weekly schedule.
---

# Prospect radar

`signal-prospecting` researches a market once. This skill keeps watching it. It sets up
feeds that surface new companies with a reason to talk, then each run turns the newest
items into a short, sourced list and drafts.

Everything lives in one folder (default `./prospect-radar/` in the working folder):
`feeds.md`, `prospects/_seen.csv`, one `prospects/<company>.md` per keeper, and
`drafts/`.

## Ground rules

1. Every prospect needs a dated, linked reason. A company name in a feed is not a reason.
2. Public business information only, unless the user has connected their own CRM or data
   tools. Never scrape sites that forbid it.
3. Never guess an email address. Never send anything; drafts are for the user.
4. Run the pre-send checks before any draft (`../pre-send-check/references/checks.md`,
   or the `pre-send-check` skill).

## Part 1: Build the feeds (first run, or "tune my feeds")

1. Get, one question at a time and only if not already known: industries, regions and
   languages, company size, buying roles and the job titles they hire, and competitor or
   incumbent tools. If `gtm-motion.md` exists, read it instead of asking.
2. Build feeds using `references/prospect-sources.md`: one Google News search feed per
   industry, region and trigger (funding, new digital product, new leader in the buying
   team, expansion, competitor change), plus job-board searches for the buying roles.
   Keep each query narrow. Aim for 10 to 20 feeds.
3. Test every feed with `curl -sL -A "Mozilla/5.0" "<url>"` (or a fetch tool). Keep it if
   it returns recent items naming companies in the target market; rewrite or drop it if
   not. Show a two-line sample from each.
4. Save `feeds.md` as a table: name, trigger, query in plain words, URL, last tested, hits.
5. Offer to walk the user through Google Alerts for anything personal (a competitor, a
   key account) and add the RSS links they paste.

## Part 2: Each run

1. **Harvest.** Read every feed's items from the last three days (seven on a weekly
   schedule). Pull out the company each item is about. Skip companies seen in the last 30
   days (`prospects/_seen.csv`). Aim for 15 to 30 candidates.
2. **Qualify.** Drop disqualified, out-of-territory and existing-customer companies. If a
   CRM is connected, skip accounts owned by someone else and note unowned ones; never
   change ownership. Record every candidate in `_seen.csv` with the outcome.
3. **Enrich the keepers.** News and hiring from the last 90 days; the tools their website
   loads (`references/tech-fingerprints.md`); the person closest to the problem and one
   alternate, with sources.
4. **Score and pick** the top five by fit, freshness of the reason, and whether there is a
   named person to contact.
5. **Check.** Run the pre-send checks on each pick. Drop or rewrite as they say.
6. **Draft.** For each pick: why now (sourced), the angle, who, the checks, and a first
   touch with one specific observation, one hypothesis and one low-effort ask. Save to
   `drafts/`.
7. **Report.** One line per pick, plus which feeds produced keepers.

## Scheduling

To run it every weekday morning, create a scheduled task that runs this skill in the
folder (in Claude Code Desktop: Routines, New routine, Local). Weekly works too; widen the
harvest window to seven days.

## Example

A founder sells a returns-management tool to mid-size online retailers in the UK and
Germany. The radar builds 14 feeds: funding and new-leader feeds per country, "launches
app" feeds for retail, hiring searches for "ecommerce operations" roles, and a
competitor-change search for two incumbent tools. Monday's run reads 212 items, finds 23
companies, keeps 7, and drafts 4 after one is dropped by the checks because the founder
emailed them last week.
