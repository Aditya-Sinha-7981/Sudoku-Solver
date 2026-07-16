import cv2
import numpy as np
import constants
import functions as func

img = cv2.imread("distorted_board.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_edged = cv2.Canny(gray_img, 30, 200)

contoured = img.copy()
contoured_approx = img.copy()

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


ordered_coordinates = func.ordered_coords(approx)

# now we get transformation matrix and then transform

trans_mat = cv2.getPerspectiveTransform(ordered_coordinates, DESTINATION_COORDINATES)
final_img = cv2.warpPerspective(img, trans_mat, (BOARD_SIZE, BOARD_SIZE))


cv2.imshow("Initial",img)

cv2.imshow("Final Board", final_img)

sudoku_grid = func.get_grid(final_img, CELL_SIZE)
print(sudoku_grid)

ans = func.solve(sudoku_grid, False)
if ans:
    print("We got answer")
    print(np.matrix(sudoku_grid))


cv2.waitKey(0)

cv2.destroyAllWindows()



