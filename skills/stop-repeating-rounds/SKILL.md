---
name: stop-repeating-rounds
description: Decide whether to launch another fix-and-review round or stop and rethink with the user. Use before starting the second round on something that was already fixed and reviewed once, when a review keeps finding the same kind of problem one layer deeper, or when several agents have been dispatched on the same issue without closing it. Do not use to decide whether work is finished, or when you are stuck and need a different angle.
---

# Stop repeating rounds

## The pattern

A fix is made and reviewed. The review rejects it. The fix is corrected and reviewed again. The review rejects it again, for a different but similar reason. Each round costs a lot and each one delivers valid work: real defects found, tests turning from red to green. Nothing feels like failure.

A typical case: several agent runs over an afternoon consume a large share of the budget and produce two "not deliverable" verdicts. What settles the question takes minutes: calling the real external service and looking at the response. None of the agents could do that, because none had the credentials.

**The trap is that every round delivers valid work.** So the signal cannot be "this is not progressing"; it feels like progress.

The real signal is checkable: **the new review's finding is the same kind as the previous one, one layer deeper.**

- Round 1: "what you fixed is not protected by any test."
- Round 2: "what you fixed is still not protected, and the test that protected it is not in the suite."
- Round 3 would be the same again.

When that happens, the problem is no longer the one being fixed. Often it has become "the project's way of testing cannot see this class of defect". Another round does not fix that. Deciding with the user that this is now the work does.

## The check, before the next round

Do it **before** writing the next brief. It takes a minute.

1. **Write the finding you expect the review to return.** One sentence, before launching anything. If it resembles the previous verdict, the round will not change the problem: stop. If you cannot write what you expect to find, you are not launching a round, you are repeating a gesture.
2. **Is severity decreasing or moving?** If each round finds **less severe** defects, it is converging: continue. If each round finds **equally severe** defects in another layer, it is recursing: stop.
3. **Is there a measurement that would settle this and that nobody has made?** If so, it is worth more than the whole round and is usually cheaper. Make it first. If only you have access to the real system (credentials, machine, network), only you can make it, and no delegated agent will substitute for it.
4. **How many rounds did you say this would take?** Declare it before the first one: "this is two rounds". A declared budget turns the third round into a conscious decision instead of inertia.

## Stopping completely

Stopping is more than not writing another brief:

1. **Check what is still running, by executing a check.** Processes, scheduled jobs, agents. A long test run, such as a mutation-testing job, can hang for an hour without anyone noticing.
2. **Write the state down**: what is closed and verified, what is open by severity, and which decisions wait for the user. If someone else resumes tomorrow, everything must be there.
3. **Tell the user what was gained and what was not.** Stopping is not failing. Say what now works, verified, and say what is still not deliverable.
4. **Bring the underlying decision to the user.** What to build now, and with what scope, is theirs.

## Hard rules

- **Run this check before the second round of any fix-and-review cycle**, not from the third. By the third you are already two rounds too deep.
- **If you cannot state what you expect the review to find, do not launch it.**
- **A measurement against the real system beats a round of briefs.** When one exists, it goes first.
- **No delegated agent can measure what only you can execute.** Recognizing that early saves the whole round.
- **Stopping is a declared decision with its reason**, not silence.

## Limits

This skill does not decide whether work is finished and does not replace an independent review before delivery. It is not for being unable to solve something; there the frame is wrong and a different approach is needed, such as reproduce-before-fixing or a fresh discussion of the problem with the user. Here the frame is fine and the extra rounds are the waste.
