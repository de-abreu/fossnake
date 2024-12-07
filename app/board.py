from app.constants import BOUNDARIES
from app.enums import Direction, Tile
from app.position import Position
from pygame import Rect
from random import randint as rand


class Board:
    def __init__(self, rows: int, columns: int, tile_size: int) -> None:
        self.rows = rows
        self.columns = columns
        self.tile_size = tile_size
        self.tiles = [[Tile.EMPTY for _ in range(columns)] for _ in range(rows)]

    def distance(self, a: Position, b: Position) -> int:
        """
        The Manhattan distance between two point 'a' and 'b' on the board, considering the board's wrap around.
        """

        x = abs(a.x - b.x)
        y = abs(a.y - b.y)
        return min(x, self.columns - x) + min(y, self.rows - y)

    def move(self, pos: Position, dir: Direction, dist: int) -> Position:
        """
        Move in one of the cardinal directions, wrapping around the edges
        """
        match dir:
            case Direction.UP:
                return Position(pos.x, (pos.y - dist + self.rows) % self.rows)
            case Direction.LEFT:
                return Position((pos.x - dist + self.columns) % self.columns, pos.y)
            case Direction.DOWN:
                return Position(pos.x, (pos.y + dist + self.rows) % self.rows)
            case _:
                return Position((pos.x + dist + self.columns) % self.columns, pos.y)

    def random(self, margin: int) -> Position:
        """
        A random position on the board, considering a margin from its edges.
        """

        x = rand(margin, self.columns - (margin + 1))
        y = rand(margin, self.rows - (margin + 1))
        return Position(x, y)

    def getTile(self, pos: Position) -> Tile:
        return self.tiles[pos.y][pos.x]

    def getTileRect(self, pos: Position) -> Rect:
        return Rect(
            pos.x * self.tile_size + BOUNDARIES,
            pos.y * self.tile_size + BOUNDARIES,
            self.tile_size,
            self.tile_size,
        )

    def setTile(self, pos: Position, tile: Tile) -> None:
        self.tiles[pos.y][pos.x] = tile
