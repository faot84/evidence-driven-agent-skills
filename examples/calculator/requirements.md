# Quote calculator acceptance criteria

Delivery under review: the calculator.py file in the current checkout, together with its tests and this requirements file.

All criteria are mandatory.

| ID | Requirement |
| --- | --- |
| R1 | For a non-negative integer subtotal in cents and an integer discount from 0 through 100 inclusive, quote_total returns subtotal × (100 − discount) // 100. |
| R2 | A discount outside 0 through 100 raises ValueError. |
| R3 | A negative subtotal raises ValueError. |

Only these behaviors are within the example's acceptance scope. A passing test suite is evidence to inspect, not an acceptance criterion by itself.
