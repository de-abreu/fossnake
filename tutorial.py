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
from random import randint as rand
from sys import exit

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.coord = (x, y)

    def __eq__(self, other) -> bool:
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]

    def __add__(self, other, size):
        return Position((self.coord[0] + other.coord[0]) % size, ( self.coord[1] + other.coord[1] ) % size)

    def __repr__(self) -> str:
        return str(self.coord)

    def distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def random(self, min : int, max: int) -> tuple[int,int]:
        return (rand(min, max- 1), rand(min, max - 1))

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size
        )
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.pos = Position.random() Position(rand(0, cell_number - 1), rand(0, cell_number - 1))


class Snake:
    def __init__(self):
        self.head
        self.tail = [Position(2, 10), Position(1, 10), Position(0, 10)]
        self.direction = Position(1, 0)

    def move_snake(self, apple):
        self.body = [self.body[0] + self.direction] + (
            self.body if self.body[0] == apple.pos else self.body[:-1]
        )

    def draw_snake(self):
        for segment in self.body:
            snake_rect = pygame.Rect(
                segment.x * cell_size, segment.y * cell_size, cell_size, cell_size
            )
            pygame.draw.rect(screen, (183, 191, 122), snake_rect)


class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake(self.fruit)
        self.check_collision()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()


def game():
    pygame.init()
    clk = pygame.time.Clock()
    main_game = Main()

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_w:
                            main_game.snake.direction = Position(0, -1)
                        case pygame.K_a:
                            main_game.snake.direction = Position(-1, 0)
                        case pygame.K_s:
                            main_game.snake.direction = Position(0, 1)
                        case pygame.K_d:
                            main_game.snake.direction = Position(1, 0)
        main_game.update()

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clk.tick(7)


game()
