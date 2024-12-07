from app.game_objects.game_object import GameObject
from app.constants import (
    BOARD_LENGTH,
    BOUNDARIES,
    SCREEN_SIZE,
    CELL_SIZE,
    FONT_PATH,
    MAX_ENERGY,
)
import pygame


class Screen:
    FG = pygame.Color("#233c1e")
    BG = pygame.Color("#8fbc47")

    def __init__(self, size: int) -> None:
        self.title_font = pygame.font.Font(FONT_PATH, 2 * CELL_SIZE)
        self.body_font = pygame.font.Font(FONT_PATH, CELL_SIZE // 2)
        self.border = pygame.Rect((BOUNDARIES,) * 2, (BOARD_LENGTH,) * 2)
        self.display = pygame.display.set_mode((size, size))
        self.energy_label = self.body_font.render("ENERGY", True, Screen.FG)
        self.energy_max_length = 4 * CELL_SIZE
        self.hud_bottom_row = size - BOUNDARIES + CELL_SIZE // 2
        self.hud_top_row = BOUNDARIES - CELL_SIZE
        self.bottom_row_pos = (BOUNDARIES, self.hud_bottom_row)
        self.top_row_pos = (BOUNDARIES, self.hud_top_row)
        self.energy_pos = BOUNDARIES + BOARD_LENGTH - 9 * CELL_SIZE, self.hud_bottom_row

        # Main menu contents
        self.title = "FOSSNAKE"
        self.title_pos = (BOUNDARIES + CELL_SIZE // 2,) * 2

        cta = "CHOOSE A DIFFICULTY:"
        self.cta_label = self.body_font.render(cta, True, Screen.FG)
        self.cta_pos = (
            (SCREEN_SIZE - self.body_font.size(cta)[0]) // 2,
            BOUNDARIES + 9 * CELL_SIZE,
        )

        self.option_labels = [
            self.body_font.render(i, True, Screen.FG)
            for i in ["EASY", "NORMAL", "HARD"]
        ]

        spacing = 2 * CELL_SIZE
        option_pos_x = (SCREEN_SIZE - self.body_font.size("NORMAL")[0]) // 2
        option_pos_y = BOUNDARIES + 11 * CELL_SIZE
        self.option_pos = [
            (option_pos_x - (self.body_font.size("EASY")[0] + spacing), option_pos_y),
            (option_pos_x, option_pos_y),
            (option_pos_x + (self.body_font.size("NORMAL")[0] + spacing), option_pos_y),
        ]

    def drawHUD(self, score: int, highscore: int, energy: int, paused: bool):
        top_row_label = (
            'GAME PAUSED: PRESS "P" TO RESUME'
            if paused
            else f"HIGHSCORE: {highscore:05d}"
        )
        top_row = self.body_font.render(top_row_label, True, Screen.FG)
        bottom_row = self.body_font.render(f"SCORE: {score:05d}", True, Screen.FG)
        energy_length = int(energy / MAX_ENERGY * self.energy_max_length)
        energy_bar = pygame.Rect(
            (BOARD_LENGTH + BOUNDARIES - energy_length, self.hud_bottom_row),
            (energy_length, CELL_SIZE // 2),
        )
        self.display.blit(top_row, self.top_row_pos)
        self.display.blit(bottom_row, self.bottom_row_pos)
        self.display.blit(self.energy_label, self.energy_pos)
        pygame.draw.rect(self.display, Screen.FG, energy_bar)

    def drawBoard(self, game_objects: list[GameObject]) -> None:
        self.display.fill(Screen.BG)
        for game_object in game_objects:
            game_object.draw(self.display)
        pygame.draw.rect(self.display, Screen.FG, self.border, 5)

    def drawMenuCursor(self, option: int) -> None:
        pos = self.option_pos[option]
        pos = (pos[0] - 5, pos[1] - 5)
        width = self.option_labels[option].get_width() + 10
        height = self.option_labels[option].get_height() + 10
        selection = pygame.Rect(pos, (width, height))
        pygame.draw.rect(self.display, Screen.FG, selection, 2)

    def drawMenuBackground(self) -> None:
        self.display.fill(Screen.BG)

        # Print title
        char_pos = self.title_pos
        for char in self.title:
            char_label = self.title_font.render(char, True, Screen.FG)
            self.display.blit(char_label, char_pos)
            char_pos = (char_pos[0] + 2.43 * CELL_SIZE, char_pos[1])

        # Print all the rest
        self.display.blit(self.cta_label, self.cta_pos)
        for label, pos in zip(self.option_labels, self.option_pos):
            self.display.blit(label, pos)

        pygame.draw.rect(self.display, Screen.FG, self.border, 5)
