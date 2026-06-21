import json
import random
import tempfile
import unittest
from pathlib import Path

from games_theory.src.default_predictor import DefaultPredictor
from games_theory.resources.resource import Resource


class DefaultPredictorTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.resource_path = self.temp_dir.name

        self.data_dir = Path(self.resource_path) / Resource.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.data_dir / 'state.json'
        self.qtable_path = self.data_dir / 'qtable.json'

        self._write_json(self.state_path, {"last_move": None})
        self._write_json(self.qtable_path, {})

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_predict_persists_last_move_and_generates_neighbours(self):
        predictor = DefaultPredictor(self.resource_path, rng=random.Random(0))

        next_state = predictor.predict("0,0,0,0", ["0", "0"])

        self.assertEqual("0,0,0,-1", next_state)
        q_table = self._read_json(self.qtable_path)
        self.assertIn("0,0,0,0", q_table)
        self.assertEqual(
            {
                "-1,0,0,0",
                "0,-1,0,0",
                "0,0,-1,0",
                "0,0,0,-1",
            },
            set(q_table["0,0,0,0"].keys())
        )
        state_payload = self._read_json(self.state_path)
        self.assertEqual(
            {
                "from": "0,0,0,0",
                "to": "0,0,0,-1",
                "points": ["0", "0"],
                "advantage": 0,
            },
            state_payload["last_move"]
        )

    def test_evaluate_updates_q_table_with_reward_and_future_gain(self):
        q_table = {
            "0,0,0,0": {
                "-1,0,0,0": 0.2,
                "0,-1,0,0": 0.0,
            },
            "0,1,-1,0": {
                "0,1,-1,-1": 0.4,
                "-1,1,-1,0": 0.1,
            }
        }
        to_evaluate = {
            "last_move": {
                "from": "0,0,0,0",
                "to": "-1,0,0,0",
                "points": ["1", "0"],
                "advantage": -1,
            }
        }
        self._write_json(self.qtable_path, q_table)
        self._write_json(self.state_path, to_evaluate)
        predictor = DefaultPredictor(self.resource_path, learning_rate=0.1, discount_rate=0.5, rng=random.Random(1))

        predictor.evaluate(to_evaluate, ["1", "2"], "0,1,-1,0")

        updated_q_table = self._read_json(self.qtable_path)
        self.assertAlmostEqual(0.4, updated_q_table["0,0,0,0"]["-1,0,0,0"])
        state_payload = self._read_json(self.state_path)
        self.assertIsNone(state_payload.get("last_move"))

    def _read_json(self, path: Path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_json(self, path: Path, payload):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file)


if __name__ == "__main__":
    unittest.main()
