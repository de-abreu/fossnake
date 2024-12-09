from app.enums import Direction
from app.dataclasses import Position, Segment
import pygame


class Snake:
    def __init__(
        self,
        dir: list[Direction],
        body: list[Segment],
        max_length: int,
        max_energy: int,
        reversable: bool,
    ) -> None:
        self.direction = dir
        self.body = body
        self.max_length = max_length
        self.max_energy = self.energy = max_energy
        self.reversable = reversable
        self.eaten = False

    @property
    def head(self) -> Position:
        return self.body[0].pos

    @property
    def length(self) -> int:
        return len(self.body)

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
        elif self.reversable:
            self.body.reverse()
            for i in range(len(self.direction)):
                self.direction[i] = self.direction[i].opposite()
            self.direction.append(dir)

    def update(self) -> None:
        # Consume direction buffer
        if len(self.direction) > 1:
            del self.direction[0]
