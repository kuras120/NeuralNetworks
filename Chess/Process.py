import os
import sys
import json
import jsbeautifier

class Process:
    def __init__(self, reset_on_new, learning_mode, state_file_path):
        self.__matrix = []
        self.__q_table = {}
        self.__points = sys.argv[-2:]
        self.__length = int(sys.argv[1])
        self.__reset_on_new = reset_on_new
        self.__learning_mode = learning_mode
        self.__hash = ''.join(sys.argv[2:-2])
        self.init(sys.argv[2:-2], state_file_path.replace('\\', '/'))

    def init(self, matrix, state_file_path):
        init_state = True
        for i in range(0, len(matrix), self.__length):
            sub_list = matrix[i:i + self.__length]
            self.__matrix.append(sub_list)
            if sub_list.count(sub_list[0]) != len(sub_list):
                init_state = False
        absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), state_file_path)
        if init_state and self.__reset_on_new:
            self.__q_table[self.__hash] = []
            for i in range(len(self.__matrix)):
                self.__q_table[self.__hash].append([])
                for j in range(len(self.__matrix[i])):
                    self.__q_table[self.__hash][i].append(0)
            with open(absolute_path, 'w') as state:
                json.dump(self.__q_table, state)
            print('State saved in ' + absolute_path)
        else:
            with open(absolute_path, 'r') as state:
                self.__q_table = json.load(state)

    def values(self):
        print('Macierz stanu:')
        for elem in self.__matrix:
            print('     ', elem)
        print('Punkty:')
        print('     Gracz: ' + self.__points[0])
        print('     AI: ' + self.__points[1])
        print('Stan:')
        print(jsbeautifier.beautify(json.dumps(self.__q_table), jsbeautifier.default_options()))


if __name__ == '__main__':
    process = Process(True, True, 'Data/state.json')
    process.values()
