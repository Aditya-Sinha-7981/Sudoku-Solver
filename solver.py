import numpy as np

SUDOKU_GRID = [
    [0,0,8,0,0,0,0,1,6],
    [5,0,0,0,9,2,0,0,8],
    [0,0,0,1,0,0,0,0,0],
    [9,0,0,3,0,0,8,2,0],
    [0,2,0,0,0,0,0,7,0],
    [0,8,4,0,0,6,0,0,5],
    [0,0,0,0,0,3,0,0,0],
    [4,0,0,9,6,0,0,0,2],
    [1,6,0,0,0,0,7,0,0]
]

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
                        solve(grid, depth+1)
                        grid[i][j] = 0
                # print(count)
                return
    print(depth)
    print(np.matrix(grid))

    return np.matrix(grid)
            
# solve(SUDOKU_GRID)
