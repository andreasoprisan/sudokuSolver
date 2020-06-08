from helpers import singleSudokuSolver 

input_string = '400870090092000487078090100060059748980040000705680930009020810817900250000018079'
array = singleSudokuSolver.array_input(input_string)

for i in range(5):
    array = singleSudokuSolver.line_exclusion_method(array)
print(array)

for i in range(5):
    array = singleSudokuSolver.check_naked_singles(array)
print(array)