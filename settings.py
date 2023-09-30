# screen and grid dimensions
SQR_SIZE = 40
COLS, ROWS = 15, 15
BOMBS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = COLS * SQR_SIZE, ROWS * SQR_SIZE

# colors
GRID_COLORS = {
    -1: "red",
    0: (200, 200, 200),
    1: "black",
    2: "blue",
    3: "yellow",
    4: "purple",
    5: "orange",
    6: "red",
    7: "green",
    8: "pink",
}
COVER_GRID_COLORS = {0: None, 1: (100, 100, 100), 2: "green"}
