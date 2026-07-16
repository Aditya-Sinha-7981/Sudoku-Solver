import cv2
import numpy as np
import pytesseract

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
                number = int((get_digit(cell)).strip())
            else:
                number = 0
            row_values.append(number)
        final_grid.append(row_values)
    return final_grid


def get_digit(cell):
    extracted_num = pytesseract.image_to_string(cell, config="--psm 6 -c tessedit_char_whitelist=123456789")
    return extracted_num


def is_valid(grid, row, col, number):
    for i in range(9):
        if number == grid[row][i]:
            return False

    for j in range(9):
        if number == grid[j][col]:
            return False

    box_row_index = (row // 3) * 3
    box_col_index = (col // 3) * 3

    for i in range(box_row_index, box_row_index+3):
        for j in range(box_col_index, box_col_index+3):
            if number == grid[i][j]:
                return False

    return True


def solve(grid, solved, depth = 1):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                # count = 0
                for number in range(1,10):
                    if is_valid(grid, i, j, number):
                        grid[i][j] = number
                        # count += 1
                        solved = solve(grid,solved, depth+1)
                        if solved == True:
                            return True
                        else:
                            grid[i][j] = 0
                # print(count)
                return
    print(depth)
    print(np.matrix(grid))
    solved = True
    return solved

# Note to my future self since I spent way too much time figuring this out: YOU ARE ALREADY CHANGING THE GRID, SO YOU ONLY RETURN "did you solve? yes or not", THE GRID IS ALREADY CHANGED WHEN YOU SOLVE
# THIS MEANS THE GRID THAT'S THE ANSWER WAS ALWAYS WITH YOU 
# If still confused, look at this
# lst = [3, 1, 2]

# result = lst.sort()

# print(result)
# print(lst)
# You changed the actual list, you do not care what function returned since actual list has already been changed

# ------------------------------------------------------------