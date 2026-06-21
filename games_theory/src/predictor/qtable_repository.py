import json

from games_theory.src.generator import Generator
from games_theory.resources.resource import Resource


class QTableRepository:
    def __init__(self, resources_path):
        self.resources_path = resources_path

    def load(self):
        try:
            with Resource.load('qtable.json', 'r', self.resources_path) as qtable_file:
                return json.load(qtable_file)
        except FileNotFoundError:
            return {}

    def save(self, q_table):
        with Resource.load('qtable.json', 'w', self.resources_path) as qtable_file:
            json.dump(q_table, qtable_file)

    @staticmethod
    def ensure_state_entry(q_table, state):
        neighbours = Generator.generate_neighbour_states(state)
        entry = q_table.setdefault(state, {})
        for neighbour in neighbours:
            entry.setdefault(neighbour, 0)
        return neighbours

    @staticmethod
    def max_future_reward(q_table, state):
        future = q_table.get(state, {})
        return max(future.values()) if future else 0
