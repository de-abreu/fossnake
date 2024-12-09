#!/usr/bin/python3

"""
Copyright (c) 2003 by Monaco F. J.
Copyright (c) 2024 by Guilherme de Abreu

This file is part of FOSSnake.

FOSSnake is a derivative work of the code from Coral by Monaco F. J.,
distributed under GNU GPL v3. Coral source code can be found at https://github.com/courselab/coral. The main changes applied to the
original code are listed in the file Changelog.

Coral is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from app.enums import Difficulty, Loop
from app.game import Game
from app.menu import Menu
from app.screen import Screen
from app.state import State
import pygame

pygame.init()
clk = pygame.time.Clock()
game_state = State(Loop.MENU, Difficulty.EASY, "highscore.txt")
screen = Screen(game_state)
menu_loop = Menu(screen, game_state)
game_loop = Game(screen, game_state)

while True:
    match game_state.loop:
        case Loop.MENU:
            menu_loop.listenEvents()
            menu_loop.draw()
        case Loop.SETUP:
            game_loop.reset()
            game_state.loop = Loop.GAME
        case Loop.GAME:
            game_loop.listenEvents()
            game_loop.draw()
        case _:
            break
    clk.tick(60)
game_state.saveHighscore()
pygame.quit()
exit()
