---
name: certify-delivery
description: Decide whether a specific software delivery meets predefined acceptance criteria using version-matched evidence. Use for a formal acceptance or release gate; issue one verdict and a status for each mandatory criterion. Do not use for open-ended diagnosis or routine testing during implementation.
---

# Certify a delivery

## Purpose

Make a bounded acceptance decision about one identified delivery. Keep the criteria fixed while evaluating it. Certification does not authorize modifying the delivery, waiving criteria, or deploying it.

## Required inputs

Identify the delivery and version, acceptance criteria, mandatory versus optional status, relevant environment, and available evidence. If an essential input is missing, state the gap and return NOT EVALUABLE rather than inventing a criterion or assuming success.

## Workflow

1. Match every mandatory criterion to one status: MET, NOT MET, NOT DEMONSTRATED, or NOT APPLICABLE with a reason.
2. Distinguish evidence supplied by others, evidence directly inspected, and behavior independently reproduced. Verify that each result applies to the version being certified.
3. Inspect the production path required by the criterion. Code presence, compilation, or a test with a related name is not enough if the criterion requires an integrated outcome.
4. Before approving, try to disprove the strongest provisional conclusion with one targeted contradiction, counterexample, or missing integration. Correct the result if the check changes it.
5. Perform only non-destructive checks within the authorized scope. If a decisive check would change state or require unavailable access, record it as NOT DEMONSTRATED or make the delivery NOT EVALUABLE as appropriate.

NOT DEMONSTRATED means the evidence is insufficient; it does not assert a product failure. It still prevents approval of a mandatory criterion. NOT MET requires evidence of a failure.

## Exactly one verdict

- CERTIFIED: every mandatory criterion is demonstrated and no material contradiction remains.
- CERTIFIED WITH RESERVATIONS: every mandatory criterion is demonstrated; stated limitations are non-blocking.
- NOT CERTIFIED: at least one mandatory criterion is contradicted, a material failure is demonstrated, or a mandatory criterion remains NOT DEMONSTRATED after the review.
- NOT EVALUABLE: essential criteria, delivery identity, access, or evidence are missing so a responsible decision cannot be made.

Do not use reservations to hide a failed or unproven mandatory criterion. Do not silently fix a problem to obtain a favorable verdict.

## Report

Give the delivery identity and scope, one verdict, a compact criterion-by-criterion status, the checks and evidence behind each material status, limitations, and the minimum action needed to close any gap. State whether the decision relied on prior evidence or independently reproduced results.
