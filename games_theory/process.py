import sys
import json
import jsbeautifier

from games_theory.helper.default_predictor import DefaultPredictor
from games_theory.resources.resource import Resource


class Process:
    def __init__(self, player_points, ai_points, cells, resources_path, config):
        self.__matrix = []
        self.__q_table = {}
        self.__to_evaluate = None
        self.resources_path = resources_path
        char = config['ai-char']
        length = config['board-size']
        learning = config['learning']

        self.__points = [str(player_points), str(ai_points)]
        flat_cells = list(cells)
        self.__hash = ''.join(flat_cells)
        self.__predictor = DefaultPredictor(resources_path)
        self._initialize(flat_cells, length, learning)

    def _initialize(self, matrix, length, learning):
        for i in range(0, len(matrix), length):
            sub_list = matrix[i:i + length]
            self.__matrix.append(sub_list)
        with Resource.load('qtable.json', 'r', self.resources_path) as qtable:
            self.__q_table = json.load(qtable)
        if learning:
            with Resource.load('state.json', 'r', self.resources_path) as state:
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
      games-theory <player_points> <ai_points> <cells...> [--config <path>]

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
    parser.add_argument("--config", help="Path to configuration (default: current directory)", default=".")
    parser.add_argument("player_points", help="Player points value")
    parser.add_argument("ai_points", help="AI points value")
    parser.add_argument(
        "cells",
        nargs="+",
        help="Flattened board cells (row-major). Must match board-size*board-size from config.json"
    )
    args = parser.parse_args()

    with Resource.load('config.json', 'r', args.config) as cfg:
        conf = json.load(cfg)
        length = conf['board-size']

    expected_cells = length * length
    if len(args.cells) != expected_cells:
        print("Wrong number of board cells: expected={}, got={} ".format(expected_cells, len(args.cells)),
              "Check your config or input parameters.",
              file=sys.stderr
        )
        sys.exit(2)

    process = Process(
        player_points=args.player_points,
        ai_points=args.ai_points,
        cells=args.cells,
        resources_path=args.config,
        config=conf,
    )
    process.values()
    process.move()
