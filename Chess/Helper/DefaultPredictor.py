import os
import json

from Chess.Helper.Generator import Generator


class DefaultPredictor:
    def __init__(self, state_file_path, learning_rate=0.1, discount_rate=0.5):
        self.__learning_rate = learning_rate
        self.__discount_rate = discount_rate
        self.__absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), state_file_path)

    def evaluate(self, current_state, q_values):
        next_states = self.__generate_neighbour_states(current_state)
        q_table = {}
        with open(self.__absolute_path, 'r') as state:
            q_table: dict = json.load(state)
        for state in next_states:
            if state not in q_table.keys():
                Generator.generate_empty_state(q_table, state, q_values)

        pass

    def predict(self):
        pass

    @staticmethod
    def __generate_neighbour_states(key):
        neighbours = []
        for i in range(len(key)):
            copy = ''.join(key)
            if key[i] == 'N':
                copy[i] = 'O'
                neighbours.append(copy)
        return neighbours
