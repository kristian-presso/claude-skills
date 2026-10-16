---
name: linkedin-post
description: Drafts LinkedIn posts in the person's own voice, learned from three to five of their past posts rather than a generic template, from a rough idea, a one-liner, notes or a longer article. Also cuts one article into two or three standalone posts. Use when someone says "write a LinkedIn post", "turn this into a LinkedIn post", "draft a post about", "make this sound like me on LinkedIn", "write a short thought", or pastes an idea and asks for a post.
---

# LinkedIn post

Most AI-drafted LinkedIn posts sound the same: a one-word hook, a line break after every
sentence, a lesson, a question at the end. People scroll past them because they recognise
the shape.

This skill writes in **the person's** voice. It learns that voice from their own posts,
records it as a short profile, and checks every draft against it.

## Step 1: get the voice

Look for, in this order:

1. A voice profile already in the conversation or project (from an earlier run).
2. Three to five of their past LinkedIn posts, pasted or in a file. Ask for ones they are
   happy with, ideally a mix of short and long.
3. Other writing of theirs: blog posts, newsletters, emails.

If there is nothing, ask once: "Paste three to five posts you have written that sound like
you, and I will match them." If they would rather not, write in a plain, direct default
(short sentences, concrete detail, no hype) and say that is what you did.

Build a **voice profile** from the samples. Read `references/voice-profile.md` for the
method and the template. It takes a minute and covers: typical length, how posts open, line
and paragraph rhythm, vocabulary and words they never use, how they handle numbers and
names, tone, how posts end, and formatting habits (emoji, hashtags, lists, dashes).

Show the profile in five to eight lines and offer to save it so the next run can skip this
step. Never copy sentences from the samples into new drafts.

## Step 2: find the one point

Every post makes one point. From the person's idea, notes or article, write down:

- **The point**, in one sentence.
- **The proof**: the number, story, example or before-and-after that makes it believable.
  It must come from the person. Never invent a statistic, client, result or anecdote; if
  the post needs one, ask, or leave `[ADD: ...]`.
- **Who it is for**, if it is not obvious.

If the brief is vague, ask one question: "What is the single point, and is it a claim, a
number or a story?"

## Step 3: pick a length

| Tier | Words | Use for |
| --- | --- | --- |
| Short | 40 to 120 | One observation, one sharp line. A "thought". |
| Medium | 150 to 250 | A story or a take with one specific number. |
| Long | 300 to 450 | A real multi-step argument or how-to. |

Default to the tier the person's own posts mostly use. If they have no samples, default to
short. LinkedIn shows roughly the first 200 characters before "see more", so whatever the
length, the opening line has to earn the click.

## Step 4: draft

Shape:

```text
Opening line: the point, a specific number, or the most surprising detail.

One or two lines that set it up, only if needed.

The body: the proof, in their rhythm.

The landing: one line the reader could repeat.

Optional: one question or call to action, only if their posts usually have one.
```

Apply the profile, then these defaults unless the profile says otherwise:

- The point in the first line. No warm-up.
- Concrete over abstract: names, numbers, places, prices.
- One idea. If two ideas compete, offer to split them into two posts.
- No engagement bait ("Agree?", "Thoughts?", "What do you think?").
- No hashtags unless the person uses them; if they do, three at most at the end.
- No emoji unless the person uses them.

Read `references/hooks.md` for opening patterns that work and ones to drop.

## Step 5: check before showing

- [ ] Reads like their samples, not like a template. Read it against two of them.
- [ ] One point, stated in the opening line.
- [ ] Every fact and number came from the person.
- [ ] Within the chosen length.
- [ ] No phrase from the "drop" list in `references/hooks.md`.
- [ ] Spelling and punctuation follow their locale and habits.

## Output

One draft, not three. Print it ready to paste. Under it, one line: tier, word count, and
anything marked `[ADD: ...]`.

If they ask for alternatives, give a second version with a different opening line only.

## Cut mode: one article, several posts

When the input is an article or long piece and the person wants several posts:

- Find the genuinely distinct points. Two or three is typical.
- Each post stands alone: no "part 1", no "link in comments for the rest", no teaser that
  holds back the payoff.
- Different angles, not the same point reworded. If the article has one real point, write
  one post and say so.
- Short or medium tier for each.
- Number them and suggest spacing them at least a few days apart.

The `content-atomisation` skill in this plugin plans the wider multi-channel version.

## Publishing

This skill drafts. It does not post. If the person has a LinkedIn or social scheduling tool
connected and asks to publish:

1. Show the exact final text and the target (personal profile or company page). Ask which
   if they did not say.
2. Ask for an explicit yes to that exact text.
3. Only then post or schedule, and report back the link or scheduled time.

Never publish on an ambiguous "post it" without that confirmation.

## Example

> **User:** Post about how we stopped doing discovery calls for orders under 500 pounds.
> Here are three of my old posts: *(pasted)*
>
> **Claude:** Your profile: short posts (80 to 120 words), open with a plain statement of
> what you did, no questions at the end, British spelling, numbers written as figures,
> occasional dry aside in brackets, never uses hashtags.
>
> > We stopped doing discovery calls for orders under £500.
> >
> > They were taking 40 minutes each. Most ended with the client picking the package they
> > had already looked at on the website.
> >
> > Now small orders go straight to a short form and a booking link. Bigger jobs still get a
> > call (those are the ones where the call changes the answer).
> >
> > [ADD: what happened to conversion or time saved]
> >
> > The call was for us, not for them.
>
> Short tier, 78 words. Needs one result from you where marked.

## Configuration

Two things vary per person:

- **Their voice samples or saved profile.** The skill is only as close to their voice as
  the samples it learned from.
- **Locale.** British or American spelling, currency and date format. Take it from their
  samples if not stated.
