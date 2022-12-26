import json

from helper.generator import Generator
from resources.resource import Resource


class DefaultPredictor:
    def __init__(self, char, length, state_file_name, learning_rate=0.1, discount_rate=0.5):
        self.__char = char
        self.__length = length
        self.__learning_rate = learning_rate
        self.__discount_rate = discount_rate
        self.__state_file_name = state_file_name

    def evaluate(self, previous_state, current_state):
        next_states = self.__generate_neighbour_states(previous_state)
        q_table: dict = {}
        with Resource.load(self.__state_file_name, 'r') as state_file:
            q_table = json.load(state_file)
            for state in next_states:
                if state not in q_table.keys():
                    Generator.generate_empty_state(q_table, state, self.__length)
            last_state = self.__state_differential(current_state, previous_state)
            row, col = int(last_state / self.__length), int(last_state % self.__length)
            # q_table[previous_state][row][col] = q_table[previous_state][row][col]

    def predict(self):
        pass

    def __state_differential(self, key, old_key):
        if len(key) != len(old_key):
            return -1
        for i in range(len(key)):
            if key[i] != old_key[i] and self.__char == key[i]:
                return i
        return -1

    @staticmethod
    def __generate_neighbour_states(key: str):
        neighbours = []
        for i in range(len(key)):
            copy = ''.join(key)
            if key[i] == 'N':
                list(copy)[i] = 'O'
                neighbours.append(copy)
        return neighbours
