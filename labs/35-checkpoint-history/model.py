"""Trusted-clock checkpoint model. Set is a fixture hook, not public authority."""
from bisect import bisect_right

MAX_TIME = (1 << 48) - 1
MAX_VALUE = (1 << 208) - 1


def bounded(value, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError("out of range")


class History:
    def __init__(self):
        self.now = 0
        self._points = []

    @property
    def points(self):
        return tuple(self._points)

    def advance(self, timepoint):
        bounded(timepoint, MAX_TIME)
        if timepoint < self.now:
            raise ValueError("clock moved backwards")
        self.now = timepoint

    def set(self, value):
        bounded(value, MAX_VALUE)
        point = (self.now, value)
        # Multiple writes at one tick have one final historical value.
        if self._points and self._points[-1][0] == self.now:
            self._points[-1] = point
        else:
            self._points.append(point)

    def _past(self, timepoint):
        bounded(timepoint, MAX_TIME)
        if timepoint >= self.now:
            raise ValueError("not a closed timepoint")

    def past(self, timepoint):
        self._past(timepoint)
        index = bisect_right([p[0] for p in self._points], timepoint)
        return self._points[index-1][1] if index else 0

    def vulnerable_next(self, timepoint):
        self._past(timepoint)
        return next((v for t, v in self._points if t >= timepoint), 0)
