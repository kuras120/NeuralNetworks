import json
import tempfile
import unittest
from importlib import resources
from pathlib import Path

from games_theory.resources.resource import Resource


class TestResourceCopyDefaults(unittest.TestCase):
    def setUp(self):
        self.pkg_base = resources.files("games_theory.resources") / Resource.DATA_DIR
        self.default_files = ["config.json"]
        self.generated_files = ["qtable.json", "state.json"]

    def _read_packaged(self, name):
        with resources.as_file(self.pkg_base / name) as p:
            return Path(p).read_text(encoding="utf-8")

    def test_copy_defaults_to_tempdir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Resource.copy_defaults(target_dir=tmpdir)

            for name in self.default_files:
                dst = Path(tmpdir) / Resource.DATA_DIR / name
                self.assertTrue(dst.exists(), f"{name} should be copied")

                content = json.loads(dst.read_text(encoding="utf-8"))
                packaged = json.loads(self._read_packaged(name))

                if name == "config.json":
                    self.assertIn("resource_path", content)
                    self.assertEqual(content["resource_path"], str(Path(tmpdir)))
                    del content["resource_path"]

                self.assertEqual(
                    content,
                    packaged,
                    f"{name} content (excluding dynamic fields) should match packaged default",
                )

            for name in self.generated_files:
                dst = Path(tmpdir) / Resource.DATA_DIR / name
                self.assertTrue(dst.exists(), f"{name} should be generated")

            qtable_path = Path(tmpdir) / Resource.DATA_DIR / "qtable.json"
            qtable = json.loads(qtable_path.read_text(encoding="utf-8"))
            self.assertEqual({}, qtable)

            state_path = Path(tmpdir) / Resource.DATA_DIR / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual({"last_move": None}, state)

    def test_copy_defaults_no_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Resource.copy_defaults(target_dir=tmpdir)
            Resource.save("config.json", "modified", True, tmpdir)
            Resource.copy_defaults(target_dir=tmpdir)

            target = Path(tmpdir) / Resource.DATA_DIR / "config.json"
            content = json.loads(target.read_text(encoding="utf-8"))

            self.assertIn("modified", content, "Modified field should be preserved")

    def test_copy_defaults_with_overwrite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Resource.copy_defaults(target_dir=tmpdir)
            Resource.save("config.json", "modified", True, tmpdir)
            Resource.copy_defaults(target_dir=tmpdir, overwrite=True)

            target = Path(tmpdir) / Resource.DATA_DIR / "config.json"
            content = json.loads(target.read_text(encoding="utf-8"))
            packaged = json.loads(self._read_packaged("config.json"))

            self.assertIn("resource_path", content)
            self.assertEqual(content["resource_path"], str(Path(tmpdir)))
            del content["resource_path"]

            self.assertEqual(
                content,
                packaged,
                "Existing file should be overwritten when overwrite=True",
            )

    def test_throw_error_on_not_existing_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(FileNotFoundError) as cm:
                Resource.copy_defaults(source_package="games_theory.test.resources", target_dir=tmpdir)

            self.assertEqual(str(cm.exception), "config.json not found in resources")


if __name__ == "__main__":
    unittest.main()
