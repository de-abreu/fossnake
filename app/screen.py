from app.game_objects.game_object import GameObject
from app.constants import (
    BG,
    BOARD_LENGTH,
    CELL_SIZE,
    FG,
    FONT_PATH,
    HEIGHT,
    H_BOUNDARIES,
    MAX_ENERGY,
    V_BOUNDARIES,
)
import pygame


class Screen:
    def __init__(self, height: int, width: int) -> None:
        self.display = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(FONT_PATH, CELL_SIZE // 2)

        # Defining some constants for interface rendering
        self.BORDER = pygame.Rect(
            H_BOUNDARIES, V_BOUNDARIES, BOARD_LENGTH, BOARD_LENGTH
        )
        self.SECOND_ROW_V_POS = HEIGHT - V_BOUNDARIES + CELL_SIZE // 2
        self.SCORE_POS = (H_BOUNDARIES, self.SECOND_ROW_V_POS)
        self.HIGHSCORE_POS = (H_BOUNDARIES, 2 * CELL_SIZE)
        self.ENERGY_POS = (
            H_BOUNDARIES + BOARD_LENGTH - 9 * CELL_SIZE,
            self.SECOND_ROW_V_POS,
        )
        self.ENERGY_LABEL = self.font.render("ENERGY", True, pygame.Color(FG))
        self.ENERGY_MAX_LENGHT = 4 * CELL_SIZE

    def drawHUD(self, score: int, highscore: int, energy: int):
        score_label = self.font.render(f"SCORE: {score:05d}", True, pygame.Color(FG))
        highscore_label = self.font.render(
            f"HIGHSCORE: {highscore:05d}", True, pygame.Color(FG)
        )
        energy_length = int(energy / MAX_ENERGY * self.ENERGY_MAX_LENGHT)
        energy_bar = pygame.Rect(
            (BOARD_LENGTH + H_BOUNDARIES - energy_length, self.SECOND_ROW_V_POS),
            (energy_length, CELL_SIZE // 2),
        )
        self.display.blit(highscore_label, self.HIGHSCORE_POS)
        self.display.blit(score_label, self.SCORE_POS)
        self.display.blit(self.ENERGY_LABEL, self.ENERGY_POS)
        pygame.draw.rect(self.display, pygame.Color(FG), energy_bar)

    def drawBoard(self, game_objects: list[GameObject]) -> None:
        self.display.fill(pygame.Color(BG))
        for game_object in game_objects:
            game_object.draw(self.display)
        pygame.draw.rect(self.display, pygame.Color(FG), self.BORDER, 5)
