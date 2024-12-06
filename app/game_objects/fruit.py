from app.board import Board
from app.enums import Tile
from app.position import Position
from app.game_objects.game_object import GameObject
import pygame


class Fruit(GameObject):
    def __init__(self, board: Board, snake_pos: Position) -> None:
        super().__init__(board)
        self.spawn(snake_pos)

    def spawn(self, pos: Position) -> None:
        """
        From a given set of random locations, find one which is the farthest from Position pos and place the fruit there.
        """
        b = self.board
        sample = []
        while len(sample) < 3:
            pos = b.random(0)
            if b.getTile(pos) == Tile.EMPTY:
                sample.append(pos)

        self.pos = sample[0]
        for i in range(1, len(sample)):
            if b.distance(sample[i], pos) > b.distance(self.pos, pos):
                self.pos = sample[i]
        b.setTile(self.pos, Tile.FRUIT)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface, pygame.Color("#aa0000"), self.board.getTileRect(self.pos)
        )
