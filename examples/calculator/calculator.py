"""Price calculator for the repository's review example."""


def quote_total(subtotal_cents: int, discount_percent: int) -> int:
    if subtotal_cents < 0:
        raise ValueError("subtotal must be non-negative")

    discount_percent = max(0, min(discount_percent, 100))
    return subtotal_cents * (100 - discount_percent) // 100
