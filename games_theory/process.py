import sys
import json
from typing import List, Sequence

import jsbeautifier

from games_theory.src.config_repository import ConfigRepository
from games_theory.src.default_predictor import DefaultPredictor
from games_theory.src.domain_types import PointValue, QTable
from games_theory.src.predictor import StateEncoder, QTableRepository, StateRepository


class Process:
    def __init__(
        self,
        player_points: PointValue,
        ai_points: PointValue,
        cells: Sequence[str],
        resources_path: str,
        length: int,
        learning: bool,
        ai_char: str,
    ) -> None:
        self.__current_points: List[str] = [str(player_points), str(ai_points)]
        self.__cells: List[str] = list(cells)
        self.__length = length
        self.__learning = learning
        self.__hash = StateEncoder(ai_char=ai_char).encode_cells(self.__cells)
        self.__predictor = DefaultPredictor(resources_path)
        self.__qtable_repository = QTableRepository(resources_path)
        self.__state_repository = StateRepository(resources_path)

    def move(self) -> None:
        if self.__learning:
            self.__predictor.evaluate(self.__state_repository.load(), self.__current_points, self.__hash)
            self.__predictor.predict(self.__hash, self.__current_points)
        else:
            self.__predictor.predict_readonly(self.__hash)

    def print_values(self) -> None:
        print(self.__format_values(self.__qtable_repository.load()), file=sys.stderr)

    def __format_values(self, q_table: QTable) -> str:
        rows = [
            str(self.__cells[i:i + self.__length])
            for i in range(0, len(self.__cells), self.__length)
        ]
        pretty_qtable = jsbeautifier.beautify(json.dumps(q_table), jsbeautifier.default_options())

        return "\n".join([
            "Current state matrix:",
            *[f"     {row}" for row in rows],
            "Points:",
            f"     Player: {self.__current_points[0]}",
            f"     AI: {self.__current_points[1]}",
            "Available states:",
            pretty_qtable.rstrip(),
        ])


def cli_main() -> None:
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

    conf = ConfigRepository(args.config).load()
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
        length=length,
        learning=conf['learning'],
        ai_char=conf['ai-char'],
    )
    process.move()
    process.print_values()
