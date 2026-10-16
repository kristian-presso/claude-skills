# Metrics and testing

Judge a sequence on the numbers that survive privacy changes, and change it only on
evidence.

## Benchmarks

As of June 2026. These are vendor-reported, inconsistent between vendors, and refreshed
yearly. Use them to see whether you are roughly on the map, then re-baseline against your
own data. Never present them to anyone as fact.

| Metric | Reported range |
| --- | --- |
| Cold email reply rate, average | about 3 to 4% |
| Reply rate, top campaigns | 10% and above |
| Reply rate, enterprise and C-suite | about 1 to 2% |
| Reply rate, mid-market directors and VPs | about 3 to 5% |
| Reply rate, tightly segmented signal-led campaigns | 10 to 20% and above |
| Positive reply to meeting | about 15 to 30% |
| Sequence started to meeting booked | about 1.5 to 4% for strong programmes |

## What to track

- **Do not optimise on opens.** Mail privacy features load tracking pixels
  automatically, so open rates are inflated and unreliable.
- **Weight reply rate, positive-reply rate and meetings booked.**
- **Track per step**, so you can see where people drop and which touch earns the replies.
- **Watch bounce and complaint rates as health metrics.** They gate everything else
  through deliverability.

## Running a test that means something

- **One variable at a time.** Subject line, or opening line, or the ask. Not all three.
- **Enough volume.** Roughly 300 to 500 recipients per variant, sent over 48 to 72 hours
  of normal business days. Below that, differences are mostly noise.
- **Promote on two numbers.** A winner should hold or improve both reply rate and meeting
  rate before rollout. A subject line can lift replies while lowering meeting quality.
- **Write the hypothesis first.** "A timing-based hook will beat a problem-based hook on
  meetings" is testable; "try a new subject" is not.

One reported finding worth testing, not trusting: openers built on timing ("you just
did X") reportedly beat openers built on a problem statement by two to three times on
reply and meeting rate. It comes from a single study.

## Small lists

Most founders send to dozens or low hundreds, not thousands. At that size, A/B testing
cannot reach significance. Instead:

- Change one thing per batch and keep notes.
- Read every reply, including the "not interested" ones, for the reason.
- Treat five or more replies saying the same thing as a stronger signal than any
  percentage.
