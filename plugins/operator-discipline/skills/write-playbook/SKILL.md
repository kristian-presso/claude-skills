---
name: write-playbook
description: Documents one recurring process as a playbook that someone else (or an agent) can run without the original person in the room - define the outcome, design the steps by watching the work being done, deploy to a named owner with a review date, and end with a done-check. Use when asked to "write a playbook", "document how we do X", "capture this process", "make this repeatable", "write an SOP", or when one person is the only one who knows how a critical recurring task is done. Not for getting a tool or account working once; use setup-guide for that.
---

# Write a playbook

A playbook makes one recurring process repeatable by anyone who holds it, so the business
does not depend on one person remembering how it is done.

It is not a setup guide (that is a one-off: get a tool working once) and it is not a
policy (that says what is allowed, not how to do it). A playbook is for work that happens
again and again: onboarding a client, closing the month, publishing an event, handling a
refund.

## Pick the right process first

Do not document everything. Unread documentation rots, and a library of stale playbooks is
worse than none, because people stop trusting any of them.

Write a playbook only for a process that passes at least two of these:

- **It recurs.** Weekly, monthly, or every time a customer does a particular thing.
- **Getting it wrong costs real money, a customer, or a deadline.**
- **Only one person knows how to do it well.** If they are off sick, it stops or goes
  wrong.
- **It is about to be handed to someone new,** a hire, a contractor, or an agent.

If the request is for a process that passes none of these, push back once: say which
process you would document instead and why.

## The three stages

### 1. Define the outcome

State, in one sentence, what the playbook produces when it is run correctly. Then state the
boundary: what starts it (the trigger) and where it stops.

```text
Outcome:  A new client has a signed contract, a paid first invoice, and a kickoff call booked.
Starts:   The client says yes on a sales call.
Stops:    The kickoff call is in both calendars.
```

If you cannot write the outcome in one sentence, you are not ready to write steps. Ask the
one question that would settle it.

### 2. Design the steps, from the person who does the work

Do not ask the expert to write the steps from memory. Experts skip the steps they no longer
notice, and those are exactly the steps a newcomer gets stuck on.

Instead, capture while the work is being done:

1. **Watch a real run.** Have the person who does this best (usually not the business
   owner) do it for real, or narrate a live run over a screen share or a recorded call.
   Write each step as they do it, including the silent ones: the tab they check first, the
   field they always double-check, the "oh, and if it's a Friday...".
2. **Write the draft at newcomer level.** One action per step. Name the tool, the exact
   screen, the exact field. Add a "you should now see..." line wherever a step can quietly
   fail. Spell out decision points ("If the client is VAT registered, do X. If not, do Y.").
3. **Prove it.** Have someone other than the author run the draft, ideally the person it
   will be handed to. Every place they hesitate or ask a question is a gap; fix it in the
   playbook, not in chat.

If you are an agent and cannot watch a live run, work from the best source you have (a
call transcript, a screen recording, a chat thread where the process was explained, the
tool's own history) and mark every step you inferred rather than observed. Ask the expert
to confirm those steps specifically.

### 3. Deploy to a named owner

Hand the playbook to a **named owner**: the person (or role, or agent) who runs it and keeps
it true. Set a **review date** about 90 days out. A critical process drifts fast: tools
change screens, prices change, a new exception appears.

A playbook with no owner or no review date is unfinished, not finished.

## What a finished playbook contains

Use the skeleton in [references/playbook-template.md](references/playbook-template.md).
At minimum:

- **Header:** owner, last updated, review by.
- **Outcome and boundary** (from stage 1).
- **Before you start:** access, tools, and inputs needed.
- **Steps** at newcomer detail (from stage 2).
- **Done-check:** a short list of things that are true when the run is complete, each one
  checkable by someone who was not there.
- **Exceptions:** the known edge cases and what to do about each.
- **Changelog:** dated lines, one per change.

## The done-check

Every playbook ends with a done-check, and a run is not finished until every line passes.
Write each line as something observable, not a feeling:

```text
Done when:
- [ ] Contract shows "Signed" in the e-signature tool.
- [ ] First invoice shows "Paid" in the accounting tool.
- [ ] Kickoff call is in the client's and our calendars, with the agenda attached.
- [ ] Client record in the CRM is moved to "Onboarding".
```

"Client is happy" is not a done-check line. "Client has replied to the welcome email" is.

## Playbooks that agents will run

A playbook written this way is also the natural spec for automating it. The steps an agent
or script would follow are the steps a person follows by hand. When a process is a
candidate for automation, write the playbook first; the automation is then a matter of
replacing steps, not discovering them.

Mark any step that needs human judgement or approval (spending money, sending something
external, anything irreversible) so an agent running it knows to stop and ask there.

## Guardrails

- **Only processes that matter.** Push back on documenting low-stakes, rare, or
  one-person-forever work.
- **Never author-from-memory alone.** Capture from a real run, then prove by having
  someone else run the draft.
- **No owner or no review date means not done.** Do not mark a playbook complete without
  both.
- **No secrets in the playbook.** Name the credential and where to get it; never paste the
  value.

## Example

Request: "Can you write up how we do month-end so the new bookkeeper can take it over?"

1. Define: "Outcome: the month's books are reconciled and the management report is sent
   to the directors. Starts: first working day of the month. Stops: report email sent."
2. Design: ask for a screen-share of the current person doing last month's close, or the
   recording if one exists. Capture each step (bank feed, unmatched transactions, payroll
   journal, report export), including the silent check they do on the card account.
   Mark two steps as inferred and ask about those.
3. Prove: the new bookkeeper runs the draft for this month with the old one watching.
   Three questions come up; each becomes an edit.
4. Deploy: owner is the new bookkeeper, review in 90 days, done-check lists the four
   observable end states.

## Configuration

- **Where playbooks live.** A `playbooks/` folder, a wiki section, a shared drive. Keep an
  index page listing each playbook, its owner and its review date, so overdue reviews are
  visible at a glance.
- **Review interval.** 90 days is the default for critical processes. Stable, low-risk
  processes can go longer.

Further reading: the "capture from the doer, not from memory" approach is close to the
method in *Systemology* by David Jenyns, which goes much deeper on systemising a small
business.
