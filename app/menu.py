from app.constants import INITIAL_INTERVAL
from app.screen import Screen
from sys import exit
import pygame

class Menu:
    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        pygame.time.set_timer(pygame.USEREVENT, INITIAL_INTERVAL)

    def listenEvents(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.quit()
                case python

    def quit(self):
        pygame.quit()
        exit()

