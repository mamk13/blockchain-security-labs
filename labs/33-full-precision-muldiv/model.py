"""Integer specification model, not an EVM mulDiv implementation."""
MAX = (1 << 256) - 1


def uint(value):
    if type(value) is not int or not 0 <= value <= MAX:
        raise ValueError("uint256 required")


def inputs(x, y, denominator):
    for value in (x, y, denominator):
        uint(value)
    if denominator == 0:
        raise ValueError("zero denominator")


def vulnerable_wrapped(x, y, denominator):
    inputs(x, y, denominator)
    return ((x * y) & MAX) // denominator


def checked_intermediate(x, y, denominator):
    inputs(x, y, denominator)
    product = x * y
    uint(product)
    return product // denominator


def mul_div(x, y, denominator, *, round_up=False):
    inputs(x, y, denominator)
    if type(round_up) is not bool:
        raise ValueError("explicit rounding flag required")
    # Python's wide intermediate is an oracle, not Solidity implementation code.
    quotient, remainder = divmod(x * y, denominator)
    result = quotient + int(round_up and remainder != 0)
    uint(result)
    return result
