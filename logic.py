import numpy as np
from scipy import signal
from io import StringIO
import screeninfo

def check_grid(mtrx):

    kernel = np.array([[1, 1, 1, ],
                       [1, 0, 1],
                       [1, 1, 1]])
    new_game = signal.convolve2d(mtrx, kernel, mode='same')
    alive = mtrx == 1

    first_factor = np.logical_or(new_game == 2, new_game == 3)
    result1 = np.logical_and(alive, first_factor)

    dead = mtrx == 0
    second_factor = new_game == 3
    
    resurrect = np.logical_and(dead, second_factor)
    mtrx = (np.logical_or(resurrect, result1)).astype(int)
    return mtrx

def matrix_dimensions(ROW_COUNT, COLUMN_COUNT,HEIGHT, WIDTH, MARGIN):

    SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
    SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN + 75
    return SCREEN_WIDTH, SCREEN_HEIGHT

def read_pattern(filename):

    with open(f"sample_patterns/{filename}.txt") as file:
        matrix = file.read()
        matrix = " ".join(matrix)
        matrix = StringIO(matrix)

    data = np.loadtxt(matrix, ndmin=2, dtype='str')
    new_matrix = data != "."

    new_matrix = new_matrix.astype(int)
    return new_matrix

def adjust_to_screen(WIDTH_cell, HEIGHT_cell, MARGIN):

    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height
    number_column = int((width -(WIDTH_cell/2 + MARGIN))/(WIDTH_cell + MARGIN))
    number_row = int((height -(HEIGHT_cell/2 + MARGIN + 75))/(HEIGHT_cell + MARGIN))
    return number_column, number_row
