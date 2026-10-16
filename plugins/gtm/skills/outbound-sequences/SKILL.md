---
name: outbound-sequences
description: Designs B2B outbound sequences (cadence, channel mix, the message for each touch) and runs a deliverability pre-flight so cold email lands in the inbox without damaging the sending domain. Use when someone asks to "write a cold email sequence", "plan an outbound cadence", "how many follow-ups should I send", "why are my emails going to spam", "set up a domain for cold outreach", "check my SPF DKIM DMARC", or wants to review an existing sequence that is getting no replies.
---

# Outbound sequences

A sequence is a planned series of touches across channels, aimed at starting one
conversation with one fit prospect. This skill covers starting that conversation. What
happens after a reply is a sales process, not a sequence.

Three things decide whether a sequence works, in this order:

1. **Relevance.** The right person, at the right moment, about something real at their
   company. This is the biggest lever by far.
2. **Delivery.** Copy that lands in spam does nothing, and a burned domain takes weeks to
   recover.
3. **Shape.** Enough touches to clear the point where most replies arrive, then stop.

If the user has no list yet, or the list is a generic export with no reason to contact
anyone now, start with the `signal-prospecting` skill and come back here.

## When to use

- Designing a new outbound sequence from scratch.
- Reviewing a sequence that gets opens but no replies, or no opens at all.
- Setting up a new sending domain or inbox for cold outreach.
- Checking a programme against the law in the recipient's country before it starts.

## How to design a sequence

Work through these steps with the user. Ask only for what you do not already have.

### 1. Pin down the target and the reason

Get three things in one or two sentences each:

- **Who.** Role and company type. Narrow beats broad: one or two contacts per account.
- **Why now.** The trigger for each account (a funding round, a hire, a launch). If there
  is no trigger, say so plainly: expect generic reply rates, and consider finding signals
  first.
- **The one ask.** What a "yes" looks like. Usually a short reply showing interest, not a
  booked 30-minute demo.

### 2. Choose the shape

Defaults to start from, then adjust to the audience:

- **8 to 12 touches across all channels**, or **4 to 7 if email only**.
- **Roughly 3 to 4 weeks** in total.
- **Front-load week one** (4 to 5 touches), then widen the gaps.
- **Stop at the end.** Do not run past about 12 touches. Park the contact and recycle them
  later with a new reason.

Senior buyers and enterprise accounts usually need fewer, more considered touches over a
longer window. Small-company founders reply fast or not at all.

Read `references/cadence-and-channels.md` when the user wants the reasoning behind these
numbers, a channel split, or a day-by-day template.

### 3. Mix the channels

Email is the base. Add a phone call and a professional-network touch where the user can
actually do them. Video is an occasional differentiator, not a channel to build on.

A sensible opening: email and a connection request on day 1, a call and voicemail on day
2 or 3, then an email that references the voicemail. Alternate channels after that.

Do not plan a channel the user will not run. A sequence with three skipped calls is worse
than an honest email-only one.

### 4. Write each touch

Every touch must earn its place by adding something new: a different angle, a piece of
proof, a useful resource, or a simpler ask. "Just bumping this" adds nothing.

Rules for the first email:

- **50 to 125 words.** Shorter is usually better.
- **Subject line under 50 characters**, plain, lower case, reads like a note from a
  colleague.
- **Open with them, not you.** One specific, accurate observation they could not receive
  in anyone else's inbox. A merge field with their company name is not personalisation.
- **One ask, low friction.** "Worth a look?" beats "Book 30 minutes on my calendar".
- **No feature lists.** One line of proof, if you have it, is enough.

A shape that works: observation, the problem it usually causes, one line of proof, a soft
question.

Read `references/copywriting.md` when drafting or critiquing the actual words, or when the
user asks for subject lines or follow-up angles.

### 5. Run the deliverability pre-flight

Do this before the first send on any new domain or inbox, and again whenever replies
suddenly drop. Go through the checklist below and mark each item pass, fail or unknown.
Do not let the user start sending with any "fail" in the first section.

### 6. Check the law for where the recipients are

The recipient's country decides which rules apply, not the sender's. Opt-out regimes
(the US) and opt-in regimes (Canada) differ sharply, and the EU and UK sit in between.
Build for the strictest regime the list touches.

Read `references/legal.md` before the first send into any new country. It is a reference
summary, not legal advice, and it says so.

### 7. Agree how it will be judged

Before launch, agree the numbers that matter and the size of test that would change the
plan. Reply rate, positive replies and meetings booked, tracked per step. Not opens.

Read `references/metrics-and-testing.md` for benchmark ranges and how to run an A/B test
that means something.

## Deliverability pre-flight checklist

As of 16/10/2026. Mailbox-provider rules tighten over time: verify at Google's email
sender guidelines (support.google.com/a/answer/81126), Yahoo's sender best practices
(senders.yahooinc.com/best-practices) and Microsoft's Outlook.com high-volume sender
requirements (Microsoft Defender for Office 365 blog, updated 30/04/2025) before relying
on any threshold. Google, Yahoo and Microsoft all apply the bulk rules at about 5,000
messages a day to their users, and Microsoft rejects non-compliant mail outright.

**Must pass before sending (firm requirements):**

- [ ] **Separate sending domain.** Cold email goes from a look-alike domain, never the
      main business domain, so a reputation hit cannot reach invoices and normal mail.
- [ ] **SPF** published on the sending domain.
- [ ] **DKIM** signing on, with a 2048-bit key where the provider allows it (1024-bit is
      the minimum).
- [ ] **DMARC** record present, at least `p=none`, with the From domain aligned to the
      SPF or DKIM domain. Plan to move towards `quarantine` once reports are clean.
- [ ] **SPF and DKIM both pass**, not just one, if any recipients are on Outlook.com,
      Hotmail or Live: Microsoft requires both for bulk senders and rejects failures with
      `550 5.7.515`.
- [ ] **Working unsubscribe** in every message, honoured within two days. For bulk mail,
      add one-click unsubscribe headers (`List-Unsubscribe` and
      `List-Unsubscribe-Post: List-Unsubscribe=One-Click`).
- [ ] **Honest sender identity.** Real name, a reply-to that is read, and a postal
      address where the recipient's law requires one.

**Should pass (practitioner consensus, softer numbers):**

- [ ] **Warm-up done.** New inboxes ramp from about 5 to 10 sends a day over 4 to 6 weeks
      before full cold volume (rule of thumb, not a provider rule).
- [ ] **Per-inbox volume capped** at roughly 10 to 20 cold sends a day, counting warm-up
      traffic. Scale with more inboxes (3 to 5 per domain) and more domains, never by
      pushing one inbox harder.
- [ ] **List verified.** Addresses checked before sending; expected bounce rate low.
- [ ] **Complaint rate watched** in the provider's postmaster tools. Keep it under 0.1%;
      at 0.3% filtering starts (Google and Yahoo; Microsoft publishes no threshold).
- [ ] **Bounces and non-engagers removed** after each batch.

Read `references/deliverability.md` when the user is setting up DNS, diagnosing a spam
problem, or planning volume above a few hundred sends a day.

## Guardrails

- Relevance over volume. When the user wants to widen the list, push to tighten it first.
- Benchmarks in this skill are vendor-reported ranges, not facts. Say so when quoting them,
  and tell the user to re-baseline against their own numbers.
- Legal content is reference, not advice. Point to qualified advice before a real
  programme in a new jurisdiction.
- Never draft copy that misrepresents who is sending, invents a prior relationship, or
  uses a fake "Re:" subject line.

## Example

A founder selling scheduling software to physiotherapy clinics wants a sequence for 40
clinics that have posted a job for a receptionist in the last fortnight.

- **Shape:** 7 touches over 18 days. Email day 1, call day 3, email day 4, connection
  request day 6, email day 9, call day 12, short break-up email day 18.
- **First email (74 words):** subject "front desk hire". Opens with the job post ("Saw
  you're hiring a receptionist at the Leeds clinic"), names the usual cause (phones and
  rebooking eating the front desk's day), one line of proof from a similar clinic, then
  "Worth seeing before you fill the role?"
- **Pre-flight:** new domain registered three weeks ago, so warm-up is not finished.
  Recommendation: start at 10 a day from two inboxes, reach the full 40 over the first
  week, and send the calls from day one because they do not touch the domain.

## Configuration

- **Sending set-up:** the user's sending domain(s), inbox count and sending tool, so the
  pre-flight can be checked against what actually exists.
- **Recipient countries:** decides which legal regime the sequence is built for.
