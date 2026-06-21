from typing import Optional

from games_theory.src.domain_types import NormalizedPoints, Points


class ScoreTracker:
    @staticmethod
    def normalize(points: Optional[Points]) -> NormalizedPoints:
        if points is None:
            return ['0', '0']
        return [str(points[0]), str(points[1])]

    @staticmethod
    def advantage(points: Points) -> int:
        player, ai = map(int, ScoreTracker.normalize(points))
        return ai - player
