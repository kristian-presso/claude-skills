---
name: gtm-motion
description: Designs a go-to-market motion for any B2B seller from their role, product and buyers - which motion to run, the ideal customer profile, a tiered account list, the buying signals worth watching with weights, the personas, and a weekly routine. Use when someone says "build my GTM motion", "plan my territory", "set up my prospecting", "who should I go after", "help me work my named accounts", "I'm a new AE, where do I start", or wants a repeatable weekly outbound or expansion routine rather than a one-off list.
---

# GTM motion

The strategy layer for selling: who to pursue, when, and in what order, written down so it
can be run every week. It sits above the other skills in this plugin -
`signal-prospecting` finds accounts with a reason to talk, `account-play` plans one account
in depth, and `outbound-sequences` gets the messages delivered.

Works for any role and product: a founder doing their own sales, an enterprise account
executive with a named territory, an account manager growing existing customers, a
consultant selling services.

## What it produces

A single file, `gtm-motion.md`, in the user's working folder (or pasted back if there is no
folder), containing:

1. The motion type and why.
2. The ideal customer profile (ICP), disqualifiers and the fit-scoring rubric.
3. A tiered account list, or the search brief to build one.
4. The signal library with weights tuned to the product.
5. The buying personas and what each cares about.
6. The play shape per tier and the weekly routine.
7. The guardrails: what data may be used, channels allowed, and that nothing is sent
   without the seller's approval.

## Ground rules

1. **Ask about employer data first.** If the seller works for an employer, ask whether
   they may use outside AI tools with customer or pipeline data. If the answer is no or
   unsure, work from public information only and do not ask for CRM exports. See
   `references/seller-guardrails.md`.
2. **Every fact about an account carries a source and date.** No source, no fact.
3. **No invented customers, results or product capabilities.**
4. **Nothing is sent.** This skill plans and drafts; the seller approves and sends.

## Step 1: Intake, one question at a time

Skip anything the user has already said. Get, in this order:

1. **Role and who they sell for** - their own company or an employer.
2. **What they sell** - the product, the problem it solves, and two or three things it is
   genuinely good at. A product page link helps.
3. **Who buys** - three to five best customers or recent wins, or the buyer they believe
   fits if there are none yet.
4. **Motion** - do they choose their accounts, were they given a named list, or are they
   growing existing customers?
5. **Accounts** - for a territory or expansion, the account names.
6. **Channels and tools** - email, social, phone, events; which CRM or tracker.
7. **Employer data** - the question in ground rule 1.

## Step 2: Choose the motion

Use `references/motion-types.md` to map the answers to one of new-logo outbound, named
territory or expansion. Recommend one. A second motion can come after four weeks of the
first.

## Step 3: Write the ICP and score fit

Follow `references/icp-and-tiering.md`: write the ICP from the best customers, add
disqualifiers, and set the fit rubric. If there were no customers to learn from, mark the
ICP as a hypothesis.

## Step 4: Tune the signals

Start from `references/signal-scoring.md`. Raise the weights of the signals that link most
directly to the problem the product solves, and drop any that never apply. Keep the
freshness bands.

## Step 5: Tier the accounts

If accounts were given, research each briefly (website, recent news - use web search if
available), score fit and timing, and place each in a tier. Cap tier 1 at ten. If no
accounts were given and the motion is outbound, write the search brief and hand to
`signal-prospecting`.

## Step 6: Personas, plays and routine

- Name the buying roles for this product and the angle each cares about (the role table
  in `references/icp-and-tiering.md`).
- Set the play shape per tier: bespoke for tier 1 (use `account-play`), light for tier 2.
- Set the weekly routine from `references/operating-rhythm.md`.

## Step 7: Hand back

Show a one-screen summary: the motion and why, the ICP, the top accounts with one line
each, and the first week's plan. Write the full motion to `gtm-motion.md`. Offer the next
step: run a signal sweep now, or build a play for the top account.

## Example

An enterprise account executive at a product analytics company has 30 named accounts.

- **Motion:** named territory - the employer chose the accounts, effort per account is
  hours, and the constraint is getting to the right people.
- **ICP:** consumer or B2B software companies with a product team of 20 or more, a data
  warehouse in place and a growth or experimentation function. Disqualifier: no in-house
  product team.
- **Signals weighted up:** a new head of product or growth (3), job posts for product
  analysts or experimentation roles (3), a warehouse or data-stack change (2), a public
  push into self-serve or product-led growth (2).
- **Employer data:** not allowed in outside tools, so the motion runs on public
  information and the account names the AE typed in.
- **Week one:** sweep all 30, tier 1 is six accounts, plays built for the top two.

## Configuration

- **Search access:** web search or fetch makes Step 5 and the weekly sweep far stronger.
  Without it, the skill works from what the user pastes.
- **Working folder:** where `gtm-motion.md` is saved so later runs start from it.
