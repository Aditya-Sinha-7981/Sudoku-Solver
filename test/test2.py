import cv2
import numpy as np


img = cv2.imread("board.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_edged = cv2.Canny(gray_img, 30, 200)
ret, threshold_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

contoured = img.copy()
contoured_approx = img.copy()
all_rect = img.copy()

contours, hierarchy = cv2.findContours(gray_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

board_contour = max(contours, key=cv2.contourArea)

# Opencv's drawCounters() expect a collection of contours but the max() function gave me one single contour's collection
board_contour_list = [board_contour]

cv2.drawContours(contoured, contours, -1, (0,255,0), 3)

approx = cv2.approxPolyDP(board_contour, 0.050 * cv2.arcLength(board_contour, True), True)
cv2.drawContours(contoured_approx, [approx], -1, (0,0,255), 3)

print(approx.shape)
print(approx[0].shape)
print(approx[1])
print(approx)

# functions

def ordered_coords(coords):
    ordered = np.zeros((4,2), dtype="float32")
    print(ordered)
    
    coords = np.squeeze(coords, axis=1)

    print(coords)

    coord_sum = coords.sum(axis = 1)

    ordered[0] = coords[np.argmin(coord_sum)]
    ordered[2] = coords[np.argmax(coord_sum)]

    coord_diff = np.diff(coords, axis = 1)
    ordered[1] = coords[np.argmin(coord_diff)]
    ordered[3] = coords[np.argmax(coord_diff)]

    print(ordered)






# ordered_coords(approx) 

cv2.imshow("Sudoku Board",img)
cv2.imshow("Gray Edge", gray_img)
cv2.imshow("Gray Edge", gray_edged)
cv2.imshow("Contoured", contoured)
cv2.imshow("Threshold", threshold_img)
# cv2.imshow("Approx", contoured_approx)


cv2.waitKey(0)

cv2.destroyAllWindows()