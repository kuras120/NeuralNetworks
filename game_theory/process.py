import math
import sys
import json
import jsbeautifier

from helper.default_predictor import DefaultPredictor
from resources.resource import Resource


class Process:
    def __init__(self, state_file_name, learning_mode, reset):
        self.__learning_mode = learning_mode
        self.__matrix = []
        self.__q_table = {}
        self.__char = sys.argv[1]
        self.__points = sys.argv[2:4]
        self.__prev_points = sys.argv[4:6]
        if len(sys.argv[6:]) % 2 != 0 or math.sqrt(int(len(sys.argv[6:]) / 2)) % 2 != 0:
            raise ArithmeticError()
        self.__length = int(len(sys.argv[6:]) / 2)
        self.__hash = ''.join(sys.argv[6:6 + self.__length])
        self.__prev_hash = ''.join(sys.argv[6 + self.__length:])
        self.__predictor = DefaultPredictor(self.__char, int(math.sqrt(self.__length)), state_file_name)
        self.__init(sys.argv[6:6 + self.__length], state_file_name, reset)

    def __init(self, matrix, state_file_name, reset):
        length = int(math.sqrt(self.__length))
        for i in range(0, len(matrix), length):
            sub_list = matrix[i:i + length]
            self.__matrix.append(sub_list)
        if reset:
            self.__q_table[self.__hash] = []
            for i in range(len(self.__matrix)):
                self.__q_table[self.__hash].append([])
                for j in range(len(self.__matrix[i])):
                    self.__q_table[self.__hash][i].append(0)
            with Resource.load(state_file_name, 'w') as state:
                json.dump(self.__q_table, state)
                Resource.log(state.name)
        else:
            with Resource.load(state_file_name, 'r') as state:
                self.__q_table = json.load(state)

    def move(self):
        self.__predictor.evaluate(self.__prev_hash, self.__hash)

    def values(self):
        print('Current state matrix:', file=sys.stderr)
        for elem in self.__matrix:
            print('     ', elem, file=sys.stderr)
        print('Points:', file=sys.stderr)
        print('     Player: ' + self.__points[0], file=sys.stderr)
        print('     AI: ' + self.__points[1], file=sys.stderr)
        print('Available states:', file=sys.stderr)
        print(jsbeautifier.beautify(json.dumps(self.__q_table), jsbeautifier.default_options()), file=sys.stderr)


if __name__ == '__main__':
    process = Process('state.json', True, True)
    process.values()
    process.move()
