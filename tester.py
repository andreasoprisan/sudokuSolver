from helpers import singleSudokuSolver 

input_string = '004300209005009001070060043006002087190007400050083000600000105003508690042910300'
array = singleSudokuSolver.array_input(input_string)

singleSudokuSolver.line_exclusion_method(array)
