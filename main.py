import cv2
import numpy as np
import constants
import functions as func

# img = cv2.imread("image/distorted_board.png")
# func.solve_image(img)

while True:
    print("\n===== Sudoku Solver =====")
    print("1. Load image from clipboard")
    print("2. Display detected board")
    print("3. Solve current board")
    print("q. Quit")

    choice = input("Select an option: ").strip().lower()

    match choice:
        case "1":
            image = func.get_clipboard_image()
            board_image = func.get_sudoku_board(image)

        case "2":
            func.display_image(board_image, "Sudoku Board")

        case "3":
            func.solve_image(board_image)

        case "q":
            print("Goodbye!")
            break

        case _:
            print("Invalid option. Please try again.")


