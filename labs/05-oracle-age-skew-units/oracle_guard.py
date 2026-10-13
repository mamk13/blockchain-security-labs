"""Educational oracle-validation model; not a production feed adapter."""

from dataclasses import dataclass


class Rejected(ValueError):
    pass


@dataclass(frozen=True)
class Observation:
    answer: int
    decimals: int
    updated_at: int


def vulnerable_derived_price(base, quote, output_decimals=18):
    """Derives a pair while silently assuming matching units and update times."""
    return base.answer * (10**output_decimals) // quote.answer


def _require_plain_int(name, value, *, minimum=0, maximum=None):
    if type(value) is not int or value < minimum:
        raise Rejected(f"invalid {name}")
    if maximum is not None and value > maximum:
        raise Rejected(f"invalid {name}")


def _validate_observation(observation, *, now, max_age):
    if type(observation) is not Observation:
        raise Rejected("invalid observation")
    _require_plain_int("answer", observation.answer, minimum=1)
    _require_plain_int("decimals", observation.decimals, maximum=18)
    _require_plain_int("updated_at", observation.updated_at, minimum=1)
    if observation.updated_at > now:
        raise Rejected("observation is from the future")
    if now - observation.updated_at > max_age:
        raise Rejected("observation is stale")


def derive_price(
    base,
    quote,
    *,
    now,
    max_age,
    max_skew,
    output_decimals=18,
):
    """Returns base/quote in explicit output units after temporal validation."""
    _require_plain_int("now", now, minimum=1)
    _require_plain_int("max_age", max_age)
    _require_plain_int("max_skew", max_skew)
    _require_plain_int("output_decimals", output_decimals, maximum=18)
    _validate_observation(base, now=now, max_age=max_age)
    _validate_observation(quote, now=now, max_age=max_age)

    # Fresh feeds can still describe materially different market moments.
    if abs(base.updated_at - quote.updated_at) > max_skew:
        raise Rejected("cross-feed update skew exceeds policy")

    numerator = base.answer * (10**quote.decimals) * (10**output_decimals)
    denominator = quote.answer * (10**base.decimals)
    return numerator // denominator
