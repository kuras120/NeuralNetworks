from typing import List

from games_theory.src.domain_types import State


class Generator:
    @staticmethod
    def generate_neighbour_states(key: State, mark_value: str = '-1') -> List[State]:
        neighbours: List[State] = []
        cells = key.split(',')
        for i, value in enumerate(cells):
            if value == '0':
                copy = list(cells)
                copy[i] = mark_value
                neighbours.append(','.join(copy))
        return neighbours
