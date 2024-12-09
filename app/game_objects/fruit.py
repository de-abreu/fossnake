from app.constants import SPRITES_PATH
from app.dataclasses import Position
from pygame.image import load


class Fruit:
    def __init__(self, pos: Position, poisoned: bool, timeout: int) -> None:
        self.pos = pos
        self.poisoned = poisoned
        if poisoned:
            self.sprite = load(SPRITES_PATH + "obstacle.svg")
        else:
            self.sprite = load(SPRITES_PATH + "fruit.svg")
        self.timeout = self.timeleft = timeout
        self.warning = timeout // 10

    def update(self) -> None:
        if self.timeleft <= self.warning:
            self.display = not self.display
        self.timeleft -= 1
