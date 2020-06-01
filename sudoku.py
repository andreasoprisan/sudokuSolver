import numpy as np
import csv
import os
import time
import sys

sudoku_state = True
checker = [1,2,3,4,5,6,7,8,9]
clear = lambda: os.system('cls')


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

    for i in range (1,10): 
        count = 0
        for j in array:
            if j == i:
                count += 1
        if count == 1:
            result_array.append(i) 
    
    return result_array
    

def verify_single(coord):

    #Get ROW unique numbers:
    row_result = row_checker(coord)
    
    if show == 1 or show == 2:
        print("Row Result:", row_result)

    #Get COLUMN unique numbers:
    column_result = column_checker(coord)

    if show == 1 or show == 2:
        print("Column Result:", column_result)

    #Get BOX unique numbers:
    box_result = box_checker(coord)

    if show == 1 or show == 2:
        print("Box Result:", box_result)


    #Get Intersection in order to verify if there is a singular value
    unique_result = intersection(row_result, column_result, box_result)

    if show == 1 or show == 2:
        print("Unique result:", unique_result)

    if len(unique_result) == 1:
        if show == 1 or show == 2:
            print("Naked Single is:", unique_result[0])
        x[coord[0] - 1, coord[1] - 1] = unique_result[0]

    


def row_checker(coord):

    #Verifies uniquness of numbers in a given ROW

    #Take coords of ROW & column
    row, column = coord

    #Take ROW and flatten it in a 1D array
    row_contains = x[row-1:row].flatten()

    # Concatenating with all possible numbers in order to determine which moves are possible
    row_contains = np.concatenate((row_contains, checker))
    return unique_verifier(row_contains)

def column_checker(coord):

    #Verifies uniquness of numbers in a given COLUMN

    #Take coords of row & COLUMN
    row, column = coord
    

    #Take COLUMN and flatten it in a 1D array
    column_contains = x[:,column-1:column].flatten()

    #: Verify uniqueness of numbers inputed
    column_contains = np.concatenate((column_contains, checker))
    return unique_verifier(column_contains)

def box_checker(coord):

    #Verifies uniqueness of numbers in a given BOX

    #Get coords of unique BOX ROW
    row, column = coord
    if row >=1 and row <=3:
        box = (1,)
    if row >=4 and row <=6:
        box = (4,)
    if row >=7 and row <=9:
        box = (7,)

    #Get coords of unique BOX COLUMN
    if column >= 1 and column <=3:
        box = box + (1,)
    if column >= 4 and column <=6:
        box = box + (4,)
    if column >= 7 and column <=9:
        box = box + (7,)

    #Take upper left coord of unique BOX    
    box_row, box_column = box

    #Take BOX values and flatten them into 1D array

    box_values = []
    for i in range(3):
        for j in range(3):
            box_values.append(x[box_row + i - 1, box_column + j - 1])
    box_contains = np.array(box_values)
    box_contains = np.concatenate((box_contains, checker))
    

    return unique_verifier(box_contains)

def check_naked_singles():
    for i in range(1,10):
        for j in range(1,10):
            #print("\n")
            #print("I:", i, "J:", j)
            if x[i - 1, j - 1] == 0:
                verify_single((i, j))



def solve_quiz(x):
    

    while True:
        previous_sudoku_form = np.array(x, copy=True)
        check_naked_singles()

        if not np.any(x == 0):
            #Found the solution!
            break


        if np.array_equal(x, previous_sudoku_form):
            #Did not find the solution!  
            #print("\nThis is too hard even for me!")
            break
    
    return x

#MAIN
#Show 0: Silent
#Show 1: ALL
#Show 2: Every Step verification
#Show 3: Round Show
#Show 5: Show Solution for each quiz

show = 0


#Array input

#y = "100005007380900000600000480820001075040760020069002001005039004000020100000046352"
#x = array_input(y)
processed_quiz = 0
correct_quiz = 0
total_quiz = 0
calculate_ETA_after = 100
progress_refresh_rate = 50

with open('sudoku.csv') as csv_file:
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

            x = array_input(quiz)
            y = solve_quiz(x)
            resolved_quiz = array_output(y)

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

                if estimated_time_of_arrival > 60:
                    if estimated_time_of_arrival > 3600:
                        eta_hours = int(estimated_time_of_arrival) // 3600
                        eta_minutes = int(estimated_time_of_arrival) % 3600 // 60
                        eta_seconds = int(estimated_time_of_arrival) % 3600 % 60
                        print(f'ETA is: {eta_hours} hours, {eta_minutes} minutes and {eta_seconds} seconds!')
                    else:
                        eta_minutes = int(estimated_time_of_arrival) // 60
                        eta_hours = int(estimated_time_of_arrival) % 60
                        print(f'ETA is: {eta_minutes} minutes and {eta_seconds} seconds!')
                else:
                    print(f'ETA is: {estimated_time_of_arrival} seconds!')
        
    #clear()
    
    print(f'Progress is {(line_count) / total_quiz * 100}%!')

    timer_end = time.time()
    actual_time = timer_end - timer_start

    if actual_time > 60:
        if actual_time > 3600:
            actual_time_hours = int(actual_time) // 3600
            actual_time_minutes = int(actual_time) % 3600 // 60
            actual_time_seconds = int(actual_time) % 3600 % 60
            print(f'Actual time was: {actual_time_hours} hours, {actual_time_minutes} minutes and {actual_time_seconds} seconds!')
        else:
            actual_time_minutes = int(actual_time) // 60
            actual_time_seconds = int(actual_time) % 60
            print(f'Actual time was: {actual_time_minutes} minutes and {actual_time_seconds} seconds!')
    else:
        print(f'Actual time was: {actual_time} seconds!')
    

print(f'I have processed {processed_quiz} quizzes!')
print(f'I have found {correct_quiz} solutions!')
print(f'Solving Rate is {correct_quiz / processed_quiz * 100}%!')

#print("\nInitial Sudoku:\n")
#print (x)



#Array output
#string_solution = array_output(x)
#if solution_found == 1:
#    print("Solution is:", string_solution)



#while SudokuIsNotSolved:
 #   for i in range(9):
  #      for j in range(9):
   #         result = verify_single((i,j))
