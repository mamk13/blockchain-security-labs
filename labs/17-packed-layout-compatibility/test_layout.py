import unittest
from layout import Field, layout, write, read, compatible, same_slot_count


class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.fields = [Field('balance', 128), Field('debt', 128)]
        self.old = layout(self.fields)

    def test_negative_control_reordered_fields(self):
        new = layout(self.fields[::-1]); slots = {}
        write(slots, self.old['balance'], 100); write(slots, self.old['debt'], 3)
        self.assertTrue(same_slot_count(self.old, new))
        self.assertFalse(compatible(self.old, new))
        self.assertEqual((read(slots, new['balance']), read(slots, new['debt'])), (3, 100))

    def test_append_preserves_existing_values(self):
        new = layout(self.fields + [Field('fee', 16)]); slots = {}
        write(slots, self.old['balance'], 100)
        self.assertTrue(compatible(self.old, new))
        self.assertEqual(read(slots, new['balance']), 100)
        self.assertEqual(read(slots, new['fee']), 0)

    def test_append_into_unused_space(self):
        old = layout([Field('a', 8)])
        new = layout([Field('a', 8), Field('b', 8)])
        self.assertTrue(compatible(old, new))
        self.assertEqual(new['b'], (0, 8, 8))

    def test_width_change_rejected(self):
        new = layout([Field('balance', 64), Field('debt', 128)])
        self.assertFalse(compatible(self.old, new))

    def test_insertion_rejected(self):
        new = layout([Field('flag', 8)] + self.fields)
        self.assertFalse(compatible(self.old, new))

    def test_removal_rejected(self):
        self.assertFalse(compatible(self.old, layout(self.fields[:1])))

    def test_rename_requires_review(self):
        self.assertFalse(compatible(self.old, layout([Field('assets', 128), Field('debt', 128)])))

    def test_field_does_not_straddle_slot(self):
        self.assertEqual(layout([Field('a', 200), Field('b', 64)])['b'], (1, 0, 64))

    def test_update_preserves_neighbor_all_byte_values(self):
        m = layout([Field('a', 8), Field('b', 8)])
        slots = {}; write(slots, m['b'], 231)
        for value in range(256):
            write(slots, m['a'], value)
            self.assertEqual((read(slots, m['a']), read(slots, m['b'])), (value, 231))

    def test_rejected_write_preserves_word(self):
        slots = {0: 123}
        for value in [-1, 256, True, 1.5]:
            with self.assertRaises(ValueError): write(slots, (0, 0, 8), value)
            self.assertEqual(slots, {0: 123})

    def test_bad_field_schema(self):
        for fields in [[Field('a', 7)], [Field('a', 264)], [Field('a', True)], [Field('a', 8), Field('a', 8)]]:
            with self.assertRaises(ValueError): layout(fields)

    def test_uint256_boundary(self):
        m = layout([Field('a', 256), Field('b', 8)])
        self.assertEqual(m['b'], (1, 0, 8))
        slots = {}; write(slots, m['a'], 2**256 - 1)
        self.assertEqual(read(slots, m['a']), 2**256 - 1)

if __name__ == '__main__': unittest.main()
