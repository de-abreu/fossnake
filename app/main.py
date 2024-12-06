from app.board import Board
from app.constants import MAX_ENERGY, CELL_NUMBER, CELL_SIZE
from app.enums import Tile
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.screen import Screen
import pygame


class Main:
    def __init__(self, screen: Screen) -> None:
        self.reset(screen)

    def listenEvents(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case self.SCREEN_UPDATE:
                    self.update()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_p:
                            self.paused = not self.paused
                        case pygame.K_ESCAPE:
                            self.quit()
                        case _:
                            self.snake.changeDirection(event)

    def update(self):
        if self.paused:
            return
        match self.snake.move():
            case Tile.FRUIT:
                self.fruit.spawn(self.snake.head.pos)

                # Increment the score by the percentual of energy left, before restoring it
                self.score += self.energy * 100 // MAX_ENERGY
                self.energy = MAX_ENERGY
                if self.score > self.highscore:
                    self.highscore = self.score
                if self.score != self.next_increase:
                    return

                # Increase the snake's energy and speed (if deemed so)
                self.interval = self.interval * 95 // 100  # Speed increase of 5%
                self.next_increase += self.next_increase
                pygame.time.set_timer(self.SCREEN_UPDATE, self.interval)

            case other:
                if self.energy <= 0 or other == Tile.SNAKE or other == Tile.EATEN:
                    self.saveHighscore()
                    self.reset(self.screen)
                else:
                    self.energy -= 1

    def draw(self):
        self.screen.drawBoard([self.fruit, self.snake])
        self.screen.drawHUD(self.score, self.highscore, self.energy)
        pygame.display.update()

    def reset(self, screen: Screen):
        # Game Objects
        self.board = Board(CELL_NUMBER, CELL_NUMBER, CELL_SIZE)
        self.snake = Snake(self.board)
        self.fruit = Fruit(self.board, self.snake.head.pos)
        self.screen = screen

        # Score, energy, and game speed
        self.score = 0
        self.highscore = self.retrieveHighscore()
        self.energy = MAX_ENERGY
        self.next_increase = 100
        self.interval = 150

        # Pause Boolean and setting the initial rate at which the game gets updated
        self.paused = False
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, self.interval)

    def retrieveHighscore(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except Exception:
            return 0

    def saveHighscore(self):
        if self.score == self.highscore:
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def quit(self):
        self.saveHighscore()
        pygame.quit()
        exit()
