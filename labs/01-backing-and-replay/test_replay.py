import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from replay_model import Event, VulnerableLedger, GuardedLedger

E = Event("bitcoin-mainnet", "a" * 64, 0)  # synthetic, not historical

class ReplayTests(unittest.TestCase):
    def test_vulnerable_duplicate_inflates_aggregate(self):
        ledger = VulnerableLedger()
        self.assertEqual(ledger.consume(E, 100, 1), 99)
        self.assertEqual(ledger.consume(E, 100, 1), 99)
        self.assertEqual(ledger.issued, 198)

    def test_duplicate_rejected_without_state_change(self):
        ledger = GuardedLedger()
        ledger.consume(E, 100, 1)
        with self.assertRaises(ValueError):
            ledger.consume(E, 100, 1)
        self.assertEqual(ledger.issued, 99)
        self.assertEqual(ledger.consumed, {E})

    def test_invalid_amount_does_not_consume_event(self):
        ledger = GuardedLedger()
        with self.assertRaises(ValueError):
            ledger.consume(E, 100, -1)
        self.assertEqual(ledger.consumed, set())
        self.assertEqual(ledger.issued, 0)
        self.assertEqual(ledger.consume(E, 100, 1), 99)

    def test_other_output_is_distinct(self):
        ledger = GuardedLedger()
        for output in (0, 1):
            ledger.consume(Event(E.network, E.txid, output), 100, 1)
        self.assertEqual(ledger.issued, 198)

    def test_canonical_event_validation(self):
        ledger = GuardedLedger()
        for event in (Event(E.network, "A"*64, 0), Event(E.network, E.txid, True),
                      Event("unknown", E.txid, 0), Event(E.network, E.txid, -1)):
            with self.subTest(event=event), self.assertRaises(ValueError):
                ledger.consume(event, 100, 1)
        self.assertEqual(ledger.issued, 0)

    def test_concurrent_duplicate_single_winner(self):
        ledger = GuardedLedger()
        barrier = Barrier(8)
        def worker(_):
            barrier.wait(timeout=10)
            try:
                return ledger.consume(E, 100, 1)
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(worker, range(8)))
        self.assertEqual(results.count(99), 1)
        self.assertEqual(results.count(None), 7)
        self.assertEqual(ledger.issued, 99)

if __name__ == "__main__":
    unittest.main(verbosity=2)
