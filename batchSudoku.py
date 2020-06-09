#IMPORTS
import numpy as np
import pandas as pd
import csv
import os
import time
import sys
from helpers import timeDisplay
from helpers import singleSudokuSolver

#DEFINES
sudoku_state = True
clear = lambda: os.system('cls')
show = 0
script_dir = os.path.dirname(__file__)

#MAIN

#SETTINGS
processed_quiz = 0
correct_quiz = 0
total_quiz = 100001
calculate_ETA_after = 100
progress_refresh_rate = 50
filename = "sudoku.csv"
data_dir_name = "data"
number_of_processes = 4

with open(f'{script_dir}{data_dir_name}/{filename}') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    
    clear()

    #Determine the total number of rows
    
    csv_row_count = sum(1 for row in csv_reader)
    if total_quiz == 0:
        quizzes_to_be_processed = 'all'
        total_quiz = csv_row_count
    else:
        quizzes_to_be_processed = total_quiz
    print(f'The provided CSV contains {csv_row_count} rows. Of those, {quizzes_to_be_processed} will be processed!')

    csv_file.seek(0)
    timer_start = time.time()
    
    
    for row in csv_reader:
        if line_count == total_quiz:
            break

        if line_count == 0:
            #First line contains info about column names
            #print(f'Column names are {", ".join(row)}')
            line_count += 1

        else:
            quiz = row[0]
            solution = row[1]

            #Get string result from string input quiz
            resolved_quiz = singleSudokuSolver.solve_quiz(quiz)
            
            if show == 1 or show == 5:
                print("Solution:", solution)
                print("Found by program:\n", resolved_quiz)

            if solution == resolved_quiz:
                correct_quiz += 1

            processed_quiz += 1
            line_count += 1

        if line_count % progress_refresh_rate == 0:
            
            print(f'Progress is {(line_count - 1) / total_quiz * 100}%!',end='\r')

            if line_count == calculate_ETA_after:
                timer_current = time.time()
                time_elapsed = timer_current - timer_start
                estimated_time_of_arrival = time_elapsed * (total_quiz / calculate_ETA_after)

                #Print ETA
                #1.2.2 TimeDisplay function added
                timeDisplay.display(estimated_time_of_arrival, "ETA")        
    #clear()
    
    print(f'Progress is {(line_count) / total_quiz * 100}%!')

    timer_end = time.time()
    actual_time = timer_end - timer_start

    #Print Actual Elapsed time
    #1.2.2 TimeDisplay function added
    timeDisplay.display(actual_time, "Actual Time")
    

print(f'I have processed {processed_quiz} quizzes!')
print(f'I have found {correct_quiz} solutions!')
print(f'Solving Rate is {correct_quiz / processed_quiz * 100}%!')
