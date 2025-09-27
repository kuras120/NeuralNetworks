import json

from games_theory.helper.generator import Generator
from games_theory.resources.resource import Resource


class DefaultPredictor:
    def __init__(self, qtable_file_name, state_file_name, learning_rate=0.1, discount_rate=0.5):
        self.__learning_rate = learning_rate
        self.__discount_rate = discount_rate
        self.__qtable_file_name = qtable_file_name
        self.__state_file_name = state_file_name

    # (to_evaluate - previous, points - current)
    def evaluate(self, to_evaluate, points):
        next_states = self.generate_neighbour_states(to_evaluate['state'])
        with Resource.load(self.__qtable_file_name, 'r') as qtable_file:
            q_table: dict = json.load(qtable_file)
        for state in next_states:
            # TODO not needed, cuz max future reward will be 0
            # if state not in q_table.keys():
            #     Generator.generate_empty_state(q_table, state, self.__length)
            if state in q_table.keys():
                pass
        # TODO move coords
        # q_table[to_evaluate['state']][row][col] =

    def predict(self):
        pass

    @staticmethod
    def generate_neighbour_states(key: str):
        neighbours = []
        for i in range(len(key)):
            copy = list(key)
            if key[i] == 'N':
                copy[i] = 'O'
                neighbours.append(''.join(copy))
        return neighbours
