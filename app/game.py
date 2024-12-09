from app.board import Board
from app.constants import (
    INITIAL_INTERVAL,
    MAX_ENERGY,
    MAX_LENGTH,
    CELL_NUMBER,
    CELL_SIZE,
    TIMEOUT,
)
from app.state import State
from app.enums import Difficulty, Loop, GameState
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.screen import Screen
import pygame


class Game:
    NORMAL_SIZE = 20
    HARD_SIZE = 25
    NORMAL_SPEED = 150
    HARD_SPEED = 100
    APPLE_TIMEOUT = 100

    def __init__(self, screen: Screen, state: State) -> None:
        self.screen = screen
        self.state = state

    def listenEvents(self):
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

    def update(self):
        if self.game_state != GameState.RUNNING:
            return
        match self.snake.update():
            case self.snake:
                self.game_state = GameState.GAMEOVER
                self.state.saveHighscore()
            case fruit if type(fruit) is Fruit:
                if fruit.poisoned:
                    self.energy -= 10
                else:
                    self.score += self.energy * 100 // MAX_ENERGY
                    self.energy = MAX_ENERGY
                    self.state.updateHighscore(self.score)
                    fruit.spawn(self.snake.head.pos)
                    if self.score < self.next_increase:
                        self.interval = (
                            self.interval * 95 // 100
                        )  # Speed increase of 5%
                        self.next_increase += self.next_increase
                        pygame.time.set_timer(pygame.USEREVENT, self.interval)
            case _:
                self.energy -= 1

    def draw(self):
        self.screen.drawBoard([self.snake] + self.fruits)
        pygame.display.update()

    # TODO: Setup initial values according to the selected difficulty
    def reset(self, difficulty: Difficulty):
        # Game Objects
        self.board = Board(CELL_NUMBER, CELL_NUMBER, CELL_SIZE)
        self.snake = Snake(self.board, MAX_LENGTH)
        self.fruits = [Fruit(self.board, self.snake.head.pos, False, TIMEOUT)]

        # Score, energy, and game speed
        self.score = 0
        self.energy = MAX_ENERGY
        self.next_increase = 100
        self.interval = INITIAL_INTERVAL

        self.game_state = GameState.RUNNING
        # TODO: Remove the following line once the main menu implementation is finished
        pygame.time.set_timer(pygame.USEREVENT, self.interval)
