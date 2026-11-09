"""Per-payer residual attribution. Outcomes are trusted side-effect-free fixtures."""
from copy import deepcopy
def settle(state, payer, incoming, attempts, *, vulnerable=False):
    if not isinstance(payer, str) or not payer or type(incoming) is not int or incoming < 0:
        raise ValueError("bad payment")
    if any(type(n) is not int or n < 0 or type(ok) is not bool for n, ok in attempts):
        raise ValueError("bad attempt")
    if sum(n for n, _ in attempts) > incoming:
        raise ValueError("allocation exceeds payment")
    s = deepcopy(state)
    s["assets"] += incoming
    spent = sum(n for n, ok in attempts if ok)
    s["assets"] -= spent
    s["paid"] += spent
    residual = s["assets"] if vulnerable else incoming - spent
    s["refunds"][payer] = s["refunds"].get(payer, 0) + residual
    state.update(s)
def withdraw(state, payer):
    amount = state["refunds"].get(payer, 0)
    if amount > state["assets"]:
        raise ValueError("insolvent")
    state["refunds"][payer] = 0
    state["assets"] -= amount
    return amount
