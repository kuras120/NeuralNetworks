import json
from typing import Optional, cast

from games_theory.resources.resource import Resource
from games_theory.src.domain_types import LastMove, StatePayload


class StateRepository:
    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path

    def load(self) -> StatePayload:
        try:
            with Resource.load('state.json', 'r', self.resources_path) as state_file:
                return cast(StatePayload, json.load(state_file))
        except FileNotFoundError:
            return {'last_move': None}

    def persist(self, last_move: Optional[LastMove]) -> None:
        Resource.save('state.json', 'last_move', last_move, self.resources_path)

    def clear_last_move(self) -> None:
        Resource.save('state.json', 'last_move', None, self.resources_path)
