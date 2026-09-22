---
name: brief-a-subagent
description: Prepare a written brief before delegating substantial work to a subagent or another assistant. Use when handing off a review, analysis, test run, or implementation that will take significant effort. Requires verified input paths, a named destination file for the report, a response limit, prohibitions, a stopping condition, and a self-refutation request. Do not use for trivial questions or for handing an entire project to another assistant.
---

# Brief a subagent

## Why it matters

In many products, a delegated agent that has finished cannot be resumed. If its long report comes back only as a chat message and gets truncated, the work is lost. If its brief contains a false statement, it spends its budget discovering that. Often an expensive delegation failure turns out to be a brief failure: the agent obeyed a wrong map.

## Before delegating, decide whether it is needed

Delegation costs real time and tokens. Do not delegate what you can answer with the same quality yourself. Delegate when the task belongs to a separate expertise, when an independent judgment is needed, or when the answer will be relied on and needs backing.

If you hesitate between two agents, the task is not well bounded yet. Bound it first.

## Step 0: verify the inputs before writing the brief

**Whatever you state in a brief is not context; it is an instruction.** The agent will not question it. Three checks, each one command:

1. **Every path exists.** List every path you will name: inputs, destination, code. Check the disk, not your memory. Folders move.
2. **What already exists on this topic.** List recent documents in the project, including loose files in its root, with date, size, and title, and include that list in the brief. Anything you do not name, the agent will declare missing and rebuild, usually worse.
3. **What you have not checked yourself.** Mark it in the brief as a hypothesis, in those words. A false fact you present as true costs more than a missing fact, because the missing one gets searched for and the false one gets believed.

## The brief: nine required parts

1. **Sender and project.** If it is one of several briefs, number it: "Brief 2 of 3."
2. **Destination file, named explicitly.** Full path, one file. Without it, the report returns as a message and, if long, is truncated and lost. This is the part most often forgotten and the most expensive one to forget.
3. **Chat response limit.** "All detail goes to the file. In chat, at most N lines: [what you want to see]."
4. **Inputs, with paths, in two layers.**
   - First the **state**: a status file or handover note, to be read completely. It is the map.
   - Then the **originals**, saying what each one is for: specification, reference only for checking quotes, or do-not-open unless needed.
   - If an input is huge, say so and ask for targeted search or reading in sections.
5. **Prohibitions.** What it must not read or change. Carry them over from the project; do not rely on the agent guessing them.
6. **Binding decisions from others.** If a security reviewer already decided something, it goes here as a constraint, not a suggestion.
7. **What to deliver, enumerated.** Concrete items. If something is out of scope because it belongs to another brief, say so.
8. **Stopping condition.** Where the work ends and what it must not do even if it could.
9. **Self-refutation.** Add the two questions below at the end of "what to deliver". They cost two sentences and are the highest-value lines in the brief:

   - **"What else in your work could be false for this same reason?"** Apply it to earlier work too, not just today's.
   - **"What lies outside the range your tests or analysis cover?"** Not what they check, but what they do not. A grid of 40 combinations that fixes one variable does not check that variable.

## Hard rules

- **Never run two briefs in parallel if one needs to read the other's output.**
- **Split large work.** A brief covering architecture, concurrency, and persistence at once exhausts the agent and produces a report that cannot be returned.
- **Check which tools the agent actually has before writing the brief.** Ask agents that can execute to measure, not to propose commands. Ask agents that cannot execute to end with the exact commands to run and the output they expect from each, so you can tell a correct result from a broken one.
- **Do not accept "tests pass" from an agent that could not run them.** Ask it to state explicitly what it did not execute.
- **If an implementer cannot run the code, the cycle has three steps: it writes, you run, you return the literal output** with the exit code, not a summary. It cannot see what it cannot run, so expect the first delivery to have failures.
- **Running in your environment is not running in the user's.** Operating system, interpreter version, and network access can differ; ask agents to state where they ran each check.
- **A red check that tells the truth beats a green one that hides it.** Forbid weakening a test just to make it pass. If a fix requires weakening a check, it should not apply the fix and should report it instead.
- **Explicitly authorize what its role restricts**, such as network access or running commands, and nothing more.
- **Do not put the conclusion in the question.** "Confirm that X is correct" invites a signature, not a review. Ask neutrally.
- **Plan for degradation.** Tell the agent what to deliver if it cannot finish: a structured partial result (what was done, what was not, why) rather than silence or plausible filler.
- **Manage the input budget.** If the material does not fit, you decide what is included and what is referenced by path, and you record what was left out. Do not let the context be truncated silently.

## When the result arrives

- Check that the destination file exists and has a plausible size. If the agent could not write it, copy its chat answer into the file and label it as a transcription, not the original report.
- Read what the agent declared as unverified, assumed, or pending first. It is what gets lost in summaries and what costs most to ignore.
- If it left contradictions for the user, do not resolve them yourself. Present them with options and costs.
- Record the resulting decision, not the whole report.

When you create or change an agent definition, run two or three smoke checks before relying on it: it loads, it has only the tools you intended, and it writes only its named destination.

## Template

~~~text
From: <sender>. Brief <n> of <m>. Project: <name>.
Destination: <full path to one new file>. Do not overwrite it if it exists; stop and report.
Chat: at most <N> lines: verdict, top findings, what you could not verify.
Read first, completely: <state file>.
Originals: <path> (specification) | <path> (reference only) | <path> (open only if needed).
Already produced on this topic: <list with date, size, title>.
Unverified by me: <statements marked as hypotheses>.
Do not read or change: <paths or systems>.
Binding decisions: <constraints from others>.
Deliver: 1. ... 2. ... 3. What else in your work could be false for the same reason? 4. What lies outside the range your checks cover?
If you cannot finish: deliver a structured partial result.
Stop when: <condition>. Do not: <actions>.
~~~
