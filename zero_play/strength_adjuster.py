import math


class StrengthAdjuster:
    def __init__(self,
                 strength: int,
                 game_count: int = 0,
                 last_score: int = 0,
                 streak_length: int = 1):
        self.strength = strength
        self.game_count = game_count
        self.last_score = last_score
        self.streak_length = streak_length

    def record_score(self, score: int):
        self.game_count += 1
        if score == self.last_score:
            self.streak_length += 1
        else:
            self.last_score = score
            self.streak_length = 1
        self.strength = math.ceil(
            self.strength * (1 + score*self.streak_length/(self.game_count+1)))
