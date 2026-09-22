"""Fictional sales report used by the misleading-error exercise."""


def paid_orders(orders):
    return [order for order in orders if order["status"] == "PAID"]


def average_paid_amount(orders):
    paid = paid_orders(orders)
    return sum(order["amount"] for order in paid) / len(paid)


def summary(orders):
    return f"Average paid order: {average_paid_amount(orders):.2f}"
