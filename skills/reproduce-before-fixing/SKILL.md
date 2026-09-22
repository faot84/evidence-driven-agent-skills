---
name: reproduce-before-fixing
description: Locate the cause of a failure before changing anything. Use when something errors, behaves differently than expected, used to work and no longer does, or fails intermittently, in code, configuration, environments, or integrations. Requires a reliable reproduction, a falsifiable hypothesis, and a negative control. Do not use to design something new or to judge a finished delivery.
---

# Reproduce before fixing

## The rule that orders everything else

**Do not change anything until you can reproduce the failure on demand.** A fix applied to a failure you cannot reproduce cannot be verified: if the symptom disappears, you will not know whether you fixed it or hid it. Intermittent failures punish this rule the most and need it the most.

## Procedure

1. **Separate symptom from failure.** Write down exactly what you observed and what you expected, without interpretation. "It errors" is not a symptom; the literal message is.
2. **Reproduce it.** Find the smallest sequence that triggers it and record it. If you cannot reproduce it, that is now the problem: add instrumentation until you capture it.
3. **Bound the change.** What changed between working and failing: code, data, versions, configuration, permissions, network, clock, environment? If nothing changed and it still fails, it never fully worked. Ask instead what new condition exposed a latent defect.
4. **Bisect.** Split the path in half and check which half contains the failure. Repeat. It is dull and it is the fastest method there is, for lines, steps, commits, and modules alike.
5. **State a falsifiable hypothesis.** "It fails because X" must come with "if it is X, then doing Y should produce Z". A hypothesis that predicts nothing checkable is not a hypothesis.
6. **Test the hypothesis before fixing.** Confirm the cause, then fix. Never the other way round.
7. **Run a negative control.** Revert the fix and confirm the failure returns. If it does not return, you had not found the cause. This is the step almost everyone skips, and it turns a hunch into a demonstration.

## Mistakes that cost the day

- **Fixing the symptom.** Silencing an error, wrapping it in a broad exception handler, raising a timeout. The defect remains and is now invisible.
- **Changing several things at once.** If it works, you do not know which change fixed it; if it does not, you do not know which one made it worse. One change at a time.
- **Believing the error message about location.** It shows where the program crashed, not where it broke. The cause is usually earlier.
- **Dismissing the boring causes.** Clock skew, permissions, a wrong path, a stale cache, a different version than you think, a file read from somewhere else. Check them before the elegant theory.
- **Treating timing as causation.** "It started after upgrading X" deserves a check, not belief.
- **Debugging on moving data.** Freeze the input. If the input varies, you are measuring noise, not the failure.

## When to bring in help

- Environment, infrastructure, storage, startup, or recovery problems: someone with operations expertise.
- Proof that the fix works reproducibly: a test verifier.
- A code fix once the cause is known: an implementer, with the identified cause in the brief. Asking before the cause is known asks them to guess.
- Suspected credentials, permissions, or data exposure: a security reviewer.

## Closing

Record **the cause**, not only the fix. The fix is in the code; the cause is what prevents a repeat. If the defect was latent for a long time, note what kept it invisible. That is often worth more than the defect itself.

Report the reproduction, the hypothesis, the confirming check, and the negative control. If the negative control could not be run, say so explicitly.
