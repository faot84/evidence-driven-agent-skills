---
name: audit-delivery
description: Investigate a software delivery by comparing its requirements and claims with implementation, tests, and evidence. Use for an open-ended review or diagnosis; report findings and verification limits without changing the delivery. Do not use for a formal acceptance decision against fixed criteria.
---

# Audit a delivery

## Purpose

Determine what a software delivery actually supports. Treat source code, tests, logs, and reports as evidence with different strengths. The review is read-only unless the user separately authorizes an action that changes state.

## Workflow

1. Establish the question, delivery identity or version, scope, governing requirements, and exclusions. If the version is unknown, say so before relying on version-specific evidence.
2. Inspect only relevant files and existing results. Record meaningful absences. If a command could write caches, logs, snapshots, or external state, do not run it as part of a read-only review.
3. Map each material claim or requirement to expected evidence, observed evidence, and current status.
4. Trace the relevant path from input through validation, transformation, dependencies, output, and consumer. Look for missing integration, divergent branches, swallowed errors, and behavior that can appear successful after a failure.
5. Assess tests by the behavior they reach and assert. A test name, pass count, mock, or report does not prove an integration that it bypasses. Check whether a result belongs to the delivery version under review.
6. Search for a counterexample to the provisional conclusion. Revisit only findings changed by that search.
7. Report confirmed observations, reasoned inferences, and unverified questions separately. Anchor each material finding to a precise file, line, result, or reproducible observation.

## Findings

For each finding, state the condition, evidence, affected criterion or claim, practical impact, and severity. Calibrate severity to actual impact and scope. Do not label every missing test a product defect; distinguish broken behavior from insufficient proof.

Finish with the reviewed scope, findings ordered by impact, evidence gaps, and focused next checks or fixes. If no issue was found, describe what was inspected without claiming that the whole delivery is defect-free.

An audit is not a formal acceptance gate. Use certify-delivery when a particular version must be judged against predefined criteria.
