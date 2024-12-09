from app.enums import Loop, Difficulty


class State:
    """Common variables (and methods to update those) shared by all execution loops"""

    def __init__(
        self, loop: Loop, difficulty: Difficulty, highscore_location: str
    ) -> None:
        self.loop = loop
        self.difficulty = difficulty
        self.difficulties = list(Difficulty)
        self.highscore_location = highscore_location
        self.highscores = [0] * len(self.difficulties)
        try:
            with open(self.highscore_location, "r") as file:
                for i, score in enumerate(file.readlines()):
                    self.highscores[i] = int(score)
        except Exception:
            pass

    def getDifficultyIndex(self):
        return self.difficulties.index(self.difficulty)

    def getHighscore(self) -> int:
        return self.highscores[self.getDifficultyIndex()]

    def changeDifficulty(self, increment: int):
        difficulties = list(Difficulty)
        new_index = (self.getDifficultyIndex() + increment) % len(difficulties)
        self.difficulty = difficulties[new_index]

    def updateHighscore(self, score: int):
        index = self.getDifficultyIndex()
        current = self.highscores[index]
        if score > current:
            self.highscores[index] = score

    def saveHighscore(self):
        with open(self.highscore_location, "w") as file:
            file.write("\n".join(map(str, self.highscores)))
