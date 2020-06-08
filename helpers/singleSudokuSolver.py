# IMPORTS
import numpy as np

# DEFINE
checker = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Show 0: Silent
# Show 1: ALL
# Show 2: Every Step verification
# Show 3: Round Show
# Show 5: Show Solution for each quiz
show = 0

# FUNCTIONS


def array_input(string_input):
    separator = ","
    z = separator.join(string_input)
    t = np.array(z.split(','))
    t.shape = (9, 9)
    x = t.astype(int)
    return x


def array_output(matrix_input):
    separator = ""
    string_matrix = matrix_input.astype(str)
    flattened_string_matrix = string_matrix.flatten()
    final_string = separator.join(flattened_string_matrix)
    return final_string


def intersection(lst1, lst2, lst3):
    lst4 = [value for value in lst1 if value in lst2 if value in lst3]
    return lst4


def unique_verifier(array):

    result_array = []

    for i in range(1, 10):
        count = 0
        for j in array:
            if j == i:
                count += 1
        if count == 1:
            result_array.append(i)

    return result_array


def verify_single(coord, x):

    # Get ROW unique numbers:
    row_result = row_checker(coord, x)

    if show == 1 or show == 2:
        print("Row Result:", row_result)

    # Get COLUMN unique numbers:
    column_result = column_checker(coord, x)

    if show == 1 or show == 2:
        print("Column Result:", column_result)

    # Get BOX unique numbers:
    box_result = box_checker(coord, x)

    if show == 1 or show == 2:
        print("Box Result:", box_result)

    # Get Intersection in order to verify if there is a singular value
    unique_result = intersection(row_result, column_result, box_result)

    if show == 1 or show == 2:
        print("Unique result:", unique_result)

    if len(unique_result) == 1:
        if show == 1 or show == 2:
            print("Naked Single is:", unique_result[0])
        return unique_result[0]
    else:
        return 0


def row_checker(coord, x):

    # Verifies uniquness of numbers in a given ROW

    # Take coords of ROW & column
    row, column = coord

    # Take ROW and flatten it in a 1D array
    row_contains = x[row-1:row].flatten()

    # Concatenating with all possible numbers in order to determine which moves are possible
    row_contains = np.concatenate((row_contains, checker))
    return unique_verifier(row_contains)


def column_checker(coord, x):

    # Verifies uniquness of numbers in a given COLUMN

    # Take coords of row & COLUMN
    row, column = coord

    # Take COLUMN and flatten it in a 1D array
    column_contains = x[:, column-1:column].flatten()

    #: Verify uniqueness of numbers inputed
    column_contains = np.concatenate((column_contains, checker))
    return unique_verifier(column_contains)


def box_checker(coord, x):

    # Verifies uniqueness of numbers in a given BOX

    # Get coords of unique BOX ROW
    row, column = coord
    if row >= 1 and row <= 3:
        box = (1,)
    if row >= 4 and row <= 6:
        box = (4,)
    if row >= 7 and row <= 9:
        box = (7,)

    # Get coords of unique BOX COLUMN
    if column >= 1 and column <= 3:
        box = box + (1,)
    if column >= 4 and column <= 6:
        box = box + (4,)
    if column >= 7 and column <= 9:
        box = box + (7,)

    # Take upper left coord of unique BOX
    box_row, box_column = box

    # Take BOX values and flatten them into 1D array

    box_values = []
    for i in range(3):
        for j in range(3):
            box_values.append(x[box_row + i - 1, box_column + j - 1])
    box_contains = np.array(box_values)
    box_contains = np.concatenate((box_contains, checker))

    return unique_verifier(box_contains)


def check_naked_singles(x):

    for i in range(1, 10):
        for j in range(1, 10):
            # print("\n")
            #print("I:", i, "J:", j)
            if x[i - 1, j - 1] == 0:
                x[i - 1, j - 1] = verify_single((i, j), x)
    return x


def solve_quiz(input_string):

    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Get input matrix
    x = array_input(input_string)

    while True:

        # Get current form in order to compare with previous form
        previous_sudoku_form = np.array(x, copy=True)

        # Get updated matrix using naked singles method

        # Main Method
        x = line_exclusion_method(x, digits)

        if not np.any(x == 0):
            # Found the solution!
            break

        if np.array_equal(x, previous_sudoku_form):
            # Did not find the solution!
            # Backup Method

            x = check_naked_singles(x)

            if np.array_equal(x, previous_sudoku_form):
                # Did not found the solution even after backup method
                break

    string_array = array_output(x)
    return string_array

# LINE EXCLUSION METHOD


def line_exclusion_method(array, digits):

    for number in digits:
        for x in range(3):
            for y in range(3):

                line = x * 3
                column = y * 3

                # Get Square Copy
                square = array[line:line+3, column:column+3].copy()

                # Verify if number already exists

                if np.any(square == number):
                    continue
                # Set -1 where spot is taken
                square = np.where(square == 0, 0, -1)

                # Check ROWS
                for i in range(line, line + 3):
                    if np.any(array[i, :] == number):
                        square[i - line, :] = -1

                # Check COLUMNS
                for i in range(column, column + 3):
                    if np.any(array[:, i] == number):
                        square[:, i - column] = -1

                # Verify if unique, get index of unique & update matrix
                if np.count_nonzero(square == 0) == 1:
                    index_x, index_y = np.where(square == 0)
                    index_x = index_x[0]
                    index_y = index_y[0]
                    array[index_x + line, index_y + column] = number
        if np.count_nonzero(array == number) == 9:
            digits.remove(number)
    return(array)
