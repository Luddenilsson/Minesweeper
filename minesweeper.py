import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
GRAY_2 = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

COLOR_LIST = [GREEN, BLUE, RED, PURPLE, CYAN, YELLOW, BLACK, WHITE, ORANGE]

# Define constants
WIDTH, HEIGHT = 700, 700
"""GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE"""
DIFFICULTIES = {
    "Easy": {"grid_size": 10, "mine_count": 10},
    "Medium": {"grid_size": 15, "mine_count": 30},
    "Hard": {"grid_size": 20, "mine_count": 75},
    "Expert": {"grid_size": 25, "mine_count": 110},
}

class Minesweeper:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()

        self.grid_size = 0
        self.mine_count = 0
        self.grid = 0
        self.mine_locations = set()
        self.flags = set()
        self.revealed_cells = set()

        self.choose_difficulty()
        # self.generate_mines()

    def draw_difficulty_buttons(self):
        button_font = pygame.font.Font(None, 36)
        for i, (difficulty, params) in enumerate(DIFFICULTIES.items()):
            button_text = button_font.render(difficulty, True, BLACK)
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            pygame.draw.rect(self.screen, GRAY, button_rect.inflate(10, 10))
            self.screen.blit(button_text, button_rect)

    def choose_difficulty(self):
        while True:
            self.screen.fill(WHITE)
            self.draw_difficulty_buttons()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = event.pos
                        for i, (difficulty, params) in enumerate(DIFFICULTIES.items()):
                            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + i * 40 - 20, 200, 40)
                            if button_rect.collidepoint(mouse_x, mouse_y):
                                self.grid_size = params["grid_size"]
                                self.mine_count = params["mine_count"]
                                self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
                                self.generate_mines()
                                return

            self.clock.tick(30)

    
    def generate_mines(self):
        for _ in range(self.mine_count):
            row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            while (row, col) in self.mine_locations:
                row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            self.mine_locations.add((row, col))
            self.grid[row][col] = -1  # -1 represents a mine

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] != -1:
                    mines_nearby = sum(1 for r in range(max(0, row - 1), min(self.grid_size, row + 2))
                                       for c in range(max(0, col - 1), min(self.grid_size, col + 2))
                                       if self.grid[r][c] == -1)
                    self.grid[row][col] = mines_nearby

    def draw_grid(self):
        CELL_SIZE = WIDTH // self.grid_size
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x, y = col * CELL_SIZE, row * CELL_SIZE
                pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 2)
                if (row, col) in self.flags:
                    pygame.draw.polygon(self.screen, RED, [(x + CELL_SIZE // 2, y + 5), (x + 5, y + CELL_SIZE - 5),
                                                           (x + CELL_SIZE - 5, y + CELL_SIZE - 5)])

                if (row, col) in self.revealed_cells:
                    if self.grid[row][col] == -1:
                        pygame.draw.circle(self.screen, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
                    else:
                        font = pygame.font.Font(None, int(700 / self.grid_size))
                        text = font.render(str(self.grid[row][col]), True, COLOR_LIST[self.grid[row][col]])
                        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                        self.screen.blit(text, text_rect)
                        

    def reveal_cell(self, row, col):
        if (row, col) not in self.revealed_cells and (row, col) not in self.flags:
            self.revealed_cells.add((row, col))
            if self.grid[row][col] == 0:
                for r in range(max(0, row - 1), min(self.grid_size, row + 2)):
                    for c in range(max(0, col - 1), min(self.grid_size, col + 2)):
                        self.reveal_cell(r, c)

    def flag_cell(self, row, col):
        if (row, col) not in self.revealed_cells:
            if (row, col) in self.flags:
                self.flags.remove((row, col))
            else:
                self.flags.add((row, col))

    def check_game_status(self):
        if all(self.grid[row][col] == -1 or (row, col) in self.revealed_cells for row in range(self.grid_size) for col in range(self.grid_size)):
            self.end_game(True)  # All non-mine cells revealed, game won
        elif any((row, col) in self.mine_locations and (row, col) in self.revealed_cells for row in range(self.grid_size) for col in range(self.grid_size)):
            self.end_game(False)  # A mine cell is revealed, game lost

    def end_game(self, win):
        message = "Congratulations! You won!" if win else "Game over! You lost."
        font = pygame.font.Font(None, 68)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def run(self):
        CELL_SIZE = WIDTH // self.grid_size
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        col, row = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                        self.reveal_cell(row, col)
                    elif event.button == 3:  # Right mouse button
                        col, row = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                        self.flag_cell(row, col)

            self.screen.fill(GRAY_2)
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(30)
            self.check_game_status()

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
