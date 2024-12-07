from enum import Enum, auto

class Tile(Enum):
    EMPTY, SNAKE, FRUIT, EATEN = (auto() for _ in range(4))


class Direction(Enum):
    UP, LEFT, DOWN, RIGHT = (auto() for _ in range(4))

    def opposite(self):
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.DOWN:
                return Direction.UP
            case _:
                return Direction.LEFT
