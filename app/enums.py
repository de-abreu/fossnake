from enum import Enum, auto


class Difficulty(Enum):
    EASY, NORMAL, HARD = (auto() for _ in range(3))


class Tile(Enum):
    EMPTY, SNAKE, FRUIT, EATEN, OBSTACLE = (auto() for _ in range(5))


class Direction(Enum):
    UP, LEFT, DOWN, RIGHT = (auto() for _ in range(4))

    def opposite(self):
        dirs = list(Direction)
        return dirs[(dirs.index(self) + 2) % len(dirs)]
