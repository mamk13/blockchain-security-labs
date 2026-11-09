"""Integer value allocation. No EVM, external calls, fees or callbacks."""
from copy import deepcopy
def batch(state, incoming, amounts, *, vulnerable=False):
    if type(incoming) is not int or incoming < 0:
        raise ValueError("bad incoming")
    if any(type(x) is not int or x < 0 for x in amounts):
        raise ValueError("bad allocation")
    next_state = deepcopy(state)
    next_state["assets"] += incoming
    remaining = incoming
    for amount in amounts:
        # Negative control reuses the outer payment as each operation's budget.
        available = incoming if vulnerable else remaining
        if amount > available:
            raise ValueError("batch budget exceeded")
        next_state["credits"] += amount
        remaining -= amount
    state.update(next_state)
    return remaining
