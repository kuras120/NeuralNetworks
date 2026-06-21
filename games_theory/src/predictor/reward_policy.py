from .score_tracker import ScoreTracker


class RewardPolicy:
    @staticmethod
    def calculate(previous_advantage, current_points):
        current_advantage = ScoreTracker.advantage(current_points)
        return current_advantage - previous_advantage
