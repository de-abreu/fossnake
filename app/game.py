from app.board import Board
from app.constants import INITIAL_INTERVAL, MAX_ENERGY, CELL_NUMBER, CELL_SIZE
from app.state import State
from app.enums import Difficulty, Tile
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.screen import Screen
import pygame


# TODO: Review every class considering that game states is now a thing
class Game:
    def __init__(self, screen: Screen, state: State) -> None:
        self.screen = screen
        self.state = state

    def listenEvents(self, state: State) -> State:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.USEREVENT:
                    self.update()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_p:
                            self.paused = not self.paused
                        case pygame.K_ESCAPE:
                            return False
                        case _:
                            self.snake.changeDirection(event)
        return state

    def update(self):
        if self.paused:
            return
        match self.snake.move():
            case Tile.FRUIT:
                self.fruit.spawn(self.snake.head.pos)

                # Increment the score by the percentual of energy left, before restoring it
                self.score += self.energy * 100 // MAX_ENERGY
                self.energy = MAX_ENERGY
                # if self.score > self.highscore[0]:
                #     self.highscore = self.score
                # if self.score != self.next_increase:
                #     return

                # Increase the snake's energy and speed (if deemed so)
                self.interval = self.interval * 95 // 100  # Speed increase of 5%
                self.next_increase += self.next_increase
                pygame.time.set_timer(pygame.USEREVENT, self.interval)

            # case other:
            # if self.energy <= 0 or other == Tile.SNAKE or other == Tile.EATEN:
            #     self.saveHighscore()
            #     TODO:
            #     Change the following line later to send the player back to the Main menu, possibly by omitting this instruction altogether.
            #     Modify every occurrence of self.highscore to fetch the highscore of the current difficulty level.
            #     self.reset(self.screen, self.highscore)
            # else:
            #     self.energy -= 1

    def draw(self):
        self.screen.drawBoard([self.fruit, self.snake])
        # self.screen.drawHUD(self.score, self.highscore, self.energy, self.paused)
        pygame.display.update()

    # TODO: Setup initial values according to the selected difficulty
    def reset(self, difficulty: Difficulty):
        # Game Objects
        self.board = Board(CELL_NUMBER, CELL_NUMBER, CELL_SIZE)
        self.snake = Snake(self.board)
        self.fruit = Fruit(self.board, self.snake.head.pos)

        # Score, energy, and game speed
        self.score = 0
        self.energy = MAX_ENERGY
        self.next_increase = 100
        self.interval = INITIAL_INTERVAL

        # Pause Boolean and setting the initial rate at which the game gets updated
        self.paused = False
        # TODO: Remove the following line once the main menu implementation is finished
        pygame.time.set_timer(pygame.USEREVENT, self.interval)

    def quit(self):
        pygame.quit()
        exit()
