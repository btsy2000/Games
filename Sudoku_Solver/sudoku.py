def find_next_empty(puzzle):
    # finds the next rwo, col on the puzzle that's not filled yet --> rep with -1
    # return row, col tuple (or (None, None) if there is none)

    # keep in mind that we are using 0-8 for our indices
    for r in range(9):
        for c in range(9): # range(9) is 0, 1, 2, ... 8
            if puzzle[r][c] <= 0:
                return r, c

    return None, None # if no spaces in the puzzle are empty (-1)

def is_valid(puzzle, guess, row, col):
    # figures out whhether the guess at the row/col of the puzzle is a valid puess
    # returns True if is valid, False otherwise

    # let's start with the row:
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    # now the colume 
    # col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i][col])
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
        
    # and then the square
    # this is tricky, but we want to get where the 3x3 square starts
    # and iterate over the 3 values in the row/column
    row_start = (row // 3) * 3  # 1 // 3 = 0, 5 //3 = 1, ...
    col_start = (col // 3) * 3  # 1

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    # if we get here, these checks pass
    return True


def solve_sudoku(puzzle):
    # solve sudoku using backtracking!
    # for puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # return whether a solution exists
    # mutates puzzle to be the solution (if solution exists)

    # step 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # step 1.1: if there's nowhere left, then we're done because we only allowed valid inputs
    if row is None:
        return True

    # step 2: if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1, 10):  # range(1, 10) is 1, 2, 3, ... 9
        # step 3: check if thsi is valid guess
        if is_valid(puzzle, guess, row, col):
            # step 3.1: if this is valid, then place that guess on the puzzle!
            puzzle[row][col] = guess
            # new recurse using this puzzle!
            # step 4: recursively call out function
            if solve_sudoku(puzzle):
                return True

        # step 5: if not valid OR if our guess does not solve the puzzle, then we need to 
        # backtrack and try a new number
        puzzle[row][col] = -1 # reest the guess

    # step 6: if none of the numbers we try work, then this puzzle is UNSOLVABLE!!
    return False

def is_valid2(puzzle, guess, row, col):
    if guess in puzzle[row]:
        return False

    if guess in [puzzle[i][col] for i in range(9)]:
        return False 
    s_r = (row // 3)*3
    s_l = (col // 3)*3
    # for r in range(s_r, s_r+3):
    #     for c in range(s_l, s_l+3):
    #         if puzzle[r][c] == guess:
    #             return False
    if guess in [puzzle[r][l] for r in range(s_r, s_r+3) for l in range(s_l, s_l+3)]:
        return False
    return True    

def solve_sudoku_changed(puzzle):

    row, col = find_next_empty(puzzle) 
    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid2(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku_changed(puzzle):
                return True    
        puzzle[row][col] = -1
    return False

if __name__ == '__main__':
    # example_board = [
    #     [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
    #     [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
    #     [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

    #     [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
    #     [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
    #     [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

    #     [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
    #     [6, 7, -1,   1, -1, 5,   -1, 4, -1],
    #     [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    # ]    
    example_board = [
        [-1, 3, -1,   1, 8, -1,   -1, 5, -1],
        [-1, -1, -1,   -1, -1, 4,   -1, -1, -1],
        [7, -1, -1,   -1, -1, -1,   -1, -1, 9],

        [-1, 8, -1,   2, 5, -1,   -1, 1, -1],
        [-1, -1, -1,   -1, 6, -1,   -1, -1, -1],
        [-1, -1, 3,   -1, -1, -1,   8, -1, -1],

        [-1, 2, -1,   -1, -1, 6,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, 3,   -1, 4, -1],
        [-1, -1, 9,   4, 2, -1,   -1, -1, 5]
    ] 
    print(solve_sudoku_changed(example_board))
    print(example_board)


