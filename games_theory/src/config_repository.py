import json
from typing import cast

from games_theory.resources.resource import Resource
from games_theory.src.domain_types import GameConfig


class ConfigRepository:
    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path

    def load(self) -> GameConfig:
        with Resource.load('config.json', 'r', self.resources_path) as config_file:
            return cast(GameConfig, json.load(config_file))
