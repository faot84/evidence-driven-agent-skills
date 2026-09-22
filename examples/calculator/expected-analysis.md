# Expected material analysis

This is a guide to the example, not a required response template.

## Audit

- The normal case in R1 is supported by code inspection and the passing valid-discount test.
- R3 is supported by the explicit ValueError branch and the passing negative-subtotal test.
- R2 is contradicted by the clamp in calculator.py: an out-of-range discount is silently converted into a valid one instead of raising ValueError.
- The passing tests do not cover R2, so the fictional team's acceptance claim overstates what its tests demonstrate.
- If tests are not run during the review, report their status as prior or unverified evidence. A test run should identify its command and the checkout it covered.

## Certification

For the current checkout, the expected criterion statuses are R1 MET, R2 NOT MET, and R3 MET, provided the reviewer inspects the implementation and confirms the included tests or reproduces the behavior. The verdict is NOT CERTIFIED because R2 is mandatory and its failure is visible in the delivered code. If access to the implementation or requirements is unavailable, the responsible verdict may instead be NOT EVALUABLE.

The minimum corrective action is to raise ValueError when discount_percent is outside 0 through 100, add boundary tests, and certify the resulting new version. The certification skill itself does not perform that fix.
