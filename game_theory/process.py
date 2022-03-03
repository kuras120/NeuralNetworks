import os
import sys
import json
import jsbeautifier

from helper.default_predictor import DefaultPredictor


class Process:
    def __init__(self, state_file_path, learning_mode, reset):
        self.__learning_mode = learning_mode
        self.__matrix = []
        self.__q_table = {}
        self.__char = sys.argv[1]
        self.__length = int(sys.argv[2])
        self.__points = sys.argv[-4:-2]
        self.__prev_points = sys.argv[-2:]
        self.__hash = ''.join(sys.argv[3:3 + (self.__length * self.__length)])
        self.__prev_hash = ''.join(sys.argv[3 + (self.__length * self.__length):-4])
        self.__predictor = DefaultPredictor(self.__char, self.__length, state_file_path)
        print(state_file_path)
        self.__init(sys.argv[3:3 + (self.__length * self.__length)], state_file_path, reset)

    def __init(self, matrix, state_file_path, reset):
        for i in range(0, len(matrix), self.__length):
            sub_list = matrix[i:i + self.__length]
            self.__matrix.append(sub_list)
        absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), state_file_path)
        if reset:
            self.__q_table[self.__hash] = []
            for i in range(len(self.__matrix)):
                self.__q_table[self.__hash].append([])
                for j in range(len(self.__matrix[i])):
                    self.__q_table[self.__hash][i].append(0)
            with open(absolute_path, 'w') as state:
                json.dump(self.__q_table, state)
            print('State saved in ' + absolute_path, file=sys.stderr)
        else:
            with open(absolute_path, 'r') as state:
                self.__q_table = json.load(state)

    def move(self):
        self.__predictor.evaluate(self.__prev_hash, self.__hash)
        pass

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
    process = Process('data/state.json', True, True)
    process.values()
    process.move()
