import unittest
from model import History, MAX_TIME, MAX_VALUE


class Tests(unittest.TestCase):
    def history(self):
        h = History()
        h.advance(3); h.set(10)
        h.advance(7); h.set(90)
        h.advance(10)
        return h

    def test_gap_negative_control(self):
        h = self.history()
        self.assertEqual(h.vulnerable_next(5), 90)
        self.assertEqual(h.past(5), 10)

    def test_exact_boundaries(self):
        h = self.history()
        self.assertEqual([h.past(t) for t in (0, 2, 3, 6, 7, 9)],
                         [0, 0, 10, 10, 90, 90])

    def test_same_tick_replaces(self):
        h = History(); h.advance(3); h.set(10); h.set(20)
        self.assertEqual(h.points, ((3, 20),))
        h.advance(4)
        self.assertEqual(h.past(3), 20)

    def test_current_and_future_rejected(self):
        h = self.history()
        for t in (10, 11, MAX_TIME):
            with self.assertRaises(ValueError):
                h.past(t)

    def test_backward_clock_preserves_state(self):
        h = self.history(); before = (h.now, h.points)
        with self.assertRaises(ValueError):
            h.advance(5)
        self.assertEqual((h.now, h.points), before)
        h.set(15); h.advance(11)
        self.assertEqual(h.past(10), 15)

    def test_closed_history_immutable(self):
        h = self.history(); before = [h.past(t) for t in range(10)]
        h.set(400); h.advance(11); h.set(0); h.advance(12)
        self.assertEqual([h.past(t) for t in range(10)], before)

    def test_empty_and_zero_values(self):
        h = History(); h.advance(1)
        self.assertEqual(h.past(0), 0)
        h.set(0); h.advance(2)
        self.assertEqual(h.past(1), 0)

    def test_invalid_inputs_preserve(self):
        h = self.history(); before = (h.now, h.points)
        for v in (-1, MAX_VALUE+1, True):
            with self.assertRaises(ValueError): h.set(v)
        for t in (-1, MAX_TIME+1, True):
            with self.assertRaises(ValueError): h.advance(t)
            with self.assertRaises(ValueError): h.past(t)
        self.assertEqual((h.now, h.points), before)

    def test_lookup_against_linear_history(self):
        h = History()
        for t in range(0, 40, 3):
            h.advance(t); h.set(t*t)
        h.advance(41)
        for query in range(41):
            eligible = [v for t, v in h.points if t <= query]
            self.assertEqual(h.past(query), eligible[-1] if eligible else 0)

    def test_time_and_value_bounds(self):
        h = History(); h.advance(MAX_TIME-1); h.set(MAX_VALUE)
        h.advance(MAX_TIME)
        self.assertEqual(h.past(MAX_TIME-1), MAX_VALUE)
