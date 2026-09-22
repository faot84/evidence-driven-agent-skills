# Recommended agent roles

All skills work with one assistant. Add a specialist only when the task can be separated and its output could change the decision. A small code review or local edit does not need an agent team.

| Role | When it helps | Boundaries | Useful output |
| --- | --- | --- | --- |
| Evidence reviewer | A delivery needs an independent audit or acceptance decision. | Read-only; does not repair the version being judged or relax criteria. | Claim-to-evidence map, findings, verdict limits. |
| Test verifier | A decisive behavior must be reproduced, including an integration or failure path. | Runs only checks authorized for the environment; records commands, version, inputs, and observed results. | Reproducible evidence and untested boundaries. |
| Domain reviewer | A criterion depends on specialist knowledge such as security, operations, data integrity, statistics, accessibility, or regulation. | Reviews only the assigned domain; does not turn a narrow finding into a project-wide verdict. | Domain-specific evidence and risks. |
| Implementer | The owner authorizes a fix after the review. | Owns specified files or modules; preserves unrelated changes; checks the affected behavior. | Change and verification record for a new version. |
| Backup verifier | An authorized edit affects valuable existing files and independent recovery evidence matters. | Checks the exact source, destination, hashes, and restore path; never treats a copy command alone as proof. | Backup receipt and any unresolved recovery risk. |

## Suggested setups

- **Small review:** one assistant applies audit-delivery or certify-delivery directly.
- **Medium delivery:** one read-only evidence reviewer plus a test verifier if dynamic proof is needed. The main assistant integrates their evidence and owns the final report.
- **High-impact delivery:** add the domain reviewer whose expertise matches the criterion at risk. Keep the implementer separate from the acceptance decision.
- **Autonomous local change:** one implementer can use verified-backup-before-edit and non-destructive-autonomy. If an independent verifier adds value, give that reviewer the backup receipts and exact changed-file list; do not give two agents simultaneous write ownership of the same files.

Avoid sending several agents to inspect the same files without a distinct question. Assign one owner for each implementation block. Share the exact delivery version, criteria, permitted paths, and stopping condition with every agent. Distinguish a specialist's finding from the final acceptance decision.

## Portable mission prompts

**Evidence reviewer:** “Review this delivery read-only against the attached requirements. Trace the critical path and give precise evidence for each material finding. State what you could not verify. Do not modify the delivery.”

**Test verifier:** “Reproduce only the assigned behavior in the authorized environment. Record the version, command, inputs, observed output, and whether the check creates artifacts or changes state. Return evidence; do not decide the entire release.”

**Domain reviewer:** “Evaluate criterion X within your specialty. Identify the applicable contract, evidence, counterexample, and uncertainty. Return a narrow finding to the lead reviewer.”

**Implementer:** “Fix finding X in the assigned files. Preserve unrelated changes, run focused checks, and report the new version or file state. Do not certify your own fix.”

**Backup verifier:** “Inspect the backup receipt for each edited existing file. Check source scope, pre-edit copy, size and hash evidence, destination safety, and whether a restore path is credible. Report only what the evidence supports.”

Claude Code supports project subagents as Markdown files with YAML frontmatter in .claude/agents/. Codex uses its own agent configuration. Apart from the adversarial reviewer below, these prompts are role recommendations, not preconfigured agents. See [Claude Code subagent guidance](https://code.claude.com/docs/en/sub-agents).

## Included subagent: adversarial reviewer

[agents/adversarial-reviewer.md](../agents/adversarial-reviewer.md) is a ready-to-install Claude Code subagent. It differs from the evidence reviewer above: it does not map every claim to evidence or certify against fixed criteria. It attacks finished work and reports only defects, ordered by severity, with a one-line deliverability verdict and a list of what it could not verify. That verdict is advice to the author, not a formal acceptance decision; use certify-delivery for that. When it recommends a statistics reviewer, use the domain reviewer role above.

Use it before delivering substantial work, and always when the author changed position after an objection; it checks whether the change rests on new evidence or on accommodation. Give it a destination file for its report, as described in [brief-a-subagent](../skills/brief-a-subagent/SKILL.md), so a long report is not lost.

Its frontmatter grants Bash so it can run checks and Write so it can save its report. Neither is limited to particular paths or commands by the tool list: the instructions to write only one file and avoid state-changing commands are behavioral. Remove those tools, or add permission rules, if you need enforcement.
