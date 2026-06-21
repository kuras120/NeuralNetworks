class Generator:
    @staticmethod
    def generate_neighbour_states(key: str, mark_value: str = '-1'):
        neighbours = []
        cells = key.split(',')
        for i, value in enumerate(cells):
            if value == '0':
                copy = list(cells)
                copy[i] = mark_value
                neighbours.append(','.join(copy))
        return neighbours
