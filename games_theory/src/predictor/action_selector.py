import random


class ActionSelector:
    def __init__(self, rng=None):
        self._random = rng or random.Random()

    def choose(self, neighbours, scored_states):
        if not neighbours:
            return None

        values = [scored_states.get(state, 0) for state in neighbours]
        weights = self._weights_from_values(values)
        if not weights:
            return self._random.choice(neighbours)
        return self._random.choices(neighbours, weights=weights, k=1)[0]

    @staticmethod
    def _weights_from_values(values):
        if not values:
            return None

        max_value = max(values)
        min_value = min(values)
        if max_value == min_value:
            return None
        if min_value <= 0:
            shift = abs(min_value) + 1
            return [value + shift for value in values]
        return values
