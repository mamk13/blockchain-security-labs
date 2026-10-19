"""Restricted flat unsigned-field layout model; not a Solidity layout validator."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    name: str
    bits: int


def layout(fields):
    result, slot, offset = {}, 0, 0
    for field in fields:
        if (not field.name or field.name in result or type(field.bits) is not int
                or field.bits not in range(8, 257, 8)):
            raise ValueError('invalid field')
        if offset + field.bits > 256:
            slot, offset = slot + 1, 0
        result[field.name] = (slot, offset, field.bits)
        offset += field.bits
    return result


def write(slots, location, value):
    slot, offset, bits = location
    if type(value) is not int or not 0 <= value < 2**bits:
        raise ValueError('value out of range')
    mask = (2**bits - 1) << offset
    slots[slot] = (slots.get(slot, 0) & ~mask) | (value << offset)


def read(slots, location):
    slot, offset, bits = location
    return (slots.get(slot, 0) >> offset) & (2**bits - 1)


def compatible(old, new):
    # Names are stable identities in this exercise; renames need explicit review.
    return all(new.get(name) == location for name, location in old.items())


def same_slot_count(old, new):
    """Negative control: total allocation does not preserve field meaning."""
    return max((x[0] for x in old.values()), default=-1) == max((x[0] for x in new.values()), default=-1)
