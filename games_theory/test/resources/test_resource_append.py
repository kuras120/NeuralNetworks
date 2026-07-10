import json
import os
import tempfile
import unittest

from games_theory.resources.resource import Resource


class TestResourceAppend(unittest.TestCase):
    def test_load_uses_current_directory_by_default(self):
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                os.makedirs("data", exist_ok=True)
                with open(os.path.join("data", "config.json"), "w", encoding="utf-8") as f:
                    json.dump({"learning": True}, f)

                with Resource.load("config.json", "r") as f:
                    data = json.load(f)
            finally:
                os.chdir(original_cwd)

        self.assertEqual({"learning": True}, data)

    def test_append_to_new_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            resource_name = "test_new.json"
            key = "key1"
            value = "value1"

            Resource.save(resource_name, key, value, tmpdir)

            file_path = os.path.join(tmpdir, "data", resource_name)
            self.assertTrue(os.path.exists(file_path))

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.assertEqual(data, {key: value})

    def test_append_to_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            resource_name = "test_existing.json"
            initial_data = {"existing_key": "existing_value"}
            
            data_dir = os.path.join(tmpdir, "data")
            os.makedirs(data_dir, exist_ok=True)
            file_path = os.path.join(data_dir, resource_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f)
                
            key = "new_key"
            value = "new_value"
            
            Resource.save(resource_name, key, value, tmpdir)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.assertEqual(data["existing_key"], "existing_value")
                self.assertEqual(data["new_key"], "new_value")


if __name__ == '__main__':
    unittest.main()
