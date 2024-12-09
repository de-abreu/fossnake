from dataclasses import dataclass
from pygame import Surface


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Segment:
    pos: Position
    sprite: Surface | None = None
