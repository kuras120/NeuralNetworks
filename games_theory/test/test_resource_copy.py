import tempfile
import unittest
from importlib import resources
from pathlib import Path

from games_theory.resources.resource import Resource


class TestResourceCopyDefaults(unittest.TestCase):
    def setUp(self):
        # packaged defaults location (read-only)
        self.pkg_base = resources.files("games_theory.resources") / "data"
        self.default_files = ("config.json", "qtable.json", "state.json")

    def _read_packaged(self, name):
        with resources.as_file(self.pkg_base / name) as p:
            return Path(p).read_text(encoding="utf-8")

    def test_copy_defaults_to_tempdir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Resource.copy_defaults(tmpdir)

            for name in self.default_files:
                dst = Path(tmpdir) / "data" / name
                self.assertTrue(dst.exists(), f"{name} should be copied")
                self.assertEqual(
                    dst.read_text(encoding="utf-8"),
                    self._read_packaged(name),
                    f"{name} content should match packaged default",
                )

    def test_copy_defaults_no_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # First copy
            Resource.copy_defaults(tmpdir)
            # Modify one file
            target = Path(tmpdir) / "data" / "state.json"
            target.write_text('{"modified": true}', encoding="utf-8")

            # Second copy without overwriting
            Resource.copy_defaults(tmpdir, overwrite=False)

            self.assertEqual(
                target.read_text(encoding="utf-8"),
                '{"modified": true}',
                "Existing file should not be overwritten by default",
            )

    def test_copy_defaults_with_overwrite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Resource.copy_defaults(tmpdir)
            target = Path(tmpdir) / "data" / "state.json"
            target.write_text('{"modified": true}', encoding="utf-8")

            Resource.copy_defaults(tmpdir, overwrite=True)

            self.assertEqual(
                target.read_text(encoding="utf-8"),
                self._read_packaged("state.json"),
                "Existing file should be overwritten when overwrite=True",
            )


if __name__ == "__main__":
    unittest.main()
