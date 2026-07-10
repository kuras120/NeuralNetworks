import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

sys.modules.setdefault(
    "jsbeautifier",
    types.SimpleNamespace(beautify=lambda value, _: value, default_options=lambda: None),
)

from games_theory.process import Process
from games_theory.resources.resource import Resource


class ProcessTestCase(unittest.TestCase):
    def test_move_does_not_persist_learning_state_when_learning_is_disabled(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / Resource.DATA_DIR
            data_dir.mkdir(parents=True)
            qtable_path = data_dir / "qtable.json"
            state_path = data_dir / "state.json"
            qtable_path.write_text(json.dumps({}), encoding="utf-8")
            state_path.write_text(json.dumps({"last_move": None}), encoding="utf-8")

            process = Process(
                player_points="0",
                ai_points="0",
                cells=["N", "N", "N", "N"],
                resources_path=tmpdir,
                length=2,
                learning=False,
                ai_char="X",
            )

            process.move()

            self.assertEqual({}, json.loads(qtable_path.read_text(encoding="utf-8")))
            self.assertEqual({"last_move": None}, json.loads(state_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
