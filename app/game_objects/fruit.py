from app.board import Board
from app.position import Position
from app.constants import SPRITES_PATH
from app.game_objects.game_object import GameObject
from pygame import Surface
from pygame.image import load


class Fruit(GameObject):
    def __init__(self, board: Board, snake_pos: Position, poisoned: bool, timeout: int) -> None:
        super().__init__(board)
        if poisoned:
            self.sprite = load(SPRITES_PATH + "obstacle.svg")
        else:
            self.sprite = load(SPRITES_PATH + "fruit.svg")
        self.timeout = timeout
        self.poisoned = poisoned
        self.warning = timeout // 10
        self.spawn(snake_pos)

    def spawn(self, pos: Position) -> None:
        """
        From a given set of random locations, find one which is the farthest from Position pos and place the fruit there.
        """
        b = self.board
        sample = []
        while len(sample) < 3:
            pos = b.random(0)
            if b.getTile(pos):
                sample.append(pos)

        self.pos = sample[0]
        for i in range(1, len(sample)):
            if b.distance(sample[i], pos) > b.distance(self.pos, pos):
                self.pos = sample[i]
        b.setTile(self.pos, self)
        self.timeleft = self.timeout
        self.display = True

    def update(self):
        if self.timeleft <= self.warning:
            self.display = not self.display


    def draw(self, surface: Surface) -> None:
        if self.display:
            surface.blit(self.sprite, self.getTileRect(self.pos))
