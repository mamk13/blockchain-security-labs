"""Checked int256 division/remainder model; no compiler or VM execution."""
MIN = -(1 << 255)
MAX = (1 << 255) - 1


def inputs(a, b):
    for value in (a, b):
        if type(value) is not int or not MIN <= value <= MAX:
            raise ValueError("int256 required")
    if b == 0 or (a == MIN and b == -1):
        raise ValueError("undefined checked quotient")


def vulnerable_floor(a, b):
    inputs(a, b)
    return divmod(a, b)


def trunc_divmod(a, b):
    inputs(a, b)
    magnitude = abs(a) // abs(b)
    quotient = -magnitude if (a < 0) != (b < 0) else magnitude
    # Derive the remainder from the selected quotient, not Python's percent rule.
    return quotient, a - quotient*b


def floor_div(a, b):
    quotient, remainder = trunc_divmod(a, b)
    return quotient - int(remainder != 0 and (a < 0) != (b < 0))
