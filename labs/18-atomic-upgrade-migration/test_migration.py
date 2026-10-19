import unittest
from copy import deepcopy
from migration import Proxy, SplitUpgrade, migrate_v2


class MigrationTests(unittest.TestCase):
    def test_negative_control_split_upgrade(self):
        p = SplitUpgrade()
        def fail(state): raise ValueError('failure')
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, fail)
        self.assertEqual((p.state['implementation'], p.state['version']), ('v2', 1))

    def test_success_preserves_all_balances(self):
        p = Proxy(); before = deepcopy(p.state)
        p.upgrade('governance', 'v2', 2, migrate_v2)
        self.assertEqual(p.state, dict(before, implementation='v2', version=2, limit=100))

    def test_partial_write_failure_rolls_back(self):
        p = Proxy(); before = deepcopy(p.state)
        def fail(state):
            state['balances']['alice'] = 0
            state['limit'] = 99
            raise ValueError('failure')
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, fail)
        self.assertEqual(p.state, before)

    def test_failed_attempt_can_retry(self):
        p = Proxy()
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, lambda s: None)
        p.upgrade('governance', 'v2', 2, migrate_v2)
        self.assertEqual(p.state['version'], 2)

    def test_repeat_success_rejected_without_mutation(self):
        p = Proxy(); p.upgrade('governance', 'v2', 2, migrate_v2); before = deepcopy(p.state)
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, migrate_v2)
        self.assertEqual(p.state, before)

    def test_unauthorized_callback_never_runs(self):
        p = Proxy(); called = []
        with self.assertRaises(ValueError): p.upgrade('eve', 'v2', 2, lambda s: called.append(True))
        self.assertEqual(called, [])
        self.assertEqual(p.state['implementation'], 'v1')

    def test_wrong_target_rejected(self):
        for impl, version in [('v3', 2), ('v2', 1), ('v2', 3)]:
            p = Proxy(); before = deepcopy(p.state)
            with self.assertRaises(ValueError): p.upgrade('governance', impl, version, migrate_v2)
            self.assertEqual(p.state, before)

    def test_successful_return_with_wrong_state_rejected(self):
        mutations = [('owner', 'eve'), ('total', 101), ('limit', 99), ('version', 1), ('implementation', 'v3')]
        for key, value in mutations:
            p = Proxy(); before = deepcopy(p.state)
            def wrong(state):
                migrate_v2(state); state[key] = value
            with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, wrong)
            self.assertEqual(p.state, before)

    def test_conserved_total_does_not_allow_reassigned_balances(self):
        p = Proxy(); before = deepcopy(p.state)
        def steal(state):
            migrate_v2(state); state['balances'] = {'alice': 0, 'bob': 100}
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, steal)
        self.assertEqual(p.state, before)

    def test_model_does_not_rollback_external_side_effect(self):
        p = Proxy(); external = []
        def fail(state):
            external.append('outside modeled ledger'); raise ValueError()
        with self.assertRaises(ValueError): p.upgrade('governance', 'v2', 2, fail)
        self.assertEqual(external, ['outside modeled ledger'])
        self.assertEqual(p.state['version'], 1)

if __name__ == '__main__': unittest.main()
