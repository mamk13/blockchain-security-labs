import unittest
from context import World, Frame, write_42, call_forwarder, delegate_forwarder


class ContextTests(unittest.TestCase):
    def test_direct_call_does_not_test_proxy_storage(self):
        w = World(); w.call('alice', 'implementation', write_42)
        self.assertEqual(w.read('implementation'), 42)
        self.assertEqual(w.read('proxy'), 0)

    def test_negative_control_forwarder(self):
        w = World()
        sender = w.call('alice', 'proxy', lambda w, f: call_forwarder(w, f, 'impl'))
        self.assertEqual((w.read('proxy'), w.read('impl'), sender), (0, 42, 'proxy'))

    def test_delegate_writes_only_proxy(self):
        w = World()
        sender = w.call('alice', 'proxy', lambda w, f: delegate_forwarder(w, f, 'impl'))
        self.assertEqual((w.read('proxy'), w.read('impl'), sender), (42, 0, 'alice'))
        self.assertEqual(w.trace[-1], Frame('impl', 'proxy', 'alice'))

    def test_two_proxies_do_not_share_storage(self):
        w = World()
        for proxy, value in [('p1', 11), ('p2', 22)]:
            w.call('alice', proxy, lambda w, f: w.delegate(f, 'impl', lambda w, g: w.set_value(g, value)))
        self.assertEqual((w.read('p1'), w.read('p2'), w.read('impl')), (11, 22, 0))

    def test_nested_delegate_keeps_owner_and_sender(self):
        w = World()
        w.call('alice', 'p', lambda w, f: w.delegate(f, 'i1', lambda w, g: w.delegate(g, 'i2', write_42)))
        self.assertEqual(w.trace[-1], Frame('i2', 'p', 'alice'))

    def test_call_inside_delegate_changes_context(self):
        w = World()
        w.call('alice', 'p', lambda w, f: w.delegate(f, 'i', lambda w, g: w.call(g.storage, 'other', write_42)))
        self.assertEqual(w.trace[-1], Frame('other', 'other', 'p'))
        self.assertEqual((w.read('p'), w.read('other')), (0, 42))

    def test_static_delegate_rejects_without_writes(self):
        w = World()
        with self.assertRaises(ValueError):
            w.call('alice', 'p', lambda w, f: w.delegate(f, 'i', write_42), static=True)
        self.assertFalse(w.slots)

    def test_child_revert_preserves_parent_state(self):
        w = World()
        def parent(w, f):
            w.set_value(f, 7)
            def child(w, g):
                w.set_value(g, 8); raise ValueError('revert')
            with self.assertRaises(ValueError): w.delegate(f, 'i', child)
        w.call('alice', 'p', parent)
        self.assertEqual(w.read('p'), 7)

    def test_parent_revert_undoes_child_success(self):
        w = World()
        def parent(w, f):
            w.delegate(f, 'i', write_42); raise ValueError('revert')
        with self.assertRaises(ValueError): w.call('alice', 'p', parent)
        self.assertFalse(w.slots)

    def test_implementation_preexisting_value_unchanged(self):
        w = World(); w.slots['i', 'value'] = 99
        w.call('alice', 'p', lambda w, f: w.delegate(f, 'i', write_42))
        self.assertEqual((w.read('p'), w.read('i')), (42, 99))

    def test_uint_bounds(self):
        for value in [-1, 2**256, True, 1.5]:
            w = World()
            with self.assertRaises(ValueError):
                w.call('a', 'p', lambda w, f: w.set_value(f, value))
            self.assertFalse(w.slots)

if __name__ == '__main__': unittest.main()
