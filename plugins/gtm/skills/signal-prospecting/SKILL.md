---
name: signal-prospecting
description: Finds B2B prospects from public business signals (funding rounds, hiring posts, product launches, leadership changes, tech-stack changes), identifies the right contact at each account, and proposes one specific use case per account with every claim sourced and dated. Use when someone asks to "find prospects", "build a target list", "who should I reach out to", "find companies that just raised", "find accounts hiring for X", "research this list of companies before outreach", "give me a reason to contact them and an opening line", or has a list of accounts and wants a reason to contact each one now.
---

# Signal prospecting

A cold message with a real, recent reason to exist gets several times the replies of a
generic one. This skill turns public business signals into a short list of accounts, the
right person at each, and one specific use case per account, ready to hand to the
`outbound-sequences` skill.

The output is a small list you trust, not a big list you hope about. Ten well-researched
accounts beat two hundred names from an export.

## When to use

- Building a first target list for a new offer.
- Turning a generic list (an export, a conference attendee list, a CRM segment) into
  accounts with a reason to contact them now.
- Weekly or monthly sweeps for fresh triggers in a defined market.

## Ground rules

These apply to every run. Do not relax them because the user is in a hurry.

1. **Every claim about a prospect cites its source and date.** "Raised a Series A" needs
   the link and the date it was announced. No source, no claim. If you inferred
   something, label it as an inference.
2. **Public business information only.** Company announcements, press, job posts, company
   websites, public filings, public professional profiles and posts. Nothing behind a
   login you are not entitled to, no scraping personal data, no guessing at private
   details (home addresses, personal phone numbers, family).
3. **Respect opt-outs.** If the user has a suppression or unsubscribe list, check against
   it first. Anyone who has asked not to be contacted is removed, whatever the signal.
4. **Business contact routes only.** Work email patterns published by the company,
   public professional profiles and the company's own contact routes. Do not hunt for
   personal email addresses.
5. **Stale signals are not signals.** Prefer events from the last 30 days. Anything older
   than 90 days needs a stronger reason to be used.

## Step 1: Define the target and the signals that matter

Get, in a sentence or two each:

- **The offer.** What the user sells and the problem it solves.
- **The ideal account.** Industry, size, geography, and anything that rules an account
  out.
- **The buyer.** The role that feels the problem, and the role that signs.
- **Which signals imply the problem.** Not every signal fits every offer. Ask "what
  would have to be true at a company for them to need this now?" and map it to the
  signal types below.

| Signal | What it often implies | Where it shows up |
| --- | --- | --- |
| Funding round | Budget to spend; pressure to grow headcount and pipeline fast | Company news page, press releases, funding databases, business press |
| Hiring posts | A team being built or a gap being filled; the job ad often names the tools and problems | Company careers page, job boards |
| Product or market launch | New workflows, new customers to support, new regions to serve | Company blog, press, changelog, launch platforms |
| Leadership change | New leaders review vendors and set fresh priorities in their first 90 days | Company announcements, press, public professional profiles |
| Tech-stack change | Migration work, integration needs, a gap the old tool filled | Job ads naming tools, public case studies, vendor customer pages, the company's own engineering blog |
| Expansion | New office, new site or new country: more of every operational problem | Press, careers page locations, company news |
| Public post by the buyer | Stated pain or priority in their own words | Their public posts, talks, podcasts, interviews |

Read `references/signals.md` when choosing signals for an unfamiliar market, or for
search patterns per signal type.

## Step 2: Find accounts with a live signal

**If you have web search or a fetch tool**, search for each chosen signal within the
target market and time window. Search the primary source where possible (the company's
own announcement, the actual job post) rather than a summary of it. Record the URL and
the date for every hit.

**If you do not have web search**, ask the user for one of:

- a list of company names or domains to research by hand, or
- pasted text: job posts, news items, a newsletter, an export.

Then work only from what they give you, and say clearly which claims could not be
checked. Do not wait for the list to do the parts that need no search: recommend the
buyer role (Step 1: the person who feels the problem, and why at this company size) and
the signals to look for, so the user can act on them straight away.

Aim for 10 to 25 candidate accounts. Stop collecting when you have enough to work
properly; more accounts with thinner research is a worse result.

## Step 3: Qualify

Drop any account that:

- fails the ideal-account definition,
- appears on the user's suppression list or is an existing customer,
- only has a signal older than 90 days with nothing fresher, or
- has a signal that does not actually connect to the offer's problem.

A strong, fresh signal does not rescue an account that fails the ideal-account definition
(too big, too small, wrong region). Drop it; do not rank it as a "long shot" above
accounts that fit. Say how many you dropped and why, in one line.

## Step 4: Find the right contact

For each remaining account, identify one primary contact and at most one alternate:

- The person who **feels the problem** is usually a better first contact than the most
  senior person.
- Use the company's own team page, the person named in the announcement, the hiring
  manager named in the job post, or public professional profiles.
- Record the name, role, and where you found them (source and date).
- If you cannot find a named person from public sources, record the role to target and
  leave the name blank. Do not guess.

## Step 5: Propose one use case per account

Write one or two sentences per account that connect the signal to the offer:

> Because [signal, with source and date], they probably now face [specific problem].
> [Offer] helps by [specific outcome].

Fill all three parts for every account, with the source and date written into the
sentence itself. A timing-only signal (a new executive, a funding round) still needs the
specific problem the offer solves for that person, for example a new finance lead and the
labour-cost line a rota tool cuts. If you cannot name that problem, say the signal gives
timing but no reason, and rank the account lower.

Be concrete. "They could benefit from better tooling" is not a use case. "They are
hiring three support agents in Manila (careers page, 02/10/2026), so they are about to
run support across two time zones; the offer gives them shared queues and hand-over
notes" is.

Label any inference as an inference. The prospect will notice a wrong assumption
immediately, and it costs more than no assumption.

## Step 6: Hand off

Produce the research table (template below) and recommend:

- the top 5 to 10 accounts by strength and freshness of signal,
- the opening line for each, built from the signal, and
- that the user moves to the `outbound-sequences` skill to design the sequence and run
  the deliverability pre-flight.

## Research template

Use this per account. Read `references/research-template.md` for a filled example and a
compact table version for longer lists.

```markdown
### <Company name> (<website>)

- **Fit:** <industry, size, location> - <why it matches the ideal account>
- **Signal:** <what happened> - Source: <URL> (<date published>)
- **Further evidence:** <optional second signal> - Source: <URL> (<date>)
- **Contact:** <name>, <role> - Source: <URL> (<date seen>)
- **Alternate:** <name or role> - Source: <URL> (<date seen>)
- **Use case:** <signal -> problem -> how the offer helps, one or two sentences>
- **Inferences:** <anything assumed rather than sourced>
- **Opening line:** <one sentence, built from the signal>
- **Freshness:** <days since signal> - **Priority:** high / medium / low
```

## Example

A founder sells an onboarding-automation tool to B2B software companies with 20 to 200
staff in the UK.

- **Signals chosen:** Series A or B in the last 60 days (headcount growth means more new
  joiners), and job posts for a first "People Operations" hire (the problem is about to
  get an owner).
- **Search:** 14 candidate accounts found; 5 dropped (2 too large, 1 existing customer,
  2 signals over 90 days old).
- **One entry:** a payments start-up announced a Series A on its blog on 24/09/2026 and
  posted a People Operations Manager role on 01/10/2026. Contact: the COO, named in the
  funding post. Use case: they plan to double headcount and have no one owning
  onboarding yet; the tool gives the new hire a working process on day one. Opening line:
  "Congratulations on the Series A - saw you're bringing in your first People Ops hire
  too."

## Configuration

- **Search access:** whether a web search or fetch tool is available. Without one, the
  skill works from lists and pasted text the user provides.
- **Suppression list:** where the user keeps opt-outs and existing customers, so they are
  removed before research starts.
