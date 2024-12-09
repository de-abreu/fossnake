from app.board import Board
from app.constants import SPRITES_PATH
from app.enums import Direction
from app.position import Position
from pygame.image import load


class Segment:
    # The various snake sprites
    DIRS = ["u", "l", "d", "r"]
    BEND = [load(SPRITES_PATH + f"{dir}_bend.svg") for dir in DIRS]
    BELLY = [load(SPRITES_PATH + f"{dir}_belly.svg") for dir in DIRS]
    BODY = [load(SPRITES_PATH + f"{dir}_body.svg") for dir in DIRS]
    MOUTH_CLOSED = [load(SPRITES_PATH + f"{dir}_mouth_closed.svg") for dir in DIRS]
    MOUTH_OPEN = [load(SPRITES_PATH + f"{dir}_mouth_open.svg") for dir in DIRS]
    TAIL = [load(SPRITES_PATH + f"{dir}_tail.svg") for dir in DIRS]

    def __init__(self, pos: Position) -> None:
        self.pos = pos

    def assignHead(self, dir: Direction, board: Board) -> None:
        next_tile = board.getTile(board.move(self.pos, dir, 1))
        i = list(Direction).index(dir)
        self.sprite = Segment.MOUTH_OPEN[i] if next_tile else Segment.MOUTH_CLOSED[i]

    def assignNeck(
        self, next: Position, prev: Position, eaten: bool, board: Board
    ) -> None:
        match next:
            case up if up == board.move(self.pos, Direction.UP, 1):
                if eaten:
                    self.sprite = Segment.BELLY[0]
                elif prev == board.move(self.pos, Direction.DOWN, 1):
                    self.sprite = Segment.BODY[0]
                elif prev == board.move(self.pos, Direction.LEFT, 1):
                    self.sprite = Segment.BEND[0]
                else:
                    self.sprite = Segment.BEND[3]
            case left if left == board.move(self.pos, Direction.LEFT, 1):
                if eaten:
                    self.sprite = Segment.BELLY[1]
                elif prev == board.move(self.pos, Direction.RIGHT, 1):
                    self.sprite = Segment.BODY[1]
                elif prev == board.move(self.pos, Direction.UP, 1):
                    self.sprite = Segment.BEND[0]
                else:
                    self.sprite = Segment.BEND[1]
            case down if down == board.move(self.pos, Direction.DOWN, 1):
                if eaten:
                    self.sprite = Segment.BELLY[2]
                elif prev == board.move(self.pos, Direction.UP, 1):
                    self.sprite = Segment.BODY[2]
                elif prev == board.move(self.pos, Direction.LEFT, 1):
                    self.sprite = Segment.BEND[1]
                else:
                    self.sprite = Segment.BEND[2]
            case _:
                if eaten:
                    self.sprite = Segment.BELLY[3]
                elif prev == board.move(self.pos, Direction.LEFT, 1):
                    self.sprite = Segment.BODY[3]
                elif prev == board.move(self.pos, Direction.UP, 1):
                    self.sprite = Segment.BEND[3]
                else:
                    self.sprite = Segment.BEND[2]

    def assignTail(self, next: Position, board: Board) -> None:
        for i, dir in enumerate(list(Direction)):
            if next == board.move(self.pos, dir, 1):
                self.sprite = Segment.TAIL[i]
