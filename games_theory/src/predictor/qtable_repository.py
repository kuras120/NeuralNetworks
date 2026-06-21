import json
from typing import cast

from games_theory.src.generator import Generator
from games_theory.src.domain_types import QTable, State
from games_theory.resources.resource import Resource


class QTableRepository:
    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path

    def load(self) -> QTable:
        try:
            with Resource.load('qtable.json', 'r', self.resources_path) as qtable_file:
                return cast(QTable, json.load(qtable_file))
        except FileNotFoundError:
            return {}

    def save(self, q_table: QTable) -> None:
        with Resource.load('qtable.json', 'w', self.resources_path) as qtable_file:
            json.dump(q_table, qtable_file)

    @staticmethod
    def ensure_state_entry(q_table: QTable, state: State) -> list[State]:
        neighbours = Generator.generate_neighbour_states(state)
        entry = q_table.setdefault(state, {})
        for neighbour in neighbours:
            entry.setdefault(neighbour, 0)
        return neighbours

    @staticmethod
    def max_future_reward(q_table: QTable, state: State) -> float:
        future = q_table.get(state, {})
        return max(future.values()) if future else 0
