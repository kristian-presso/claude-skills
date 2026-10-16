# Signal scoring

A buying signal is a public, dated event that makes the product more relevant now than
last month. Weight each by how directly it links to the product, discount it by age, and
act on the strongest within days. Only sourced, dated signals count.

## Starting weights

Tune these to the product during motion design.

| Signal | Example | Start weight |
| --- | --- | --- |
| Leadership change in the buying team | a new head of the function the product serves | 3 |
| Initiative the product serves | a public plan, strategy or job post naming the problem | 3 |
| Hiring surge in the buying team | several open roles in the function | 2 |
| Funding, acquisition or expansion | a round, a merger, a new market or site | 2 |
| Tech change next to the product | adopting or dropping an adjacent tool | 2 |
| Pain made public | an outage, a complaint, a regulatory finding | 2 |
| Peer or competitor move | a close peer buys, launches or wins on this | 1 |
| Executive talks about the topic | a post, a talk, a podcast | 1 |
| Customer usage change (expansion only) | a new team active, a limit hit, usage falling | 3 |

## Score

`signal score = weight x freshness`, with freshness 1.0 under 14 days, 0.5 at 15 to 45
days and 0 after 45 days. Sum per account and cap at 10. That is the timing axis for
tiering.

## The weekly sweep

1. For every tier-1 and tier-2 account, search the last 14 days: the company newsroom,
   blog and careers page, news for the company name with signal words (funding, acquires,
   appoints, launches, hiring, partnership, outage, regulator), and the buying-team
   leaders.
2. Record each hit as account, signal type, one-line fact, date, source URL.
3. Drop anything undated or unsourced. One event covered by ten outlets is one signal.
4. Rescore, retier, and surface the top five accounts with one line each on why now.

## Mistakes to avoid

- **A job post read as proof of a project.** It shows intent: "they are hiring for X",
  not "they are building X".
- **Personal life events as signals.** A new baby or a house move is never a reason to
  sell, and makes the outreach creepy.
- **These weights as truth.** They are starting heuristics. After a month, compare reply
  rates on signal-led touches with touches that had no signal, and adjust.
