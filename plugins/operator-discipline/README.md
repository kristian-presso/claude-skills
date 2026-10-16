# operator-discipline

Six skills for Claude about how an agent behaves when it does real work for a busy founder.
Not frameworks: gates and habits that stop good work going in the wrong direction.

The default failure of a capable agent is not incompetence. It is confident, well-executed
work against a brief nobody checked, followed by a bare problem handed back with the
thinking left undone. The first two skills are gates against exactly that. The other four
turn recurring work into something that survives the person who knows how to do it.

## Skills

| Skill | Use it when |
| --- | --- |
| **pushback** | A request is vague, has more than one reasonable reading, contradicts a decision already made, or is expensive to get wrong. Fires before work starts. |
| **solutions-shape** | You are about to report a blocker, failure, ambiguity or set of options. Reshapes it into finding, recommendation, action. |
| **setup-guide** | You are setting up a tool, account or integration, or a step in an existing guide turns out wrong. Writes a guide a stranger can follow first time, and fixes it in place. |
| **write-playbook** | A recurring process lives in one person's head. Documents it from a real run, hands it to a named owner with a review date and a done-check. |
| **meeting-notes** | You have a transcript or notes from a meeting. Produces decisions, actions with owners and dates, open questions, and a follow-up email draft. |
| **level-up** | You want to know the single next thing worth automating. Asks five questions one at a time and commits to one recommendation. |

## Make it always-on

Skills load when their description matches the conversation, so `pushback` and
`solutions-shape` will not be in view on every turn. To make the two gates apply every
session, paste this into your `CLAUDE.md` (each skill's own "Make it always-on" section has
a longer version):

```markdown
## Operator discipline (always on)
- Before starting a request that is vague, has two readings, contradicts a decision or is costly to get wrong: one message with my reading, the risk, one question.
- Never hand back a bare problem: every blocker, status update and end-of-task report is Finding, Recommendation (one pick and why), Action.
- Clear, cheap and reversible: just do it.
```

## Install

In Claude Code:

```bash
/plugin marketplace add kristian-presso/claude-skills
/plugin install operator-discipline@claude-skills
```

On claude.ai or the Claude desktop app, upload any skill folder (for example
`skills/pushback/`) as a custom skill.

## Configuration

Each skill ends with a short **Configuration** section naming the one or two things that
genuinely vary (where your decisions live, where guides and playbooks are kept, which notes
tool you use). None of them need any particular directory layout or service to work.

## Feedback

Used one of these? [Tell me what worked and what broke](https://tally.so/r/7XlJbL?source=operator-discipline) - two minutes, every answer read.

## Licence

MIT.
