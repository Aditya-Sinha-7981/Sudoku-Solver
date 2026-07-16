import numpy as np

GRID = [
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

def is_valid(row, col, number):
    global GRID
    valid = True
    reason = []
    for i in range(9):
        if number == GRID[row][i]:
            valid = False
            reason.append("Row")

    for j in range(9):
        if number == GRID[j][col]:
            valid = False
            reason.append("Column")

    box_row_index = (row // 3) * 3
    box_col_index = (col // 3) * 3
    print(box_row_index)
    print(box_col_index)

    for i in range(box_row_index, box_row_index+3):
        for j in range(box_col_index, box_col_index+3):
            if number == GRID[i][j]:
                valid = False
                reason.append("Box")

    print(valid)
    print(reason)

is_valid(8,4,3)


for number in range(1,10):
    print(number)


for number in (range(1,10)):
    print(number)