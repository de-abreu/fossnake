from app.board import Board
from app.constants import BASE_CELL, BOUNDARIES, FONT_PATH
from app.enums import Difficulty, GameState
from app.game_objects.fruit import Fruit
from app.game_objects.snake import Snake
from app.state import State
from enum import auto
import pygame


class Screen:
    FG = pygame.Color("#233c1e")
    BG = pygame.Color("#8fbc47")
    SIZE = 768
    BOARD_LENGTH = SIZE - 2 * BOUNDARIES
    TOPLEFT, TOPRIGHT, BOTTOMLEFT, BOTTOMRIGHT = (auto() for _ in range(4))

    def __init__(self, state: State) -> None:
        self.state = state
        self.title_font = pygame.font.Font(FONT_PATH, 2 * BASE_CELL)
        self.body_font = pygame.font.Font(FONT_PATH, BASE_CELL // 2)
        self.border = pygame.Rect((BOUNDARIES,) * 2, (Screen.BOARD_LENGTH,) * 2)
        self.display = pygame.display.set_mode((Screen.SIZE,) * 2)
        self.energy_label = self.body_font.render("ENERGY", True, Screen.FG)
        self.energy_max_length = 4 * BASE_CELL
        self.bottom_row = BOUNDARIES + Screen.BOARD_LENGTH + BASE_CELL // 2
        self.top_row = BOUNDARIES - BASE_CELL
        self.energy_pos = (
            BOUNDARIES + Screen.BOARD_LENGTH - 9 * BASE_CELL,
            self.bottom_row,
        )

        # Main menu contents
        self.title = "FOSSNAKE"
        self.title_pos = (BOUNDARIES + BASE_CELL // 2,) * 2

        # Difficulty options
        cta = "CHOOSE A DIFFICULTY:"
        self.cta_label = self.body_font.render(cta, True, Screen.FG)
        self.cta_pos = (
            (Screen.SIZE - self.body_font.size(cta)[0]) // 2,
            BOUNDARIES + 9 * BASE_CELL,
        )

        self.option_labels = [
            self.body_font.render(i, True, Screen.FG) for i in Difficulty.str_list()
        ]

        spacing = 2 * BASE_CELL
        option_pos_x = (Screen.SIZE - self.body_font.size("NORMAL")[0]) // 2
        option_pos_y = BOUNDARIES + 11 * BASE_CELL
        self.option_pos = [
            (option_pos_x - (self.body_font.size("EASY")[0] + spacing), option_pos_y),
            (option_pos_x, option_pos_y),
            (option_pos_x + (self.body_font.size("NORMAL")[0] + spacing), option_pos_y),
        ]

    def printToCorner(self, text: str, corner: int) -> None:
        label = self.body_font.render(text, True, Screen.FG)
        match corner:
            case Screen.TOPLEFT:
                pos = (BOUNDARIES, self.top_row)
            case Screen.TOPRIGHT:
                pos = (
                    BOUNDARIES + Screen.BOARD_LENGTH - label.get_size()[0],
                    self.top_row,
                )
            case Screen.BOTTOMLEFT:
                pos = (BOUNDARIES, self.bottom_row)
            case _:
                pos = (
                    BOUNDARIES + Screen.BOARD_LENGTH - label.get_size()[0],
                    self.bottom_row,
                )
        self.display.blit(label, pos)

    def drawHUD(
        self, score: int, energy: int, max_energy: int, state: GameState
    ) -> None:
        match state:
            case GameState.RUNNING:
                self.printToCorner(
                    f"HIGHSCORE: {self.state.getHighscore():05d}", Screen.TOPLEFT
                )
                self.printToCorner("P: PAUSE", Screen.TOPRIGHT)
            case GameState.PAUSED:
                self.printToCorner("P: RESUME GAME", Screen.TOPLEFT)
                self.printToCorner("ESC: QUIT", Screen.TOPRIGHT)
            case _:
                self.printToCorner("GAME OVER: PRESS ESC TO GO BACK", Screen.TOPLEFT)
        self.printToCorner(f"SCORE: {score:05d}", Screen.BOTTOMLEFT)
        energy_length = int(energy / max_energy * self.energy_max_length)
        energy_bar = pygame.Rect(
            (Screen.BOARD_LENGTH + BOUNDARIES - energy_length, self.bottom_row),
            (energy_length, BASE_CELL // 2),
        )
        self.display.blit(self.energy_label, self.energy_pos)
        pygame.draw.rect(self.display, Screen.FG, energy_bar)
        pygame.draw.rect(self.display, Screen.FG, self.border, 5)

    def drawBoard(self, snake: Snake, fruits: list[Fruit], board: Board) -> None:
        self.display.fill(Screen.BG)
        for segment in snake.body:
            self.display.blit(segment.sprite, board.getTileRect(segment.pos))  # type: ignore
        for fruit in fruits:
            if fruit.display:
                self.display.blit(fruit.sprite, board.getTileRect(fruit.pos))

    def drawMenuCursor(self) -> None:
        option = self.state.getDifficultyIndex()
        pos = self.option_pos[option]
        pos = (pos[0] - 8, pos[1] - 8)
        width = self.option_labels[option].get_width() + 10
        height = self.option_labels[option].get_height() + 16
        selection = pygame.Rect(pos, (width, height))
        pygame.draw.rect(self.display, Screen.FG, selection, 4)

    def drawMenuBackground(self) -> None:
        self.display.fill(Screen.BG)

        # Print title
        char_pos = self.title_pos
        for char in self.title:
            char_label = self.title_font.render(char, True, Screen.FG)
            self.display.blit(char_label, char_pos)
            char_pos = (char_pos[0] + 2.43 * BASE_CELL, char_pos[1])

        # Print difficulty options
        self.display.blit(self.cta_label, self.cta_pos)
        for label, pos in zip(self.option_labels, self.option_pos):
            self.display.blit(label, pos)

        # Print control instructions
        self.printToCorner("ESC: QUIT", Screen.TOPRIGHT)
        self.printToCorner("W/A/S/D: MOVE", Screen.BOTTOMLEFT)
        self.printToCorner("ENTER: CONFIRM", Screen.BOTTOMRIGHT)
        pygame.draw.rect(self.display, Screen.FG, self.border, 5)
