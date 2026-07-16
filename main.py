import cv2
import numpy as np
import constants
import functions as func

board_image = None
unsolved_grid = None
solved_grid = None

while True:
    print("\n===== Sudoku Solver =====")
    print("1. Load image from clipboard")
    print("2. Display detected board")
    print("3. Solve current board")
    print("4. Create the solution's image and display it")
    print("q. Quit")

    choice = input("Select an option: ").strip().lower()

    match choice:
        case "1":
            image = func.get_clipboard_image()
            board_image = func.get_sudoku_board(image)

        case "2":
            func.display_image_opencv(board_image, "Sudoku Board")

        case "3":
            unsolved_grid, solved_grid = func.solve_image(board_image)
            print(np.matrix(solved_grid))

        case "4":
            if unsolved_grid is None:
                unsolved_grid, solved_grid = func.solve_image(board_image)
            solved_image = func.draw_solution(board_image, unsolved_grid, solved_grid)
            cv2.imwrite("Solved_Sudoku_Board.png", solved_image)
            func.display_image_system(solved_image, "Solved Sudoku Board")

        case "q":
            print("Goodbye!")
            break

        case _:
            print("Invalid option. Please try again.")


