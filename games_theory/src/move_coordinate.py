from typing import List, Tuple

from games_theory.src.domain_types import MoveCoordinatePayload, State


class MoveCoordinate:
    def __init__(self, board_size: int) -> None:
        if board_size <= 0:
            raise ValueError("Board size must be greater than zero")
        self._board_size = board_size

    def derive(self, current_state: State, selected_state: State) -> MoveCoordinatePayload:
        current_cells, selected_cells = self._validated_cells(current_state, selected_state)
        changed_index = self._changed_index(current_cells, selected_cells)
        self._validate_move(current_cells, selected_cells, changed_index)
        return self._to_payload(changed_index)

    def _validated_cells(
        self,
        current_state: State,
        selected_state: State,
    ) -> Tuple[List[str], List[str]]:
        current_cells = current_state.split(',')
        selected_cells = selected_state.split(',')
        expected_cells = self._board_size * self._board_size
        if len(current_cells) != expected_cells or len(selected_cells) != expected_cells:
            raise ValueError("States must contain board-size * board-size cells")
        return current_cells, selected_cells

    @staticmethod
    def _changed_index(current_cells: List[str], selected_cells: List[str]) -> int:
        changed_indices = [
            index
            for index, (current, selected) in enumerate(zip(current_cells, selected_cells))
            if current != selected
        ]
        if len(changed_indices) != 1:
            raise ValueError("Selected state must differ from current state by exactly one cell")
        return changed_indices[0]

    @staticmethod
    def _validate_move(
        current_cells: List[str],
        selected_cells: List[str],
        index: int,
    ) -> None:
        if current_cells[index] != '0' or selected_cells[index] != '-1':
            raise ValueError("Selected move must place the bot marker in an empty cell")

    def _to_payload(self, index: int) -> MoveCoordinatePayload:
        return {'x': index % self._board_size, 'y': index // self._board_size}
