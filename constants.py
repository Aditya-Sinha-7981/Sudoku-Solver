import numpy as np

# CONSTANTS

BOARD_SIZE = 900
CELL_SIZE = BOARD_SIZE//9
DESTINATION_COORDINATES = np.array([
    [0, 0],
    [BOARD_SIZE - 1, 0],
    [BOARD_SIZE - 1, BOARD_SIZE - 1],
    [0, BOARD_SIZE - 1]
], dtype="float32")
CONFIG = "--psm 6 -c tessedit_char_whitelist=123456789" #this config whitelists only numbers with single digits, currently not passing it to function from constants