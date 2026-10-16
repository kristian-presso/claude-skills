---
name: level-up
description: Finds the single next thing worth automating in a small business or a personal workflow. Asks five short questions one at a time, then recommends one automation, says why it beats the runner-up, and says how it should be built (a scheduled script, a reusable skill or prompt, or an existing tool). Proposes only, never builds. Use when asked "what should I automate next", "level up", "where am I wasting time", "what's next to systemise", or as a weekly or monthly operating check-in.
---

# Level up

Most people know they should automate more and do not know what to automate next. The
usual result is either nothing, or a clever automation of something that did not matter.

This skill finds the **one** next automation with the best payoff, by asking a few sharp
questions and then committing to a recommendation. It does not build anything. Building is
the next conversation.

## The five questions

Ask them **one at a time**. Wait for each answer, reflect it back in one line so the person
knows you heard it, then ask the next. Never send them as a list: a list gets skimmed and
half-answered.

1. **"What did you do by hand three or more times this week?"**
   Repetition is the clearest signal. Ask for the boring specifics: which tool, how long
   each time.
2. **"What would break if ten times as many customers turned up on Monday?"**
   This finds the single points of failure: the step that only works because volume is low,
   or because one person does it.
3. **"Which part of the business still runs entirely by hand?"**
   Prompt with areas if they are stuck: getting paid, answering customers, scheduling,
   email, tasks, meetings, keeping knowledge written down.
4. **"What number do you check by hand that could just be sent to you?"**
   Revenue, sign-ups, bookings, overdue invoices, stock. A number checked by hand is
   usually checked late or not at all.
5. **"What did you put off this week because it was fiddly or boring?"**
   Avoided work is often the most valuable to automate, because it is currently not
   getting done.

If they skip a question or say "nothing", accept it and move on. If an answer is vague
("emails"), ask one follow-up for the specific case, then move on.

If you already have context on how they work (earlier in the conversation, or notes they
have shared), use it to sharpen the questions, and skip any question it already answers.

## Pick one

List the candidates from the answers, then choose **one**. Prefer the candidate that is:

1. **Frequent.** It happens often, so the time saved compounds.
2. **Well specified.** The steps are the same each time and you could write them down.
   A task that needs judgement each time is a poor first automation.
3. **Costly when missed.** Late invoices, unanswered leads, a number nobody saw.
4. **Small to build.** A first automation should be live within a day, not a quarter.

Name the runner-up in one line, so the person can overrule you knowingly. Do not present
three equal options.

## Say how it should be built

Match the build to the shape of the work. Choose the simplest thing that will do it.

- **Fully specified, same steps every time** (send the weekly numbers, chase invoices over
  30 days, back up a folder): a **scheduled script or a no-code automation** that runs on a
  timer. Do not reach for an autonomous agent when a plain scheduled job will do; it is
  cheaper, more predictable and easier to fix.
- **Repeatable but needs a bit of judgement** (draft replies to common enquiries, write up
  meetings, triage a support inbox): a **reusable skill or saved prompt** that an assistant
  runs on request, with a human approving anything that goes out.
- **Something an existing tool already does** (the accounting tool can send reminders, the
  booking tool can confirm appointments): **turn on that feature**. Name the setting.

## The recommendation

End with one short block:

```text
Next automation:  <what, in one line>
Why this one:     <frequency, cost of missing it, and why it beats the runner-up>
Runner-up:        <one line>
How to build it:  <scheduled script / skill or saved prompt / existing feature, and the
                  first concrete step>
Time saved:       <rough estimate per week, from their own answers>
```

Then stop. If they want to build it, that is a new task. Offer once, in one line.

## What it never does

- Build, edit or switch on anything. It proposes only.
- Offer a menu of equal options. One pick, one runner-up.
- Recommend an autonomous agent where a scheduled job would do.
- Ask all five questions at once.

## Example

> **Q1:** What did you do by hand three or more times this week?
> **A:** Copied new bookings from the booking form into the spreadsheet. About ten a day.
>
> *(Reflect, then Q2 to Q5. Answers: nothing would break at 10x except that spreadsheet;
> invoices are chased by hand; revenue is checked by logging into the bank.)*
>
> ```text
> Next automation:  Send each new booking straight to the spreadsheet.
> Why this one:     Ten times a day, identical steps, and it is the one thing that breaks
>                   at higher volume. Beats invoice chasing because that happens weekly.
> Runner-up:        Automatic reminders for invoices over 14 days overdue.
> How to build it:  No-code automation: booking form "new submission" to "add row". Check
>                   whether the form tool has a native spreadsheet integration first.
> Time saved:       About 1.5 hours a week.
> ```

## Configuration

None. If you run it on a schedule (weekly works well), keep the previous recommendation to
hand so the next run can check whether it was built.
