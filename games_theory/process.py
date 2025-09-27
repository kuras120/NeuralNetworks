import sys
import json
import jsbeautifier

from games_theory.helper.default_predictor import DefaultPredictor
from games_theory.resources.resource import Resource


class Process:
    def __init__(self, player_points, ai_points, cells,
                 qtable_file_name='qtable.json',
                 state_file_name='state.json',
                 config_file_name='config.json'):
        self.__matrix = []
        self.__q_table = {}
        self.__to_evaluate = None
        with Resource.load(config_file_name, 'r') as config:
            conf = json.load(config)
            char = conf['ai-char']
            length = conf['board-size']
            learning = conf['learning']
            reset = conf['reset']

        self.__points = [str(player_points), str(ai_points)]
        flat_cells = list(cells)
        self.__hash = ''.join(flat_cells)
        init_cells = flat_cells

        self.__predictor = DefaultPredictor(qtable_file_name, state_file_name)
        self._initialize(init_cells, length, qtable_file_name, state_file_name, learning, reset)

    def _initialize(self, matrix, length, qtable_file_name, state_file_name, learning, reset):
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

def cli_main():
    """
    CLI entry point for games-theory.

    Usage:
      games-theory <player_points> <ai_points> <cells...>

    Details:
      - Board cells count must equal board-size * board-size from config.json.
      - Cells should be provided in row-major order.
      - Example for 3x3: games-theory 0 0 N N N N N N N N N
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="games-theory",
        description="Run Q-learning process on a board state."
    )
    parser.add_argument("player_points", help="Player points value")
    parser.add_argument("ai_points", help="AI points value")
    parser.add_argument(
        "cells",
        nargs="+",
        help="Flattened board cells (row-major). Must match board-size*board-size from config.json"
    )
    args = parser.parse_args()

    # Load board size from config to validate cell count
    with Resource.load('config.json', 'r') as cfg:
        conf = json.load(cfg)
        length = conf['board-size']

    expected_cells = length * length
    if len(args.cells) != expected_cells:
        print(
            f"Wrong number of board cells: expected {expected_cells}, got {len(args.cells)}. "
            f"Check your config or input parameters.",
            file=sys.stderr
        )
        sys.exit(2)

    process = Process(player_points=args.player_points, ai_points=args.ai_points, cells=args.cells)
    process.values()
    process.move()
