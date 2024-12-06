from app.board import Board
from app.constants import MAX_LENGTH
from app.enums import Tile, Direction
from app.game_objects.game_object import GameObject
from app.game_objects.segment import Segment
from app.position import Position
import pygame


class Snake(GameObject):
    def __init__(self, board: Board) -> None:
        super().__init__(board)
        self.spawn()

    @property
    def head(self):
        return self.body[0]

    def spawn(self) -> None:
        # Place the snake on the board at a random position where it's head is at least three tiles away from a border.
        initial_pos = self.board.random(3)

        # Set it to move away from the closest border, with body orientation to match
        self.direction = [self.initialDirection(initial_pos)]
        body_orientation = self.direction[0].opposite()

        # Create the initial body segments at an offset position from the head
        self.body = [
            Segment(self.board.move(initial_pos, body_orientation, i)) for i in range(3)
        ]
        self.assignSprites()

        for segment in self.body:
            self.board.setTile(segment.pos, Tile.SNAKE)

    def assignSprites(self) -> None:
        self.head.assignHead(self.direction[0], self.board)
        self.body[1].assignNeck(self.head.pos, self.body[2].pos, self.board)
        self.body[-1].assignTail(self.body[-2].pos, self.board)

    def move(self) -> Tile:
        # fetch the tile type at the position the snake is moving to
        next_pos = self.board.move(self.head.pos, self.direction[0], 1)
        next_tile = self.board.getTile(next_pos)

        # If moving onto itself, interrupt
        if next_tile != Tile.SNAKE and next_tile != Tile.EATEN:
            # Update snake and board accordingly
            self.body = [Segment(next_pos)] + self.body
            if next_tile == Tile.FRUIT:
                self.board.setTile(self.head.pos, Tile.EATEN)
            else:
                self.board.setTile(self.head.pos, Tile.SNAKE)
            if len(self.body) == MAX_LENGTH or next_tile != Tile.FRUIT:
                self.board.setTile(self.body.pop().pos, Tile.EMPTY)
            self.assignSprites()

            # Consume direction buffer
            if len(self.direction) > 1:
                del self.direction[0]
        return next_tile

    def initialDirection(self, pos: Position) -> Direction:
        if pos.x < self.board.columns // 2:
            if pos.y < self.board.rows // 2:
                if pos.x < pos.y:
                    return Direction.RIGHT
                return Direction.DOWN
            if pos.x < self.board.rows - pos.y:
                return Direction.RIGHT
            return Direction.UP
        if pos.y < self.board.rows // 2:
            if self.board.columns - pos.x < pos.y:
                return Direction.LEFT
            return Direction.DOWN
        if self.board.columns - pos.x < self.board.rows - pos.y:
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
        for segment in self.body:
            surface.blit(segment.sprite, self.board.getTileRect(segment.pos))
