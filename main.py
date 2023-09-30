#
# @title Minesweeper
# 
# @author Henry Bobeck
# @date 230929
#
#

import pygame
import random
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 750
COLS, ROWS = 15, 15
BOMBS = 30
FONT = pygame.font.SysFont("Comic Sans", 20)
GRID_COLORS = {-1: "red", 0: (200, 200, 200), 1: "black", 2: "blue", 3: "yellow", 4: "purple", 5: "orange", 6: "red", 7: "green", 8: "pink"}
COVER_GRID_COLORS = {0: None, 1: (100, 100, 100), 2: "green"}


class Game():


    def __init__(self, window, cols = COLS, rows = ROWS, bombs = BOMBS):
        self.window = window
        self.cols = cols
        self.rows = rows
        self.bombs = BOMBS
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        self.cover_grid = [[1 for col in range(self.cols)] for row in range(self.rows)]
        self.SQR_SIZE = SCREEN_WIDTH // self.cols
        self.run = True
        self.victorious = False
        self.clicks = 0

    # generates the grid based on the location of the first clicked square
    def generate_grid(self, row_clicked, col_clicked):
        # place bombs
        bombs_left = self.bombs
        while bombs_left > 0:
            row, col = random.randrange(self.cols), random.randrange(self.rows)
            # only place bombs outside of initial click and its neighbors
            neighbors = self.get_neighbors(row, col)
            if self.grid[row][col] == -1 or (row, col) == (row_clicked, col_clicked) or (row_clicked, col_clicked) in neighbors:
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
            neighbors.append((row-1, col-1))
        if row > 0:
            neighbors.append((row-1, col))
        if row > 0 and col < self.cols-1:
            neighbors.append((row-1, col+1))
        if col > 0:
            neighbors.append((row, col-1))
        if col < self.cols-1:
            neighbors.append((row, col+1))
        if row < self.rows-1 and col > 0:
            neighbors.append((row+1, col-1))
        if row < self.rows-1:
            neighbors.append((row+1, col))
        if row < self.rows-1 and col< self.cols-1:
            neighbors.append((row+1, col+1))
        return neighbors

    # reveal everything and end the game
    # type: 1 (win), 0 (loss)
    def game_over(self, type):
        if type == 1:
            self.victorious = True
        else:
            # uncover everything
            self.cover_grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        
        self.draw()
        # wait 3 seconds
        pygame.time.delay(3000)
        # flag for game loop to end
        self.run = False

    def check_victory(self):
        for row in range(self.rows):
            for col in range(self.cols):
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
            row, col = int(y // self.SQR_SIZE), int(x // self.SQR_SIZE)
            if row < self.rows and col < self.cols: # if click is in the grid
                if button == 1: # left click
                    print(f"clicked {row}, {col}")
                    self.clicks += 1

                    if self.clicks == 1: # if first click, generate grid
                        self.generate_grid(row, col)
                        self.uncover_square(row, col)
                        self.check_victory()
                    elif self.cover_grid[row][col] == 2: # flagged
                        self.cover_grid[row][col] = 1
                    elif self.grid[row][col] == -1: # bomb
                        print("Bomb clicked, game over")
                        self.game_over(0)
                    else:
                        self.uncover_square(row, col)
                        self.check_victory()
                        
                elif button == 3: # right click
                    if self.cover_grid[row][col] == 1: # covered
                        self.cover_grid[row][col] = 2



    # draw the display
    def draw(self):
        # draw background
        self.window.fill("white") 

        # draw the grid
        for row in range(self.rows):
            y = self.SQR_SIZE * row
            for col in range(self.cols):
                gv = self.grid[row][col]
                cgv = self.cover_grid[row][col]
                x = self.SQR_SIZE*col
                # draw background outline
                pygame.draw.rect(self.window, "black", (x, y, self.SQR_SIZE, self.SQR_SIZE))
                if cgv != 0: # covered
                    pygame.draw.rect(self.window, COVER_GRID_COLORS[cgv], (x+1, y+1, self.SQR_SIZE-2, self.SQR_SIZE-2))
                else: # uncovered
                    if gv == -1: # bomb
                        pygame.draw.rect(self.window, GRID_COLORS[gv], (x+1, y+1, self.SQR_SIZE-2, self.SQR_SIZE-2))
                    else: # numbers
                        pygame.draw.rect(self.window, GRID_COLORS[0], (x+1, y+1, self.SQR_SIZE-2, self.SQR_SIZE-2))
                        # draw number text
                        if gv != 0:
                            text = FONT.render(str(gv), 1, GRID_COLORS[gv])
                            self.window.blit(text, (x + (self.SQR_SIZE // 2 - text.get_width()/2), y + (self.SQR_SIZE // 2 - text.get_height()/2)))
                    
        # draw victory text
        if self.victorious:
            text_victory = FONT.render("Congratulations! You Won", 1, "green")
            self.window.blit(text_victory, (SCREEN_WIDTH // 2 - text_victory.get_width()//2, SCREEN_HEIGHT // 2 - text_victory.get_height()//2))

        # refresh display
        pygame.display.update() 

        
    def start(self):
        self.clicks = 0
        self.victorious = False
        self.run = True
        while self.run:
            for event in pygame.event.get():
                    # quit
                    if event.type == pygame.QUIT:
                        self.run = False
                    # mouse
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.click_handler(event.pos, event.button)

            self.draw()
            


def main():
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    

    game = Game(win)
    game.start()

    pygame.quit()
    quit()
        

if __name__ == "__main__":
  main()