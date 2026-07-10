import json
import tempfile
import unittest
from pathlib import Path

from games_theory.resources.resource import Resource
from games_theory.src.config_repository import ConfigRepository


class ConfigRepositoryTestCase(unittest.TestCase):
    def test_load_reads_game_config_from_resource_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / Resource.DATA_DIR
            data_dir.mkdir(parents=True)
            config = {
                "learning": True,
                "board-size": 3,
                "ai-char": "O",
            }
            (data_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")

            self.assertEqual(config, ConfigRepository(tmpdir).load())


if __name__ == "__main__":
    unittest.main()
