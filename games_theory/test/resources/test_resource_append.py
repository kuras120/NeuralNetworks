import json
import os
import tempfile
import unittest

from games_theory.resources.resource import Resource


class TestResourceAppend(unittest.TestCase):
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
