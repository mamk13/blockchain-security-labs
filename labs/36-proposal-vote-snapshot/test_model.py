import unittest
from model import Proposal, VulnerableCurrent, WeightFixture


class Tests(unittest.TestCase):
    def fixture(self):
        return WeightFixture({("alice", 5): 100, ("bob", 5): 0,
                              ("alice", 8): 0, ("bob", 8): 100},
                             {"alice": 100, "bob": 0})

    def test_reused_current_weight_negative_control(self):
        source = self.fixture(); p = VulnerableCurrent(5)
        p.cast("alice", source, 6)
        source.current = {"alice": 0, "bob": 100}
        p.cast("bob", source, 7)
        self.assertEqual(p.total, 200)

    def test_snapshot_stops_reuse(self):
        source = self.fixture(); p = Proposal(5)
        p.cast("alice", source, 6)
        source.current = {"alice": 0, "bob": 100}
        with self.assertRaises(ValueError): p.cast("bob", source, 7)
        self.assertEqual((p.total, p.voted), (100, {"alice"}))

    def test_later_current_changes_do_not_change_weight(self):
        source = self.fixture(); source.current["alice"] = 0
        self.assertEqual(Proposal(5).cast("alice", source, 9), 100)

    def test_new_proposal_uses_its_own_snapshot(self):
        source = self.fixture()
        self.assertEqual(Proposal(8).cast("bob", source, 9), 100)

    def test_same_voter_rejected_without_tally_change(self):
        p = Proposal(5); source = self.fixture(); p.cast("alice", source, 6)
        with self.assertRaises(ValueError): p.cast("alice", source, 7)
        self.assertEqual((p.total, p.voted), (100, {"alice"}))

    def test_current_snapshot_not_closed(self):
        p = Proposal(5)
        for now in (4, 5, True):
            with self.assertRaises(ValueError): p.cast("alice", self.fixture(), now)
        self.assertEqual((p.total, p.voted), (0, set()))
        self.assertEqual(p.cast("alice", self.fixture(), 6), 100)

    def test_clock_units_must_match(self):
        p = Proposal(5, clock_mode="timestamp")
        with self.assertRaises(ValueError): p.cast("alice", self.fixture(), 6)
        self.assertEqual(p.total, 0)

    def test_missing_source_rejection_then_retry(self):
        p = Proposal(5)
        with self.assertRaises(KeyError):
            p.cast("alice", WeightFixture({}, {}), 6)
        self.assertEqual((p.total, p.voted), (0, set()))
        self.assertEqual(p.cast("alice", self.fixture(), 6), 100)

    def test_invalid_weight_rejected(self):
        for weight in (-1, 0, True, 1 << 256):
            p = Proposal(5)
            with self.assertRaises(ValueError):
                p.cast("alice", WeightFixture({("alice", 5): weight}, {}), 6)
            self.assertEqual((p.total, p.voted), (0, set()))

    def test_tally_overflow_preserves(self):
        source = WeightFixture({("alice", 5): (1 << 256)-1, ("bob", 5): 1}, {})
        p = Proposal(5); p.cast("alice", source, 6)
        with self.assertRaises(ValueError): p.cast("bob", source, 6)
        self.assertEqual((p.total, p.voted), ((1 << 256)-1, {"alice"}))
