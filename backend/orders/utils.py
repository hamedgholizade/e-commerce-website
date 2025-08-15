from decimal import Decimal, InvalidOperation


def safe_decimal(value):
    try:
        return Decimal(str(value))
    except (TypeError, InvalidOperation):
        return 0.0
    