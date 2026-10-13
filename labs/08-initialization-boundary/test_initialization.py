import unittest
from initialization import Implementation, TwoStepFactory, AtomicFactory, Rejected


class NoOpImplementation(Implementation):
    def initialize(self, storage, owner, direct=False):
        pass


class WrongOwnerImplementation(Implementation):
    def initialize(self, storage, owner, direct=False):
        storage.owner, storage.initialized = 'eve', True


class InitializationTests(unittest.TestCase):
    def test_negative_control_attacker_initializes_first(self):
        p = TwoStepFactory().deploy('p', Implementation())
        p.initialize('eve')
        with self.assertRaises(Rejected):
            p.initialize('alice')
        self.assertEqual('eve', p.storage.owner)

    def test_guarded_deployment(self):
        f = AtomicFactory()
        p = f.deploy_initialized('p', Implementation(), 'alice')
        self.assertIs(p, f.instances['p'])
        self.assertEqual('alice', p.storage.owner)

    def test_post_deployment_takeover_rejected(self):
        p = AtomicFactory().deploy_initialized('p', Implementation(), 'alice')
        with self.assertRaises(Rejected):
            p.initialize('eve')
        self.assertEqual('alice', p.storage.owner)

    def test_locked_implementation_does_not_lock_proxy_storage(self):
        i = Implementation()
        with self.assertRaises(Rejected):
            i.initialize(i.storage, 'eve', direct=True)
        p = AtomicFactory().deploy_initialized('p', i, 'alice')
        self.assertFalse(i.storage.initialized)
        self.assertTrue(p.storage.initialized)

    def test_unlocked_implementation_rejected(self):
        f = AtomicFactory()
        with self.assertRaises(Rejected):
            f.deploy_initialized('p', Implementation(locked=False), 'alice')
        self.assertEqual({}, f.instances)

    def test_empty_code_apparent_success_negative_control(self):
        p = TwoStepFactory().deploy('p', Implementation(has_code=False))
        p.initialize('alice')
        self.assertFalse(p.storage.initialized)

    def test_empty_code_rejected(self):
        f = AtomicFactory()
        with self.assertRaises(Rejected):
            f.deploy_initialized('p', Implementation(has_code=False), 'alice')
        self.assertEqual({}, f.instances)

    def test_noop_call_fails_postcondition(self):
        f = AtomicFactory()
        with self.assertRaises(Rejected):
            f.deploy_initialized('p', NoOpImplementation(), 'alice')
        self.assertEqual({}, f.instances)

    def test_wrong_owner_fails_postcondition(self):
        f = AtomicFactory()
        with self.assertRaises(Rejected):
            f.deploy_initialized('p', WrongOwnerImplementation(), 'alice')
        self.assertEqual({}, f.instances)

    def test_invalid_owner_does_not_register_candidate(self):
        for owner in ('', ' ', None, 0):
            f = AtomicFactory()
            with self.assertRaises(Rejected):
                f.deploy_initialized('p', Implementation(), owner)
            self.assertEqual({}, f.instances)

    def test_duplicate_preserves_original(self):
        f = AtomicFactory()
        first = f.deploy_initialized('p', Implementation(), 'alice')
        with self.assertRaises(Rejected):
            f.deploy_initialized('p', Implementation(), 'eve')
        self.assertIs(first, f.instances['p'])
        self.assertEqual('alice', first.storage.owner)

    def test_unsafe_entrypoint_disabled(self):
        with self.assertRaises(Rejected):
            AtomicFactory().deploy('p', Implementation())


if __name__ == '__main__':
    unittest.main()
