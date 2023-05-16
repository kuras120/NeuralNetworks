import sys
import json
import jsbeautifier

from helper.default_predictor import DefaultPredictor
from resources.resource import Resource


class Process:
    def __init__(self, qtable_file_name='qtable.json', state_file_name='state.json', config_file_name='config.json'):
        self.__matrix = []
        self.__q_table = {}
        self.__to_evaluate = None
        with Resource.load(config_file_name, 'r') as config:
            conf = json.load(config)
            char = conf['ai-char']
            length = conf['board-size']
            learning = conf['learning']
            reset = conf['reset']
        # <table length> + <number arguments> + 1 sys.argv[0]
        if len(sys.argv) != length * length + 3:
            print("Wrong number of arguments. Check config or input parameters.", file=sys.stderr)
            raise SystemError()
        self.__points = sys.argv[1:3]
        self.__hash = ''.join(sys.argv[3:3 + (length * length)])
        self.__predictor = DefaultPredictor(qtable_file_name, state_file_name)
        self.__init(sys.argv[3:3 + (length * length)], length, qtable_file_name, state_file_name, learning, reset)

    def __init(self, matrix, length, qtable_file_name, state_file_name, learning, reset):
        for i in range(0, len(matrix), length):
            sub_list = matrix[i:i + length]
            self.__matrix.append(sub_list)
        if reset:
            self.__q_table[self.__hash] = []
            for i in range(len(self.__matrix)):
                self.__q_table[self.__hash].append([0] * len(self.__matrix[i]))
            with Resource.load(qtable_file_name, 'w') as qtable:
                json.dump(self.__q_table, qtable)
                Resource.log(qtable.name)
            if learning:
                # TODO move coords
                # TODO default initialization of qtable & state
                self.__to_evaluate = {'state': ''.join(['N'] * (length * length)), 'points': self.__points}
                with Resource.load(state_file_name, 'w') as state:
                    json.dump(self.__to_evaluate, state)
                    Resource.log(state.name)
        else:
            with Resource.load(qtable_file_name, 'r') as qtable:
                self.__q_table = json.load(qtable)
            if learning:
                with Resource.load(state_file_name, 'r') as state:
                    self.__to_evaluate = json.load(state)

    def move(self):
        if self.__to_evaluate:
            self.__predictor.evaluate(self.__to_evaluate, self.__points)
        self.__predictor.predict()

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
    process = Process()
    process.values()
    process.move()
