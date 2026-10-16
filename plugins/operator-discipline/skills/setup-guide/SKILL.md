---
name: setup-guide
description: Writes or updates a for-dummies setup guide for getting a tool, service, account or integration working, proves every step before handing it over, and self-heals an existing guide the moment a step turns out wrong. Use when setting something up for the first time, when asked to "set up X", "write a setup guide for X" or "document how to set up X", and whenever following an existing guide and a step is wrong, missing, unclear or out of date. Not for a recurring process that someone runs again and again; use write-playbook for that.
---

# Setup guide

Every time something gets set up - a server, a secrets manager, an API, an account - write
it down as a guide simple enough that someone who has never touched the tool can follow it
without getting stuck.

The bar: **a competent stranger, no context, gets it working on the first try.**

A guide only its author can follow is not a guide. It is a souvenir.

## When this fires

1. **Setting something up.** Any first-time setup of a tool, service, account or
   integration. The guide is part of the deliverable, not an afterthought. Write it *as
   you go*, never from memory afterwards.
2. **An explicit request.** "Write a setup guide for X", "document how to set up X".
3. **A step is wrong.** You are following an existing guide and something is wrong,
   missing, unclear or out of order. The self-healing gate below fires, and it is not
   optional.

## The for-dummies standard

Write for a smart twelve-year-old who has never used the tool. Every guide:

- **Opens with "What you are doing, and why".** Plain-English purpose, naming the pain it
  removes.
- **Lists prerequisites up front,** in a "Before you start" section: accounts, cards,
  access, installed tools. If a prerequisite is already handled, say so and say "skip".
- **Gives a time estimate,** total at the top and per step in the heading, for example
  "## Step 1 - Sign up (3 min)".
- **One action per numbered step.** Never bundle two actions into one step.
- **Every command copy-paste-exact,** in a code block, runnable as-is. No placeholders
  unless the line directly above explains exactly what to substitute.
- **Version pins kept, with a note.** If a command pins a version, keep the exact pin so
  it runs as-is, and add one line saying where to check the current version. The pin is
  correct at time of writing; the self-healing gate updates it when someone hits a stale
  one.
- **Every UI step click-by-click.** Where the control is, its exact label, what to click
  next. "Top-left workspace name, then Settings, then Billing", never "go to billing".
- **Every step says what you should SEE.** A `Verify:` line or "you should now see...".
  The reader has to confirm a step worked before moving on.
- **No jargon without a one-line plain definition** the first time it appears.
- **Decision points spelled out.** "If you see X, do Y. If you see Z, do W." Never leave
  the reader guessing.
- **Ends with "You are done",** a **Troubleshooting** table mapping symptom to fix that
  covers every failure you hit while setting it up, and a **Deferred** section for anything
  deliberately out of scope.

Plain words. Short sentences.

A skeleton is in [TEMPLATE.md](TEMPLATE.md). Copy it and fill every section.

## Capture everything

The guide is wrong if it has a gap, and the step that feels too obvious to write down is
the one that blocks a stranger. While setting the thing up, record:

- Every command and flag, exactly as run.
- Every URL in full.
- Every click, every field, every value typed into a form.
- Every prompt the tool shows, and the exact answer to give.
- Every wait, with a duration: "takes about 30 seconds".
- Every thing that went wrong, and the fix.

If you are documenting a setup that is already done rather than running it live,
reconstruct each step concretely and check every command against the tool's current
documentation before publishing. Do not approximate from memory: a guide written from
memory is a guide with the obvious steps missing.

## Never write a secret into a guide

Reference credentials by name and say where to get them: "API key: dashboard, then
Developers, then API keys". Use a `REPLACE_ME` placeholder in any config block. For
verification steps, prefer a redacted check (print the first six characters and the length)
over printing the whole value.

A guide gets committed, and often copied elsewhere. A pasted secret leaks in every place
the guide lives.

## Prove the guide before you hand it over

A guide is a claim: *follow these steps and you get this result*. Hand it over unproven and
you have not helped. You have delegated your debugging to someone with less context than you.

**1. Run every command yourself first, including the verification.**

The verification step is the one most likely to be wrong, because it is written last and
looks obvious. A verification that fails for a reason unrelated to the reader's work is
worse than none: they conclude they broke something and stop.

A real pattern: a credential-rotation guide ships with a check that returns `401` against
the *existing* credential, because that credential was already dead. The reader rotates
correctly, runs the check, sees `401`, and believes they failed. Running it first catches
this, and often reframes the task - it was not tidying a working credential, it was
replacing a broken one.

Where a command cannot run until the human acts, say so and state what it should print
when it works. Where a check will fail *before* the task is done, say that too: it tells
the reader the test is real.

**2. Never state a UI detail you have not seen.**

You are often describing a dashboard you cannot see. A confidently wrong click-path is worse
than an admitted gap, because the reader trusts you over their own screen and stalls.

- Identify things by properties the reader can see - a name, a permissions summary, a
  "last used" timestamp, a status badge - never by a value only an API returns. Internal
  IDs are often not shown in the UI at all.
- Prefer a deterministic trick over a description: have the reader do something whose
  effect they can watch (use the credential, then refresh and pick the row that changed).
- Say what you verified and what you inferred. Mark a corrected step as corrected rather
  than silently rewriting it; it shows the guide is maintained.
- Add a **safe to explore** note wherever it is true ("nothing is saved until you click
  Create"). Fear of breaking something is the most common reason a reader stops.

**3. Deliver it where it will be read.**

The bar is a tired person at 11pm on a phone. A file path in a repository does not meet it
on its own. If you can, publish the guide somewhere openable on a phone (a wiki page, a
shared doc, a rendered page) and hand over the link, keeping the source file as the
canonical copy. Put every command in its own code block so it can be copied in one tap.

## The self-healing gate

**If you follow a guide and any step is wrong, missing, unclear or out of order, you fix
the guide file in the same session, before reporting the task done.**

Not "note it for later". Not "mention it in chat". Fix the file.

When you fix it:

1. Edit the step so it matches reality.
2. Bump the `Last verified:` line to today's date.
3. Add a dated line to the `## Changelog` section at the bottom, creating it if absent.
4. If the guide is published anywhere else, update every copy. The next reader hits the
   same step.

When a reader reports a step is wrong, that is the most valuable feedback the guide will
ever get. Fix it before continuing the conversation.

If the guide lives in a repository other people or agents are actively changing, make the
fix on a fresh branch or separate worktree from the latest main, not in a checkout that
might switch branches under you mid-session. Edits made in a busy shared checkout are easy
to lose.

### Red flags. Stop when you think one of these

| Rationalisation | Reality |
| --- | --- |
| "I'll just do the correct thing and move on" | The next person does not know the correct thing. The guide is the only memory. |
| "The guide is 95% right" | The missing 5% is exactly what leaves a stranger stuck. |
| "I'll mention the gap in chat" | Chat is not the guide. The fix dies in the history. |
| "It's a tiny wording thing" | Tiny wording is what trips a beginner. |
| "The guide wasn't wrong, the tool changed" | Same outcome: it no longer matches reality. |
| "I'll fix it next time I run this" | There is no guaranteed next time. |

A guide that gets followed and not corrected rots silently, and the rot is invisible until
it wastes someone's morning.

## Common mistakes

- Writing the guide from memory afterwards, which loses the obvious steps.
- "Configure it as needed" or "set up your account": vague non-instructions. Every step is
  concrete or it does not belong.
- Skipping the verify line, so the reader cannot tell whether a step worked.
- Shipping a verify command you never ran.
- Pasting a real secret.
- Leaving out a failure you hit because you already fixed it. If it bit you, it bites the
  next person.

## Configuration

**Where guides live** varies by project. Pick one location and keep to it: a `docs/setup/`
directory, a dated folder per guide, a wiki. Two properties matter more than the choice:
the location is greppable, and the file carries its own `Last verified:` date, so freshness
is a property of the file rather than of a directory name.

Optionally, **where a phone-readable copy goes** (a wiki, a shared doc). If you have one,
mirror every guide there and keep both in step.
