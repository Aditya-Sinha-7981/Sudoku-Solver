import cv2
import numpy as np
import constants
import functions as func

# img = cv2.imread("image/distorted_board.png")
# func.solve_image(img)

image = func.get_clipboard_image()

func.solve_image(image)