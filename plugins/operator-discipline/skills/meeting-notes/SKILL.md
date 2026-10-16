---
name: meeting-notes
description: Turns a meeting transcript or rough notes into decisions, actions with owners and dates, open questions, and a short follow-up email draft. Works with a pasted transcript, a file, or a connected notes or recording tool. Use when asked to "write up this call", "analyse this meeting", "what did we agree", "meeting notes", "action items from this", "draft the follow-up", or when a transcript or recording link is shared and the user wants it worked up.
---

# Meeting notes

A meeting is only worth what it changes afterwards. Most notes record what was said. This
skill records what was **decided**, who is **doing** what by **when**, and what is still
**open**, then drafts the follow-up so it actually gets sent.

## Get the material

Use the best source available, in this order:

1. **Connected notes or recording tool.** If a meeting-notes, transcription, or recording
   tool is connected (any tool that returns a meeting's transcript or summary), find the
   meeting by title, date or attendee and pull the full transcript, not only the tool's
   summary. Summaries drop the decisions that were made in passing.
2. **Calendar.** If a calendar is connected, use it to fill in the attendee list, date and
   meeting title, and to check the spelling of names.
3. **A file or a paste.** A transcript, a recording's text export, or rough bullet notes.

If you have nothing but a meeting title, ask for the notes. Do not write up a meeting you
have not seen.

Rough notes are fine. Work with what is there and flag anything you had to guess.

## What to extract

Read the whole thing before writing anything. Then pull out:

**Decisions.** Things that were agreed and now change what people do. "We'll go with the
annual plan", "launch moves to the 14th". Not opinions, not ideas floated and dropped.
If a decision was implied but never said out loud ("so... we're doing the annual plan
then?" with no objection), list it and mark it *(implied - confirm)*.

**Actions.** Every action has three parts. If one is missing, say so rather than invent it.

- **What:** a concrete deliverable, starting with a verb. "Send the revised quote", not
  "pricing".
- **Owner:** a named person. "We" and "the team" are not owners. If nobody took it, write
  *Owner: unassigned* and list it under open questions.
- **Due:** a date. Convert relative dates ("by Friday", "next week") to real dates using
  the meeting date, and show both if it helps. If no date was given, write *Due: not set*.

**Open questions.** Things raised and not resolved, and anything needed before an action
can start. Name who is best placed to answer each one.

**Risks or concerns** raised, briefly, if any were. Skip the section if none.

## Accuracy rules

- **Names:** check proper nouns (people, companies, products) against the attendee list
  and any context you have. Transcription tools mangle names. If unsure, write the name as
  heard and add *(spelling?)*.
- **Never invent.** No owner, date, number or decision that is not in the material. A gap
  you flag is useful; a gap you fill with a guess is a future argument.
- **Attribute carefully.** Only say "Sam agreed to..." if Sam did. If it is unclear who
  said something, do not attach a name.
- **Keep personal matters out.** If the conversation strayed into someone's health,
  family, personal finances or private life, leave it out of the write-up and the email
  unless the user asks for it. Mention in your reply that you left something out, without
  repeating it.
- **No secrets.** If a password, key or account number was read out, do not copy it into
  the notes.

## The write-up

Use this structure. Lead with the summary so the whole meeting reads at a glance.

```markdown
# <Meeting title> - <DD Month YYYY>

**Attendees:** <names>
**Source:** <transcript / notes / recording tool>

## Summary
<One or two sentences: why the meeting happened and what came out of it.>

## Decisions
1. <Decision>
2. <Decision> *(implied - confirm)*

## Actions
| # | Action | Owner | Due |
| --- | --- | --- | --- |
| 1 | <Verb-first deliverable> | <Name> | <DD Mon> |
| 2 | <...> | unassigned | not set |

## Open questions
- <Question> - best placed to answer: <name>

## Risks raised
- <Risk>  (delete this section if none)
```

Keep it short. A 45-minute call usually produces under a page. Do not narrate the
discussion; the transcript exists if anyone wants it.

## The follow-up email

Draft a short email the meeting owner can send to attendees the same day. It confirms the
decisions and the actions, so anyone who remembers it differently says so now rather than
in a fortnight.

- **Subject:** "<Meeting title> - decisions and next steps"
- **Body:** a one-line thank-you, the decisions as a short list, the actions as
  "Owner - action - due date", the open questions, and one line asking people to reply if
  anything is wrong or missing.
- Under 200 words. Plain, warm, no filler.
- Write it from the user's point of view ("I'll send the revised quote by Thursday").

Present it as a draft. Never send it yourself unless the user explicitly asks you to and
you have a connected email tool. If they ask, show the final text and confirm before
sending.

## After the write-up

Offer, in one line, the most useful next step you can actually do with the tools you have.
Pick one, not a menu. For example:

- Create the actions as tasks or tickets in a connected task tool (with approval).
- Add the due dates as calendar reminders.
- Save the write-up where the user keeps meeting notes.

Do not do any of these without a yes. Filing tickets or sending email on someone's behalf
is outward-facing.

## Preparing for a follow-up meeting

If asked to prep for a meeting with people you have notes on, pull the previous write-ups
with those attendees and give a short brief: what was decided last time, which actions
are still open (and whose), and the open questions worth raising. Do not write a new
record for a meeting that has not happened.

## Example

Input: a 30-minute transcript between a founder (Alex), a designer (Priya) and a client
(Tom) about a website relaunch.

Output, abridged:

```markdown
# Website relaunch check-in - 14 October 2026

**Attendees:** Alex, Priya, Tom (client)

## Summary
Reviewed the homepage design. Tom approved the direction; launch moves a week to fit
the extra case-study page.

## Decisions
1. Homepage design approved as shown.
2. Launch date moves from 21 to 28 October.
3. Case-study page added to launch scope *(implied - confirm)*.

## Actions
| # | Action | Owner | Due |
| --- | --- | --- | --- |
| 1 | Send two case-study drafts | Tom | 17 Oct |
| 2 | Design case-study page template | Priya | 21 Oct |
| 3 | Update project plan and share | Alex | 15 Oct |
| 4 | Confirm hosting renewal | unassigned | not set |

## Open questions
- Does the new launch date affect the press release? - best placed to answer: Tom
```

## Configuration

- **Your notes source.** If you use a meeting recording or transcription tool, connect it
  so the skill can fetch transcripts directly. Otherwise paste or attach the notes.
- **Where write-ups go.** A notes folder, a wiki, a CRM record. Tell Claude once and it
  will offer to save there.
