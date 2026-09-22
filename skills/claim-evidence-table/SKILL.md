---
name: claim-evidence-table
description: Before reporting any conclusion about the present state of a system (it works, it is fixed, tests pass, it starts, the cause is X, nothing is left), put every such claim in a four-column table with its status, the evidence that supports it, and how that evidence could be wrong. Use at the end of debugging, fixing, or verification work. Do not use for explaining concepts, conversation, or plans that assert nothing about the world yet.
---

# Claim-evidence table

## Purpose

A confident sentence reads the same whether or not anyone checked it. This skill makes missing evidence visible in the report itself. It does not make the assistant more careful; it makes the gaps impossible to hide behind fluent prose.

The typical failure it targets is not carelessness. It is reading code, generalizing, and reporting the generalization as an observation: "the suite passes" (it passed in a scratch copy nobody else can see), "the blockers are fixed" (an import is missing and the module does not start), "this value is always empty" (true only in the branch that was just edited).

## When to use it

Use it before sending any answer that states something about the current state of the world: a module works, a defect is fixed, tests pass, a file contains something, a setting is applied, a cause is identified, or something cannot be done.

Do not use it to explain a concept, to discuss data already present in the conversation, or to propose a plan. Applying it to everything is as useless as never applying it.

## The table

Place it at the end of the answer, always with the same four columns:

~~~text
| Claim | Status | How I know | How this could be wrong |
|---|---|---|---|
| The module starts and reaches the end | verified | `python -m app --selftest` printed `selftest ok`, exit 0 | the self-test may not reach the branch that failed |
| The limit can no longer be exceeded | unverified | `grep -rn "daily_loss" src/` found 0 writes | the pattern only sees the literal name, not dynamic attribute access |
| It behaves the same on Python 3.12 | unverified | only 3.11 is available here; needs a run on 3.12 | — |
~~~

Use exactly three statuses:

- **verified**: a command was run or a file was read in this session, and the evidence cell contains the command and its literal output, not a paraphrase.
- **inferred**: deduced from something verified. The cell names the source and the assumption.
- **unverified**: not known. The cell says what would be needed to know it. Do not disguise it as "probably", "should", or "in principle".

## The fourth column

A **verified** row with an empty fourth cell does not exist. Either fill it or downgrade the row to **unverified**. "I cannot think of anything" is not an answer: if you cannot describe how your check could produce a false pass, you have not looked at it as an adversary.

Example of the fourth column doing its job: a claim that "no hard-coded colors remain" is backed by a search for one naming pattern. The honest fourth cell, "my pattern only sees the forms I imagined", immediately downgrades the row, and a color written in a different form may still be in use.

When the claim is "this is now generated", "this is included", or "none are left", look for proof in the built artifact (the compiled CSS, the bundle, the binary), not in the source. A successful build says nothing about what the compiler silently chose to omit.

For claims about how a screen looks or behaves, the evidence is a screenshot path, not a build log. A screenshot can also mislead (different viewport, demo data, cached state), so the fourth column still applies. If no screenshot can be taken, the row is unverified and the pending check is the screenshot.

## Hard rules

- **A claim without a row is not written.** If a row cannot be filled, either go and check it or remove the claim from the answer. There is no third option.
- **Fill the table while working, not at the end.** Reconstructing it from memory produces the command that *would have* proved the claim. That is an alibi, not evidence. If you are writing a command you did not run in this session, the row is unverified.
- **If code was touched, the last row is always "it starts and reaches the end"**, with its output pasted.

## Four traps to check before signing

1. **Is the evidence where I say it is?** A result produced in a temporary copy does not exist for whoever audits the delivered tree.
2. **Can this check fail?** A check whose result cannot differ, such as an identity that is zero by algebra, verifies nothing and gives false comfort. Build the case where it turns red. If you cannot, the row is unverified.
3. **Does the whole thing start?** Every unit check can pass while the program dies on a missing import or a renamed parameter.
4. **Am I generalizing from the branch I just edited?** Before claiming "always X", look at what the opposite branch does, including empty inputs.

## Changing position

If you change your conclusion after the user objects, the first line of the answer states the new evidence. If there is none, only a different derivation, say so plainly: "no new measurement". A flawless argument resting on a fact nobody checked is the most expensive failure in this work.

## Quoting other agents

When you summarize another agent's work, its "not verified" statements travel with the quote. Its "verified facts" are not inherited: check them before passing them to someone else as a premise.

## Limits

This table does not replace running things and does not replace an independent reviewer. A table that is entirely verified does not mean the system is correct. It means these checks, and only these, found nothing.
