from enum import Enum, auto


class GameState(Enum):
    RUNNING, PAUSED, GAMEOVER = (auto() for _ in range(3))


class Difficulty(Enum):
    EASY, NORMAL, HARD = (auto() for _ in range(3))

    @classmethod
    def str_list(cls) -> list[str]:
        return [member.name for member in cls]


class Direction(Enum):
    UP, LEFT, DOWN, RIGHT = (auto() for _ in range(4))

    def opposite(self):
        dirs = list(Direction)
        return dirs[(dirs.index(self) + 2) % len(dirs)]


class Loop(Enum):
    MENU, SETUP, GAME, QUIT = (auto() for _ in range(4))
