import random
from typing import Optional

from games_theory.src.domain_types import LastMove, Points, State, StatePayload
from games_theory.src.predictor import (
    ActionSelector,
    QTableRepository,
    StateStorage,
    ScoreTracker,
    RewardPolicy,
)


class DefaultPredictor:
    def __init__(
        self,
        resources_path: str,
        learning_rate: float = 0.1,
        discount_rate: float = 0.5,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.resources_path = resources_path
        self.__learning_rate = learning_rate
        self.__discount_rate = discount_rate
        self._qtable_repository = QTableRepository(resources_path)
        self._state_storage = StateStorage(resources_path)
        self._action_selector = ActionSelector(rng)

    def evaluate(
        self,
        to_evaluate: Optional[StatePayload],
        current_points: Points,
        current_state: State,
    ) -> None:
        if not to_evaluate:
            return

        last_move = to_evaluate.get('last_move')
        if not last_move:
            return

        previous_state = last_move.get('from')
        action_state = last_move.get('to')
        prev_advantage = last_move.get('advantage')
        if prev_advantage is None:
            previous_points = last_move.get('points')
            if previous_points is None:
                return
            prev_advantage = ScoreTracker.advantage(previous_points)
        if not previous_state or not action_state:
            return

        q_table = self._qtable_repository.load()
        self._qtable_repository.ensure_state_entry(q_table, previous_state)
        self._qtable_repository.ensure_state_entry(q_table, current_state)

        reward = RewardPolicy.calculate(prev_advantage, current_points)
        old_value = q_table[previous_state].get(action_state, 0)
        max_future_reward = self._qtable_repository.max_future_reward(q_table, current_state)
        updated_value = old_value + self.__learning_rate * (
            reward + self.__discount_rate * max_future_reward - old_value
        )
        q_table[previous_state][action_state] = updated_value

        self._qtable_repository.save(q_table)
        self._state_storage.clear_last_move()

    def predict(self, current_state: State, current_points: Points) -> Optional[State]:
        q_table = self._qtable_repository.load()
        neighbours = self._qtable_repository.ensure_state_entry(q_table, current_state)

        if not neighbours:
            self._state_storage.persist(None)
            self._qtable_repository.save(q_table)
            return None

        scored_states = q_table[current_state]
        chosen_state = self._action_selector.choose(neighbours, scored_states)
        if chosen_state is None:
            return None

        last_move: LastMove = {
            'from': current_state,
            'to': chosen_state,
            'points': ScoreTracker.normalize(current_points),
            'advantage': ScoreTracker.advantage(current_points),
        }
        self._state_storage.persist(last_move)
        self._qtable_repository.save(q_table)
        return chosen_state
