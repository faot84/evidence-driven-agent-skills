# Misleading error exercise

This fictional sales report crashes with `ZeroDivisionError`. The traceback points at the division, but the division is not where the defect is. Copy this directory to a disposable workspace, leaving out expected-analysis.md (the answer key), then ask an assistant with reproduce-before-fixing and claim-evidence-table installed:

> The sales summary test crashes. Find the cause, fix it, and report what you verified.

Run the tests with:

    python -B -m unittest discover -s . -p "test_*.py" -v

A good result names the actual cause, shows that the hypothesis predicted something checkable, and includes a negative control: revert the fix and confirm that the failure returns.

Compare the result with [expected analysis](expected-analysis.md). The exercise is a manual agent exercise, not a benchmark.
