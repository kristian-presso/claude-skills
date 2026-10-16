---
name: account-play
description: Builds the plan for one target account - a sourced brief, the buying committee with who to contact first, two or three value hypotheses or proposed use cases, a multi-person four-week play, and first-touch drafts per person held for approval. Use when someone says "build a play for [company]", "how do I get into [company]", "who should I contact at [company]", "propose use cases for [company]", "multi-thread this deal", "draft outreach to [company]", or after a signal sweep turns up a hot account.
---

# Account play

The depth half of selling. Takes one account and turns it into a dated plan across several
people, with drafts the seller can approve and send. Pairs with `gtm-motion` (which says
which accounts deserve a play), `signal-prospecting` (which finds the reason to talk) and
`outbound-sequences` (cadence, copy and deliverability).

## What it produces

1. A short account brief with sourced facts and the why-now.
2. A buying-committee map: an entry point plus at least two further roles, each sourced.
3. Two or three value hypotheses or use cases, each tied to a signal and a real product
   capability, with a first small step.
4. The play: threads in order, channel, asset, exit condition and review date.
5. One first-touch draft per thread, in the seller's voice.

## Ground rules

1. **Every fact about the account has a source and date.** Inferences read as inferences.
2. **No invented numbers, customers or capabilities.** A hypothesis states a mechanism;
   numbers come from the buyer or the seller's own verified case studies.
3. **Public business information only**, unless the seller confirms their employer allows
   their own data in outside AI tools.
4. **Nothing is sent, and no one is impersonated.** Drafts are held for the seller.
5. **Never contact several people at one company on the same day.**

## Step 1: Context

If a `gtm-motion.md` exists in the working folder, read it for the product, personas,
signals and the employer-data answer. If not, ask in one question what they sell and to
whom, and whether their employer allows customer data in outside AI tools.

## Step 2: Research the account

With web search or fetch: what they do, size and stage signals, news and hiring from the
last 90 days, the team the product serves, and named people in it. Keep a source URL and
date for every fact. Without search, work from what the seller pastes and say what could
not be checked.

## Step 3: Map the committee

Use `references/buying-committee.md`. Name the roles for this product, fill each from
public sources with name, role, source and confidence that the role is current, and leave
gaps as gaps. Choose the entry point - usually the person closest to the pain, not the
most senior - and the next two threads.

## Step 4: Form two or three hypotheses

Use the shape in `references/value-hypotheses.md`. Tie each to a dated signal and a
capability the seller confirms exists. If they asked for use cases, give each a first
small step (a pilot, a workshop, an audit) and say what would make it a bad fit.

## Step 5: Write the play

Fill the record in `references/play-template.md`: why now, hypotheses, entry point,
threads with timing, one useful asset, an exit condition and a review date. Prefer warm
paths - a mutual connection, an existing customer contact, a shared event - before cold
ones.

## Step 6: Draft the first touches

One draft per thread: one specific observation, one hypothesis, one low-effort ask, and an
opt-out line where the channel and the recipient's country require it. Keep it short. For
email addresses follow `references/contact-data.md` - use one only if it is published or
verified; otherwise draft for a social message or a warm introduction.

## Step 7: Hand back

Show the brief, the map, the hypotheses, the play and the drafts on one page. If a CRM or
tracker is connected and allowed, offer to log the play and contacts; otherwise save it as
`plays/[account].md` in the working folder.

## Example

An AE at a product analytics company, account: a mid-size online retailer.

- **Why now:** a new VP of Product announced on 29/09/2026 (company blog), and two
  experimentation analyst roles posted on 06/10/2026 (careers page).
- **Entry point:** the head of growth, who owns the conversion targets (team page).
  Threads two and three: the new VP of Product (week 2), the data engineering lead
  (week 3).
- **H1:** because they are hiring experimentation analysts, the growth team is likely
  trying to run more tests with fewer engineering hours; self-serve experiment analysis
  could cut the time from test to readout, which they would see as more tests shipped
  per quarter. First step: a one-hour review of their current test backlog.
- **Exit:** a meeting booked, a clear no, or four weeks with no reply.
