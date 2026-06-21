class StateEncoder:
    EMPTY = '0'
    HUMAN = '1'
    AI = '-1'

    def __init__(self, ai_char='O', empty_char='N'):
        self._ai_char = ai_char
        self._empty_char = empty_char

    def encode_cells(self, cells):
        return ','.join(self._encode_cell(cell) for cell in cells)

    def _encode_cell(self, cell):
        if cell == self._empty_char:
            return self.EMPTY
        if cell == self._ai_char:
            return self.AI
        return self.HUMAN
