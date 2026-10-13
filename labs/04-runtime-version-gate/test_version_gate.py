import unittest

from version_gate import (
    Rejected,
    ReleasePairGate,
    RuntimeManifest,
    VulnerableMinimumGate,
    parse_version,
)


class RuntimeVersionGateTests(unittest.TestCase):
    def test_vulnerable_global_minimum_accepts_affected_pair(self):
        manifest = RuntimeManifest("0.70.3", "3.0.7", "3.0.7")
        self.assertTrue(VulnerableMinimumGate.accepts(manifest))

    def test_all_advisory_patch_pairs_are_accepted(self):
        pairs = (
            ("0.70.4", "3.0.8"),
            ("0.61.15", "3.0.8"),
            ("0.60.9", "2.3.5"),
            ("0.54.10", "2.2.9"),
        )
        for wasmd, wasmvm in pairs:
            with self.subTest(wasmd=wasmd, wasmvm=wasmvm):
                self.assertTrue(
                    ReleasePairGate.verify(RuntimeManifest(wasmd, wasmvm, wasmvm))
                )

    def test_affected_versions_are_rejected(self):
        pairs = (
            ("0.70.3", "3.0.7"),
            ("0.61.14", "3.0.7"),
            ("0.60.8", "2.3.4"),
            ("0.54.9", "2.2.8"),
        )
        for wasmd, wasmvm in pairs:
            with self.subTest(wasmd=wasmd, wasmvm=wasmvm):
                with self.assertRaises(Rejected):
                    ReleasePairGate.verify(RuntimeManifest(wasmd, wasmvm, wasmvm))

    def test_loaded_library_must_equal_declared_dependency(self):
        with self.assertRaisesRegex(Rejected, "loaded wasmvm"):
            ReleasePairGate.verify(RuntimeManifest("0.70.4", "3.0.8", "3.0.7"))

    def test_wrong_wasmvm_release_line_is_rejected(self):
        with self.assertRaisesRegex(Rejected, "release line"):
            ReleasePairGate.verify(RuntimeManifest("0.70.4", "2.3.5", "2.3.5"))

    def test_later_patch_in_same_lines_is_accepted(self):
        self.assertTrue(
            ReleasePairGate.verify(RuntimeManifest("0.70.5", "3.0.9", "3.0.9"))
        )

    def test_unknown_wasmd_line_is_not_assumed_safe(self):
        with self.assertRaisesRegex(Rejected, "advisory matrix"):
            ReleasePairGate.verify(RuntimeManifest("0.71.0", "3.1.0", "3.1.0"))

    def test_prerelease_and_short_versions_are_rejected(self):
        for value in ("3.0", "3.0.8-rc1", "latest", ""):
            with self.subTest(value=value):
                with self.assertRaises(Rejected):
                    parse_version(value)

    def test_v_prefix_is_accepted(self):
        self.assertEqual(parse_version("v3.0.8"), (3, 0, 8))

    def test_invalid_manifest_type_is_rejected(self):
        with self.assertRaisesRegex(Rejected, "invalid manifest"):
            ReleasePairGate.verify(("0.70.4", "3.0.8", "3.0.8"))


if __name__ == "__main__":
    unittest.main()
