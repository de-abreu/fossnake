from abc import abstractmethod, ABC
from app.board import Board
from app.constants import BOUNDARIES
from app.position import Position
from pygame import Surface, Rect


class GameObject(ABC):
    """
    Base class for all game objects. Objects that are, on a given position: placed on a shared board, printed to a surface, and eventually moved (updated).
    """

    def __init__(self, board: Board) -> None:
        self.board = board

    @abstractmethod
    def update(self) -> "GameObject | None":
        pass

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        pass

    def getTileRect(self, pos: Position) -> Rect:
        return Rect(
            (
                pos.x * self.board.tile_size + BOUNDARIES,
                pos.y * self.board.tile_size + BOUNDARIES,
            ),
            (self.board.tile_size,) * 2,
        )
