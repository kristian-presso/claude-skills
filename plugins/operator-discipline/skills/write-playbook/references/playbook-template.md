# Playbook template

Copy this into wherever your playbooks live, name the file for the process
(for example `client-onboarding.md`), and fill every section. Delete any section that
genuinely does not apply.

```markdown
# <Process name>

**Owner:** <named person, role, or agent>
**Last updated:** DD/MM/YYYY
**Review by:** DD/MM/YYYY  (about 90 days out)

## Outcome

<One sentence: what is true when this is run correctly.>

- **Starts:** <the trigger>
- **Stops:** <the end point>

## Before you start

- <Access needed, for example "Admin login to the accounting tool">
- <Inputs needed, for example "The signed proposal PDF">
- <Tools needed>

## Steps

1. **<One action>.** <Where, exactly. What to click or type.>
   You should now see: <the observable result>.
2. **<One action>.** <...>
   - If <condition>, do <X>.
   - If <other condition>, do <Y>.
3. **<One action>.** NEEDS APPROVAL: <who approves, and what they are approving>.

## Done when

- [ ] <Observable end state, checkable by someone who was not there>
- [ ] <...>

## Exceptions

| Situation | What to do |
| --- | --- |
| <edge case> | <action> |

## Changelog

- DD/MM/YYYY - Playbook created from a live run with <role>.
```

## Notes on filling it in

- **Steps marked inferred.** If you wrote a step from a transcript or a description
  rather than watching it done, add "(inferred - confirm)" at the end of the step and
  remove it once someone has run it.
- **NEEDS APPROVAL** marks any step that spends money, sends something outside the
  business, or cannot be undone. A person or agent running the playbook stops there.
- **The index.** Keep one page that lists every playbook with its owner and review date.
  When a review date passes, the owner re-runs the playbook, fixes anything that drifted,
  and bumps both dates.
