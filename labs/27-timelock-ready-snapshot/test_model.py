import unittest
from model import Timelock
class Tests(unittest.TestCase):
    def test_negative_control(self):
        t=Timelock(vulnerable=True); t.schedule("a"); t.tick(1); t.set_delay(0); t.execute("a")
        self.assertIn("a",t.done)
    def test_decrease_does_not_accelerate(self):
        t=Timelock(); t.schedule("a"); t.tick(1); t.set_delay(0)
        with self.assertRaises(ValueError): t.execute("a")
        self.assertEqual(t.pending["a"],(0,10))
    def test_increase_does_not_delay_existing(self):
        t=Timelock(); t.schedule("a"); t.set_delay(100); t.tick(10); t.execute("a")
    def test_new_schedule_new_delay(self):
        t=Timelock(); t.schedule("a"); t.tick(1); t.set_delay(0); t.schedule("b"); t.execute("b")
        self.assertIn("a",t.pending)
    def test_boundary_and_replay(self):
        t=Timelock(); t.schedule("a"); t.tick(9)
        with self.assertRaises(ValueError): t.execute("a")
        t.tick(10); t.execute("a")
        with self.assertRaises(ValueError): t.execute("a")
    def test_cancel_reschedule(self):
        t=Timelock(); t.schedule("a"); t.tick(5); t.cancel("a"); t.schedule("a")
        self.assertEqual(t.pending["a"],(5,15))
    def test_duplicate_schedule(self):
        t=Timelock(); t.schedule("a")
        with self.assertRaises(ValueError): t.schedule("a")
        self.assertEqual(t.pending["a"],(0,10))
    def test_bad_clock_and_delay(self):
        t=Timelock(); t.tick(5)
        with self.assertRaises(ValueError): t.tick(4)
        with self.assertRaises(ValueError): t.set_delay(-1)
        self.assertEqual((t.now,t.delay),(5,10))
