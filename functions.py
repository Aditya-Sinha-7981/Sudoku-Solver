import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import constants

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


def solve(grid, depth = 1):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                # count = 0
                for number in range(1,10):
                    if is_valid(grid, i, j, number):
                        grid[i][j] = number
                        # count += 1
                        solved = solve(grid, depth+1)
                        # technically I can directly put "if solve(grid, depth+1)" but I am gonna keep this as is for my future self's sanity
                        if solved:
                            return True
                        else:
                            grid[i][j] = 0
                # print(count)
                return
    print(f"Depth: {depth}")
    # print(np.matrix(grid))
    return True

# Note to my future self since I spent way too much time figuring this out: YOU ARE ALREADY CHANGING THE GRID, SO YOU ONLY RETURN "did you solve? yes or not", THE GRID IS ALREADY CHANGED WHEN YOU SOLVE
# THIS MEANS THE GRID THAT'S THE ANSWER WAS ALWAYS WITH YOU 
# If still confused, look at this
# lst = [3, 1, 2]

# result = lst.sort()

# print(result)
# print(lst)
# You changed the actual list, you do not care what function returned since actual list has already been changed



def solve_image(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_edged = cv2.Canny(gray_img, 30, 200)
    contoured_approx = image.copy()
    contours, hierarchy = cv2.findContours(gray_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    board_contour = max(contours, key=cv2.contourArea)

    # Opencv's drawCounters() expect a collection of contours but the max() function gave me one single contour's collection
    board_contour_list = [board_contour]
    # This line is not used but still here as a reminder

    approx = cv2.approxPolyDP(board_contour, 0.050 * cv2.arcLength(board_contour, True), True)
    cv2.drawContours(contoured_approx, [approx], -1, (0,0,255), 3)

    for index, point in enumerate(approx):
        x, y = point[0]
        cv2.circle(contoured_approx, (x, y), 8, (0,255,0), -1)
        # I used enumerate to basically get index, it's simply for loop but with index
        cv2.putText(contoured_approx, f"P{index} ({x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)


    ordered_coordinates = ordered_coords(approx)

    # now we get transformation matrix and then transform

    trans_mat = cv2.getPerspectiveTransform(ordered_coordinates, constants.DESTINATION_COORDINATES)
    final_img = cv2.warpPerspective(image, trans_mat, (constants.BOARD_SIZE, constants.BOARD_SIZE))


    cv2.imshow("Initial",image)

    cv2.imshow("Final Board", final_img)

    sudoku_grid = get_grid(final_img, constants.CELL_SIZE)
    print(sudoku_grid)

    ans = solve(sudoku_grid)
    if ans:
        print("We got answer")
        print(np.matrix(sudoku_grid))

    cv2.waitKey(0)

    cv2.destroyAllWindows()


def get_clipboard_image():
    image = ImageGrab.grabclipboard()
    print(image)
    image_array = np.array(image)
    print(type(image_array))
    final_img = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    return final_img

# ------------------------------------------------------------