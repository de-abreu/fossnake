from app.enums import Difficulty, Loop
from app.state import State
from app.screen import Screen
from sys import exit
import pygame


class Menu:
    def __init__(self, screen: Screen, state: State) -> None:
        self.screen = screen
        self.state = state

    def listenEvents(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.state.loop = Loop.QUIT
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.state.loop = Loop.QUIT
                        case pygame.K_a:
                            self.state.changeDifficulty(-1)
                        case pygame.K_d:
                            self.state.changeDifficulty(+1)
                        case pygame.K_w | pygame.K_s:
                            self.state.loop = Loop.SETUP

    def draw(self):
        self.screen.drawMenuBackground()
        self.screen.drawMenuCursor()
        pygame.display.update()

    def quit(self):
        pygame.quit()
        exit()
