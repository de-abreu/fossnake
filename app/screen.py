from app.game_objects.game_object import GameObject
from app.constants import (
    BG,
    BOARD_LENGTH,
    BOUNDARIES,
    CELL_SIZE,
    FG,
    FONT_PATH,
    MAX_ENERGY,
)
import pygame


class Screen:
    def __init__(self, size: int) -> None:
        self.body_font = pygame.font.Font(FONT_PATH, CELL_SIZE // 2)
        self.border = pygame.Rect(BOUNDARIES, BOUNDARIES, BOARD_LENGTH, BOARD_LENGTH)
        self.display = pygame.display.set_mode((size, size))
        self.energy_label = self.body_font.render("ENERGY", True, pygame.Color(FG))
        self.energy_max_length = 4 * CELL_SIZE
        self.hud_bottom_row = size - BOUNDARIES + CELL_SIZE // 2
        self.hud_top_row = BOUNDARIES - CELL_SIZE
        self.bottom_row_pos = (BOUNDARIES, self.hud_bottom_row)
        self.top_row_pos = (BOUNDARIES, self.hud_top_row)
        self.energy_pos = BOUNDARIES + BOARD_LENGTH - 9 * CELL_SIZE, self.hud_bottom_row

    def drawHUD(self, score: int, highscore: int, energy: int, paused: bool):
        top_row_label = (
            'GAME PAUSED: PRESS "P" TO RESUME'
            if paused
            else f"HIGHSCORE: {highscore:05d}"
        )
        top_row = self.body_font.render(top_row_label, True, pygame.Color(FG))
        bottom_row = self.body_font.render(
            f"SCORE: {score:05d}", True, pygame.Color(FG)
        )
        energy_length = int(energy / MAX_ENERGY * self.energy_max_length)
        energy_bar = pygame.Rect(
            (BOARD_LENGTH + BOUNDARIES - energy_length, self.hud_bottom_row),
            (energy_length, CELL_SIZE // 2),
        )
        self.display.blit(top_row, self.top_row_pos)
        self.display.blit(bottom_row, self.bottom_row_pos)
        self.display.blit(self.energy_label, self.energy_pos)
        pygame.draw.rect(self.display, pygame.Color(FG), energy_bar)

    def drawBoard(self, game_objects: list[GameObject]) -> None:
        self.display.fill(pygame.Color(BG))
        for game_object in game_objects:
            game_object.draw(self.display)
        pygame.draw.rect(self.display, pygame.Color(FG), self.border, 5)
