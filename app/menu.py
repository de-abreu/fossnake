from app.enums import Difficulty
from app.screen import Screen
from sys import exit
import pygame


class Menu:
    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.difficulties = list(Difficulty)
        self.difficulty = 0

    def listenEvents(self) -> Difficulty | None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.quit()
                        case pygame.K_a:
                            self.difficulty = self.difficulty - 1
                        case pygame.K_d:
                            self.difficulty = self.difficulty + 1
                        case pygame.K_w | pygame.K_s:
                            return self.difficulties[self.difficulty]
                    self.difficulty %= len(self.difficulties)

    def draw(self):
        self.screen.drawMenuBackground()
        self.screen.drawMenuCursor(self.difficulty)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        exit()
