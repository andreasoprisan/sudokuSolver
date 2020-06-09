from helpers import singleSudokuSolver
import pandas as pd 
import time

input_string = '400870090092000487078090100060059748980040000705680930009020810817900250000018079'
array = singleSudokuSolver.array_input(input_string)


start = time.time()
chunksize = 10000
for chunk in pd.read_csv("data/sudoku.csv", chunksize=chunksize, nrows=10000):
    

    print(pd.value_counts(chunk['solutions'].eq(chunk['quizzes'].apply(singleSudokuSolver.solve_quiz))))

end = time.time()
print(end-start)