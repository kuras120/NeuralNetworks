import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

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
            qtable = {"0,0,0,0": {"0,0,0,-1": 1}}
            qtable_path.write_text(json.dumps(qtable), encoding="utf-8")
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

            coordinate = process.move()

            self.assertEqual(qtable, json.loads(qtable_path.read_text(encoding="utf-8")))
            self.assertEqual({"last_move": None}, json.loads(state_path.read_text(encoding="utf-8")))
            self.assertEqual({"x": 1, "y": 1}, coordinate)

    def test_move_returns_none_when_no_legal_move_is_available(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / Resource.DATA_DIR
            data_dir.mkdir(parents=True)
            (data_dir / "qtable.json").write_text("{}", encoding="utf-8")
            (data_dir / "state.json").write_text(
                json.dumps({"last_move": None}),
                encoding="utf-8",
            )
            process = Process(
                player_points="0",
                ai_points="0",
                cells=["X", "O", "X", "O"],
                resources_path=tmpdir,
                length=2,
                learning=False,
                ai_char="X",
            )

            self.assertIsNone(process.move())

    @patch("games_theory.process.ConfigRepository")
    @patch("games_theory.process.Process")
    def test_cli_prints_only_move_json_to_stdout(self, process_class, config_repository_class):
        from contextlib import redirect_stderr, redirect_stdout
        from io import StringIO
        from games_theory.process import cli_main

        config_repository_class.return_value.load.return_value = {
            "board-size": 2,
            "learning": False,
            "ai-char": "X",
        }
        process = MagicMock()
        process.move.return_value = {"x": 1, "y": 0}
        process_class.return_value = process
        stdout = StringIO()
        stderr = StringIO()

        with patch.object(sys, "argv", ["games-theory", "0", "0", "N", "N", "N", "N"]):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                cli_main()

        self.assertEqual({"x": 1, "y": 0}, json.loads(stdout.getvalue()))
        process.print_values.assert_called_once_with()

    @patch("games_theory.process.ConfigRepository")
    @patch("games_theory.process.Process")
    def test_cli_prints_null_when_no_move_is_available(self, process_class, config_repository_class):
        from contextlib import redirect_stdout
        from io import StringIO
        from games_theory.process import cli_main

        config_repository_class.return_value.load.return_value = {
            "board-size": 2,
            "learning": False,
            "ai-char": "X",
        }
        process_class.return_value.move.return_value = None
        stdout = StringIO()

        with patch.object(sys, "argv", ["games-theory", "0", "0", "X", "O", "X", "O"]):
            with redirect_stdout(stdout):
                cli_main()

        self.assertIsNone(json.loads(stdout.getvalue()))


if __name__ == "__main__":
    unittest.main()
