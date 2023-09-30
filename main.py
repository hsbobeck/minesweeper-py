#
# @title Minesweeper
#
# @author Henry Bobeck
# @date 230929
#
#

import pygame
import random
from settings import *

pygame.init()

FONT = pygame.font.SysFont("Comic Sans", 20)


class Game:
    def __init__(self, window):
        self.window = window
        self.grid = [[0 for col in range(COLS)] for row in range(ROWS)]
        self.cover_grid = [[1 for col in range(COLS)] for row in range(ROWS)]
        self.run = True
        self.victorious = False
        self.clicks = 0

    # generates the grid based on the location of the first clicked square
    def generate_grid(self, row_clicked, col_clicked):
        # place bombs
        bombs_left = BOMBS
        while bombs_left > 0:
            row, col = random.randrange(COLS), random.randrange(ROWS)
            # only place bombs outside of initial click and its neighbors
            neighbors = self.get_neighbors(row, col)
            if (
                self.grid[row][col] == -1  # don't place bombs on top of each other
                or (row, col) == (row_clicked, col_clicked)
                or (row_clicked, col_clicked) in neighbors
            ):
                continue
            else:
                # place bomb here
                self.grid[row][col] = -1
                bombs_left -= 1
                # update surrounding values
                for r, c in neighbors:
                    if self.grid[r][c] > -1:
                        self.grid[r][c] += 1

    # return a list of all valid neighbors in the form of tuples (row, col)
    def get_neighbors(self, row, col):
        neighbors = []
        if row > 0 and col > 0:
            neighbors.append((row - 1, col - 1))
        if row > 0:
            neighbors.append((row - 1, col))
        if row > 0 and col < COLS - 1:
            neighbors.append((row - 1, col + 1))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < COLS - 1:
            neighbors.append((row, col + 1))
        if row < ROWS - 1 and col > 0:
            neighbors.append((row + 1, col - 1))
        if row < ROWS - 1:
            neighbors.append((row + 1, col))
        if row < ROWS - 1 and col < COLS - 1:
            neighbors.append((row + 1, col + 1))
        return neighbors

    # reveal everything and end the game
    # type: 1 (win), 0 (loss)
    def game_over(self, type):
        if type == 1:
            self.victorious = True
        else:
            # uncover everything
            self.cover_grid = [[0 for col in range(COLS)] for row in range(ROWS)]

        self.draw()
        # wait 3 seconds
        pygame.time.delay(3000)
        # flag for game loop to end
        self.run = False

    def check_victory(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.cover_grid[row][col] != 0 and self.grid[row][col] > -1:
                    # not victorious yet
                    return

        # victorious
        self.game_over(1)

    # uncovers the given safe square and any applicable neighbors
    def uncover_square(self, row, col):
        self.cover_grid[row][col] = 0
        if self.grid[row][col] == 0:
            for sqr in self.get_neighbors(row, col):
                r, c = sqr[0], sqr[1]
                if self.grid[r][c] == 0 and self.cover_grid[r][c] == 1:
                    self.uncover_square(*sqr)
                if self.grid[r][c] > 0 and self.cover_grid[r][c] == 1:
                    self.cover_grid[r][c] = 0

    def click_handler(self, pos, button):
        x, y = pos
        row, col = int(y // SQR_SIZE), int(x // SQR_SIZE)
        if row < ROWS and col < COLS:  # if click is in the grid
            if button == 1:  # left click
                print(f"clicked {row}, {col}")
                self.clicks += 1

                if self.clicks == 1:  # if first click, generate grid
                    self.generate_grid(row, col)
                    self.uncover_square(row, col)
                    self.check_victory()
                elif self.cover_grid[row][col] == 2:  # flagged
                    self.cover_grid[row][col] = 1
                elif self.grid[row][col] == -1:  # bomb
                    print("Bomb clicked, game over")
                    self.game_over(0)
                else:
                    self.uncover_square(row, col)
                    self.check_victory()

            elif button == 3:  # right click
                if self.cover_grid[row][col] == 1:  # covered
                    self.cover_grid[row][col] = 2

    # draw the display
    def draw(self):
        # draw background
        self.window.fill("white")

        # draw the grid
        for row in range(ROWS):
            y = SQR_SIZE * row
            for col in range(COLS):
                gv = self.grid[row][col]
                cgv = self.cover_grid[row][col]
                x = SQR_SIZE * col
                # draw background outline
                pygame.draw.rect(self.window, "black", (x, y, SQR_SIZE, SQR_SIZE))
                if cgv != 0:  # covered
                    pygame.draw.rect(
                        self.window,
                        COVER_GRID_COLORS[cgv],
                        (x + 1, y + 1, SQR_SIZE - 2, SQR_SIZE - 2),
                    )
                else:  # uncovered
                    if gv == -1:  # bomb
                        pygame.draw.rect(
                            self.window,
                            GRID_COLORS[gv],
                            (x + 1, y + 1, SQR_SIZE - 2, SQR_SIZE - 2),
                        )
                    else:  # numbers
                        pygame.draw.rect(
                            self.window,
                            GRID_COLORS[0],
                            (x + 1, y + 1, SQR_SIZE - 2, SQR_SIZE - 2),
                        )
                        # draw number text
                        if gv != 0:
                            text = FONT.render(str(gv), 1, GRID_COLORS[gv])
                            self.window.blit(
                                text,
                                (
                                    x + (SQR_SIZE // 2 - text.get_width() / 2),
                                    y + (SQR_SIZE // 2 - text.get_height() / 2),
                                ),
                            )

        # draw victory text
        if self.victorious:
            text_victory = FONT.render("Congratulations! You Won", 1, "green")
            self.window.blit(
                text_victory,
                (
                    SCREEN_WIDTH // 2 - text_victory.get_width() // 2,
                    SCREEN_HEIGHT // 2 - text_victory.get_height() // 2,
                ),
            )

        # refresh display
        pygame.display.flip()

    def start(self):
        self.clicks = 0
        self.victorious = False
        self.run = True
        while self.run:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click_handler(event.pos, event.button)

            self.draw()


def main():
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    playing = True
    while playing:
        game = Game(win)
        game.start()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
