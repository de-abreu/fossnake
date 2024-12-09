from app.constants import BOUNDARIES
from app.enums import Direction
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.position import Position
from pygame import Rect
from random import randint as rand


class Board:
    def __init__(self, side: int, tile_size: int) -> None:
        self.tiles = [[None for _ in range(side)] for _ in range(side)]
        self.tile_size = tile_size

    @property
    def size(self):
        return len(self.tiles)

    def distance(self, a: Position, b: Position) -> int:
        """
        The Manhattan distance between two point 'a' and 'b' on the board, considering the board's wrap around.
        """

        x = abs(a.x - b.x)
        y = abs(a.y - b.y)
        return min(x, self.size - x) + min(y, self.size - y)

    def offset(self, pos: Position, dir: Direction, dist: int) -> Position:
        """
        Offset a position towards one of the cardinal directions, wrapping around the edges
        """
        match dir:
            case Direction.UP:
                return Position(pos.x, (pos.y - dist + self.size) % self.size)
            case Direction.LEFT:
                return Position((pos.x - dist + self.size) % self.size, pos.y)
            case Direction.DOWN:
                return Position(pos.x, (pos.y + dist + self.size) % self.size)
            case _:
                return Position((pos.x + dist + self.size) % self.size, pos.y)

    def random(self, margin: int) -> Position:
        """
        A random position on the board, considering a margin from its edges.
        """

        x = rand(margin, self.size - (margin + 1))
        y = rand(margin, self.size - (margin + 1))
        return Position(x, y)

    def getTile(self, pos: Position) -> Snake | Fruit | None:
        return self.tiles[pos.y][pos.x]

    def setTile(self, pos: Position, obj) -> None:
        self.tiles[pos.y][pos.x] = obj

    def getTileRect(self, pos: Position) -> Rect:
        return Rect(
            (
                pos.x * self.tile_size + BOUNDARIES,
                pos.y * self.tile_size + BOUNDARIES,
            ),
            (self.tile_size,) * 2,
        )
