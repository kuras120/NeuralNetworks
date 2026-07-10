from typing import Iterable

from games_theory.src.domain_types import State


class StateEncoder:
    EMPTY: str = '0'
    HUMAN: str = '1'
    AI: str = '-1'

    def __init__(self, ai_char: str = 'O', empty_char: str = 'N') -> None:
        self._ai_char = ai_char
        self._empty_char = empty_char

    def encode_cells(self, cells: Iterable[str]) -> State:
        return ','.join(self._encode_cell(cell) for cell in cells)

    def _encode_cell(self, cell: str) -> str:
        if cell == self._empty_char:
            return self.EMPTY
        if cell == self._ai_char:
            return self.AI
        return self.HUMAN
