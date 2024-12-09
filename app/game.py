from app.board import Board
from app.constants import BASE_CELL, SPRITES_PATH
from app.dataclasses import Position, Segment
from app.enums import Difficulty, Direction, Loop, GameState
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.screen import Screen
from app.state import State
from pygame.image import load
import pygame

# Snake sprites
DIRS = ["u", "l", "d", "r"]
BEND = [load(SPRITES_PATH + f"{dir}_bend.svg") for dir in DIRS]
BELLY = [load(SPRITES_PATH + f"{dir}_belly.svg") for dir in DIRS]
BODY = [load(SPRITES_PATH + f"{dir}_body.svg") for dir in DIRS]
MOUTH_CLOSED = [load(SPRITES_PATH + f"{dir}_mouth_closed.svg") for dir in DIRS]
MOUTH_OPEN = [load(SPRITES_PATH + f"{dir}_mouth_open.svg") for dir in DIRS]
TAIL = [load(SPRITES_PATH + f"{dir}_tail.svg") for dir in DIRS]

# Fruit sprites
FRUIT = load(SPRITES_PATH + "fruit.svg")
POISONED = load(SPRITES_PATH + "poisoned.svg")


class Game:
    def __init__(self, screen: Screen, state: State) -> None:
        self.screen = screen
        self.state = state

    def reset(self) -> None:
        match self.state.difficulty:
            case Difficulty.EASY:
                self.board = Board(40, BASE_CELL // 2)
                self.snake = self.placeSnake(
                    2 * self.board.size, 6 * self.board.size, True
                )
                self.fruits = [
                    self.placeFruit(self.snake.head, False, -1) for _ in range(2)
                ]
                self.increase_difficulty = 200
                self.interval = 150
            case Difficulty.NORMAL:
                self.board = Board(20, BASE_CELL)
                self.snake = self.placeSnake(
                    3 * self.board.size, 4 * self.board.size, False
                )
                self.fruits = [self.placeFruit(self.snake.head, False, -1)] + [
                    self.placeFruit(self.snake.head, True, 2 * self.board.size)
                    for _ in range(5)
                ]
                self.increase_difficulty = 200
                self.interval = 150
            case _:
                self.board = Board(20, BASE_CELL)
                self.snake = self.placeSnake(
                    4 * self.board.size, 3 * self.board.size, False
                )
                self.fruits = [
                    self.placeFruit(self.snake.head, False, 2 * self.board.size)
                ] + [
                    self.placeFruit(self.snake.head, True, 2 * self.board.size)
                    for _ in range(5)
                ]
                self.increase_difficulty = 50
                self.interval = 100
        self.score = 0
        self.eaten = False
        self.game_state = GameState.RUNNING
        pygame.time.set_timer(pygame.USEREVENT, self.interval)
        self.assignSprites(False)

    def listenEvents(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.state.loop = Loop.QUIT
                case pygame.USEREVENT:
                    self.update()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_p:
                            match self.game_state:
                                case GameState.RUNNING:
                                    self.game_state = GameState.PAUSED
                                case GameState.PAUSED:
                                    self.game_state = GameState.RUNNING
                        case pygame.K_ESCAPE:
                            self.state.loop = Loop.MENU
                        case _:
                            self.snake.changeDirection(event)

    def update(self) -> None:
        if self.game_state != GameState.RUNNING:
            return
        next_pos = self.board.offset(self.snake.head, self.snake.direction[0], 1)
        next_tile = self.board.getTile(next_pos)
        if next_tile != self.snake and self.snake.energy > 0:
            self.snake.body = [Segment(next_pos)] + self.snake.body
            self.board.setTile(self.snake.head, self.snake)
            if type(next_tile) is Fruit:
                if next_tile.poisoned:
                    self.snake.energy -= 10
                    self.board.setTile(self.snake.body.pop().pos, None)
                else:
                    self.score += self.snake.energy * 100 // self.snake.max_energy
                    self.snake.energy = self.snake.max_energy
                    self.state.updateHighscore(self.score)
                    if self.score < self.increase_difficulty:
                        self.interval = (
                            self.interval * 98 // 100
                        )  # Speed increase of 2%
                        self.increase_difficulty += self.increase_difficulty
                        pygame.time.set_timer(pygame.USEREVENT, self.interval)
                self.respawnfruit(next_tile)
                self.assignSprites(True)
            else:
                self.snake.energy -= 1
                self.board.setTile(self.snake.body.pop().pos, None)
                self.assignSprites(False)
            self.snake.update()
            for fruit in self.fruits:
                fruit.update()
                if fruit.timeleft == 0:
                    self.respawnfruit(fruit)
        else:
            self.game_state = GameState.GAMEOVER
            self.state.saveHighscore()

    def draw(self):
        self.screen.drawBoard(self.snake, self.fruits, self.board)
        self.screen.drawHUD(
            self.score,
            self.snake.energy,
            self.snake.max_energy,
            self.game_state,
        )
        pygame.display.update()

    def assignSprites(self, new: bool) -> None:
        self.assignHead()
        self.assignNeck()
        self.assignTail()
        self.eaten = new

    def assignHead(self) -> None:
        dir = self.snake.direction[0]
        next_tile = self.board.getTile(self.board.offset(self.snake.head, dir, 1))
        i = list(Direction).index(dir)
        self.snake.body[0].sprite = MOUTH_OPEN[i] if next_tile else MOUTH_CLOSED[i]

    def assignNeck(self):
        next, current, prev = [self.snake.body[i].pos for i in range(3)]
        match next:
            case up if up == self.board.offset(current, Direction.UP, 1):
                if self.eaten:
                    self.snake.body[1].sprite = BELLY[0]
                elif prev == self.board.offset(current, Direction.DOWN, 1):
                    self.snake.body[1].sprite = BODY[0]
                elif prev == self.board.offset(current, Direction.LEFT, 1):
                    self.snake.body[1].sprite = BEND[0]
                else:
                    self.snake.body[1].sprite = BEND[3]
            case left if left == self.board.offset(current, Direction.LEFT, 1):
                if self.eaten:
                    self.snake.body[1].sprite = BELLY[1]
                elif prev == self.board.offset(current, Direction.RIGHT, 1):
                    self.snake.body[1].sprite = BODY[1]
                elif prev == self.board.offset(current, Direction.UP, 1):
                    self.snake.body[1].sprite = BEND[0]
                else:
                    self.snake.body[1].sprite = BEND[1]
            case down if down == self.board.offset(current, Direction.DOWN, 1):
                if self.eaten:
                    self.snake.body[1].sprite = BELLY[2]
                elif prev == self.board.offset(current, Direction.UP, 1):
                    self.snake.body[1].sprite = BODY[2]
                elif prev == self.board.offset(current, Direction.LEFT, 1):
                    self.snake.body[1].sprite = BEND[1]
                else:
                    self.snake.body[1].sprite = BEND[2]
            case _:
                if self.eaten:
                    self.snake.body[1].sprite = BELLY[3]
                elif prev == self.board.offset(current, Direction.LEFT, 1):
                    self.snake.body[1].sprite = BODY[3]
                elif prev == self.board.offset(current, Direction.UP, 1):
                    self.snake.body[1].sprite = BEND[3]
                else:
                    self.snake.body[1].sprite = BEND[2]

    def assignTail(self) -> None:
        next = self.snake.body[-2].pos
        current = self.snake.body[-1]
        for i, dir in enumerate(list(Direction)):
            if next == self.board.offset(current.pos, dir, 1):
                current.sprite = TAIL[i]

    def initialDirection(self, pos: Position) -> Direction:
        if pos.x < self.board.size // 2:
            if pos.y < self.board.size // 2:
                if pos.x < pos.y:
                    return Direction.RIGHT
                return Direction.DOWN
            if pos.x < self.board.size - pos.y:
                return Direction.RIGHT
            return Direction.UP
        if pos.y < self.board.size // 2:
            if self.board.size - pos.x < pos.y:
                return Direction.LEFT
            return Direction.DOWN
        if self.board.size - pos.x < self.board.size - pos.y:
            return Direction.LEFT
        return Direction.UP

    def placeSnake(self, max_length: int, max_energy: int, reversable: bool) -> Snake:
        pos = self.board.random(3)
        dir = [self.initialDirection(pos)]
        orientation = dir[0].opposite()
        body = [Segment(self.board.offset(pos, orientation, i)) for i in range(3)]
        snake = Snake(dir, body, max_length, max_energy, reversable)
        for segment in snake.body:
            self.board.setTile(segment.pos, snake)
        return snake

    def respawnfruit(self, fruit: Fruit) -> None:
        self.fruits += [self.placeFruit(self.snake.head, fruit.poisoned, fruit.timeout)]
        try:
            self.fruits.remove(fruit)
        except ValueError:
            pass

    def placeFruit(self, snake: Position, poisoned: bool, timeout: int) -> Fruit:
        sample = []
        while len(sample) < 3:
            pos = self.board.random(0)
            if not self.board.getTile(pos):
                sample.append(pos)

        pos = sample[0]
        for other in sample[1:]:
            if self.board.distance(snake, pos) > self.board.distance(snake, other):
                pos = other
        fruit = Fruit(pos, poisoned, timeout)
        self.board.setTile(pos, fruit)
        return fruit
