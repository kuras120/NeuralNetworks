import random
from typing import List, Mapping, Optional, Sequence

from games_theory.src.domain_types import State


class ActionSelector:
    def __init__(self, rng: Optional[random.Random] = None) -> None:
        self._random = rng or random.Random()

    def choose(
        self,
        neighbours: Sequence[State],
        scored_states: Mapping[State, float],
    ) -> Optional[State]:
        if not neighbours:
            return None

        values = [scored_states.get(state, 0) for state in neighbours]
        weights = self._weights_from_values(values)
        if not weights:
            return self._random.choice(neighbours)
        return self._random.choices(neighbours, weights=weights, k=1)[0]

    @staticmethod
    def _weights_from_values(values: Sequence[float]) -> Optional[List[float]]:
        if not values:
            return None

        max_value = max(values)
        min_value = min(values)
        if max_value == min_value:
            return None
        if min_value <= 0:
            shift = abs(min_value) + 1
            return [value + shift for value in values]
        return list(values)
