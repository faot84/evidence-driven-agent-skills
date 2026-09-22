# Expected analysis

## Reproduction

The test `test_summary_uses_every_paid_order` fails with `ZeroDivisionError` in `average_paid_amount`. It fails the same way on every run, because the input is a fixed file.

## Symptom versus cause

The crash happens at the division because `paid` is empty. The division is where the program stopped, not where it broke. The cause is earlier: `paid_orders` compares `status` with `"PAID"` exactly, while the data contains `"paid"` and `"Paid "` (with a trailing space).

A falsifiable hypothesis must predict something the crash does not already imply. For example: "if the exact status comparison is the cause, then comparing a stripped, upper-cased status selects orders 1 and 2, whose amounts sum to 100.0". Checking that prediction supports the cause before any fix is made.

## Fix

Normalize the status before comparing, for example `order["status"].strip().upper() == "PAID"`. Both tests then pass, including the one with an upper-case status, and the summary reports `50.00`.

Guarding the division with `if paid else 0.0` is a symptom fix. The crash disappears, the report says `0.00`, and the test still fails.

## Negative control

Reverting the normalization brings back the `ZeroDivisionError`. A report without this step has not shown that the identified cause is the cause.

## Open questions a careful report may raise

- Whether other status values, such as `"Paid."`, should count. The data does not say.
- Whether an empty list of paid orders should produce an error or a defined message. The current behavior is still a crash, which is outside the reported defect.
