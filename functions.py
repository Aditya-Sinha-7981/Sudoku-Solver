import cv2
import numpy as np

# ------------------------------------------------------------
# functions

def ordered_coords(coords):
    # create an empty array, make sure it's float32 since that's what openCV wants
    ordered = np.zeros((4,2), dtype="float32")
    
    # shape of coords is (4,1,2), we want (4,2) so we just remove the middle useless dimension(1)
    coords = np.squeeze(coords, axis=1)

    coord_sum = coords.sum(axis = 1)
    ordered[0] = coords[np.argmin(coord_sum)]
    ordered[2] = coords[np.argmax(coord_sum)]

    # np does y - x, not x - y
    coord_diff = np.diff(coords, axis = 1)
    ordered[1] = coords[np.argmin(coord_diff)]
    ordered[3] = coords[np.argmax(coord_diff)]

    return ordered



def final_points(coords):
    # This function is now technically redundant since we are using fixed size for destination
    (tl, tr, br, bl) = coords
    widthTop = np.linalg.norm(tl - tr)
    widthBottom = np.linalg.norm(bl - br)
    maxWidth = int(max(widthTop, widthBottom))

    heightLeft = np.linalg.norm(tl - bl)
    heightRight = np.linalg.norm(tr - br)
    maxHeight = int(max(heightLeft, heightRight))

    final_coords = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    
    return final_coords, maxWidth, maxHeight


def get_grid(board, cell_size):
    grayscale = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    ret, threshold_img = cv2.threshold(grayscale, 127, 255, cv2.THRESH_BINARY)
    margin = cell_size//10
    final_grid = []
    for row in range(9):
        row_values = []
        for col in range(9):
            y1 = row * cell_size + margin
            y2 = (row + 1) * cell_size - margin
            x1 = col * cell_size + margin
            x2 = (col + 1) * cell_size - margin
            cell = threshold_img[y1:y2, x1:x2]
            white_Pixels = cv2.countNonZero(cell)
            white_ratio = white_Pixels / cell.size #getting ratio of white pixels so it becomes dynamic
            if white_ratio < 0.95:
                number = 1
                pass #todo: add OCR for number
            else:
                number = 0
            row_values.append(number)
        final_grid.append(row_values)
    return final_grid


def get_digit(cell):
    pass

# ------------------------------------------------------------