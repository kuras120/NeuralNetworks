from typing import Optional

from games_theory.resources.resource import Resource
from games_theory.src.domain_types import LastMove


class StateStorage:
    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path

    def persist(self, last_move: Optional[LastMove]) -> None:
        Resource.save('state.json', 'last_move', last_move, self.resources_path)

    def clear_last_move(self) -> None:
        Resource.save('state.json', 'last_move', None, self.resources_path)
