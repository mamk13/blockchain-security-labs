"""Release-pair gate based on CWA-2026-006; not an upstream patch."""

import re
from dataclasses import dataclass


class Rejected(ValueError):
    pass


@dataclass(frozen=True)
class RuntimeManifest:
    wasmd: str
    wasmvm_declared: str
    wasmvm_loaded: str


PATCHED_LINES = {
    (0, 70): ((0, 70, 4), (3, 0, 8)),
    (0, 61): ((0, 61, 15), (3, 0, 8)),
    (0, 60): ((0, 60, 9), (2, 3, 5)),
    (0, 54): ((0, 54, 10), (2, 2, 9)),
}


def parse_version(value):
    if type(value) is not str or re.fullmatch(r"v?\d+\.\d+\.\d+", value) is None:
        raise Rejected("version must be a stable three-part release")
    return tuple(int(part) for part in value.removeprefix("v").split("."))


class VulnerableMinimumGate:
    """Incorrectly compares every release line with one global minimum."""

    @staticmethod
    def accepts(manifest):
        return (
            parse_version(manifest.wasmd) >= (0, 54, 10)
            and parse_version(manifest.wasmvm_declared) >= (2, 2, 9)
        )


class ReleasePairGate:
    """Checks the maintained line, patched pair, and loaded-library parity."""

    @staticmethod
    def verify(manifest):
        if type(manifest) is not RuntimeManifest:
            raise Rejected("invalid manifest")
        wasmd = parse_version(manifest.wasmd)
        declared = parse_version(manifest.wasmvm_declared)
        loaded = parse_version(manifest.wasmvm_loaded)
        required = PATCHED_LINES.get(wasmd[:2])
        if required is None:
            raise Rejected("release line is not in this advisory matrix")
        minimum_wasmd, minimum_wasmvm = required
        if wasmd < minimum_wasmd:
            raise Rejected("affected wasmd version")
        if declared[:2] != minimum_wasmvm[:2] or declared < minimum_wasmvm:
            raise Rejected("wasmvm does not match the patched release line")
        if loaded != declared:
            raise Rejected("loaded wasmvm differs from the declared dependency")
        return True
