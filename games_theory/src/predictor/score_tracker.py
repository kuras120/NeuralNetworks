
class ScoreTracker:
    @staticmethod
    def normalize(points):
        if points is None:
            return ['0', '0']
        return [str(points[0]), str(points[1])]

    @staticmethod
    def advantage(points):
        player, ai = map(int, ScoreTracker.normalize(points))
        return ai - player
