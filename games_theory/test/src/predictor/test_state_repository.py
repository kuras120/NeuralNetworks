import json
import tempfile
import unittest
from pathlib import Path

from games_theory.resources.resource import Resource
from games_theory.src.predictor import StateRepository


class StateRepositoryTestCase(unittest.TestCase):
    def test_load_reads_last_move_payload(self):
        payload = {
            "last_move": {
                "from": "0,0,0,0",
                "to": "-1,0,0,0",
                "points": ["0", "1"],
                "advantage": 1,
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / Resource.DATA_DIR
            data_dir.mkdir(parents=True)
            (data_dir / "state.json").write_text(json.dumps(payload), encoding="utf-8")

            self.assertEqual(payload, StateRepository(tmpdir).load())

    def test_load_returns_empty_last_move_when_state_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual({"last_move": None}, StateRepository(tmpdir).load())


if __name__ == "__main__":
    unittest.main()
