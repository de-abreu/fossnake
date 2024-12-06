from abc import abstractmethod, ABC
from app.board import Board
from pygame import Surface


class GameObject(ABC):
    """
    Base class for all game objects. Objects that are, on a given position: placed on a shared board, printed to a surface, and eventually moved (updated).
    """

    def __init__(self, board: Board) -> None:
        self.board = board

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        pass
