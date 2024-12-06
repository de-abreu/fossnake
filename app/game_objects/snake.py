from app.board import Board
from app.constants import MAX_ENERGY, MAX_LENGTH
from app.enums import Tile, Direction
from app.game_objects.game_object import GameObject
import pygame


class Tail:
    def __init__(
        self,
        pos: Position,
    ) -> None:
        pass


class Snake(GameObject):
    def __init__(self, board: Board) -> None:
        super().__init__(board)
        self.energy = MAX_ENERGY
        self.spawn()

    def spawn(self) -> None:
        self.pos = self.board.random(3)
        self.direction = [self.initialDirection()]
        tail_direction = self.direction[0].opposite()
        self.tail = [
            self.board.move(self.pos, tail_direction, 1),
            self.board.move(self.pos, tail_direction, 2),
        ]
        self.board.setTile(self.pos, Tile.SNAKE)
        for pos in self.tail:
            self.board.setTile(pos, Tile.SNAKE)

    def move(self) -> Tile:
        # Move snake
        self.tail = [self.pos] + self.tail
        self.pos = self.board.move(self.pos, self.direction[0], 1)

        # Consume direction buffer
        if len(self.direction) > 1:
            del self.direction[0]

        # Update board state
        prev_tile = self.board.getTile(self.pos)
        self.board.setTile(self.pos, Tile.SNAKE)

        # Adjust the snake's size upon consuming (or not) a Fruit
        if prev_tile == Tile.FRUIT:
            if len(self.tail) < MAX_LENGTH:
                return prev_tile
        else:
            self.energy -= 1
        self.board.setTile(self.tail.pop(), Tile.EMPTY)
        return prev_tile

    def initialDirection(self) -> Direction:
        if self.pos.x < self.board.columns // 2:
            if self.pos.y < self.board.rows // 2:
                if self.pos.x < self.pos.y:
                    return Direction.RIGHT
                return Direction.DOWN
            if self.pos.x < self.board.rows - self.pos.y:
                return Direction.RIGHT
            return Direction.UP
        if self.pos.y < self.board.rows // 2:
            if self.board.columns - self.pos.x < self.pos.y:
                return Direction.LEFT
            return Direction.DOWN
        if self.board.columns - self.pos.x < self.board.rows - self.pos.y:
            return Direction.LEFT
        return Direction.UP

    def changeDirection(self, keypress: pygame.event.Event) -> None:
        dir = None
        match keypress.key:
            case pygame.K_w:
                dir = Direction.UP
            case pygame.K_a:
                dir = Direction.LEFT
            case pygame.K_s:
                dir = Direction.DOWN
            case pygame.K_d:
                dir = Direction.RIGHT
            case _:
                return
        if self.direction[-1] != dir.opposite():
            self.direction.append(dir)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface, pygame.Color("#00aa00"), self.board.getTileRect(self.pos)
        )
        for pos in self.tail:
            pygame.draw.rect(
                surface, pygame.Color("#00ff00"), self.board.getTileRect(pos)
            )
