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

import pygame
from app.constants import HEIGHT, WIDTH
from app.screen import Screen
from app.main import Main

pygame.init()
clk = pygame.time.Clock()
game_loop = Main(Screen(HEIGHT, WIDTH))
while True:
    game_loop.listenEvents()
    game_loop.draw()
    clk.tick(60)
