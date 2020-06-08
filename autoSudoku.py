#IMPORTS
from PIL import Image
from PIL import ImageGrab
from helpers import singleSudokuSolver
import numpy as np
import cv2 as cv
import keyboard
import pyautogui

#FUNCTIONS

#STARTER
def solve_puzzle():
    quiz_screenshot = get_quiz_screenshot()
    sudoku_array = np.zeros((9,9), dtype=int)
    
    for i in range(1,10):
        sudoku_array = process_templates(quiz_screenshot, i, sudoku_array)

    sudoku_array_string = array_to_string(sudoku_array)
    solved_sudoku = singleSudokuSolver.solve_quiz(sudoku_array_string) 

    sudoku_iterator(solved_sudoku)

#GET_SUDOKU
def get_quiz_screenshot():
    a = ImageGrab.grab(bbox=(808,294,1752,1239))
    opencvImage = cv.cvtColor(np.array(a), cv.COLOR_RGB2BGR)
    return opencvImage

def process_templates(image, number, sudoku_array):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    threshold = 0.85
    template = cv.imread(f"template_{number}.png", 0)
    w, h = template.shape[::-1]

    output = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)

    position = np.where(output >= threshold)
    for point in zip(*position[::-1]): 
        #cv.rectangle(image, point, (point[0] + w, point[1] + h), 0, 2)
        coords = (point[0] + w/2, point[1] + h/2)
        
        x, y = get_matrix_place_from_coords(coords)
        
        sudoku_array[x, y] = number

    return sudoku_array


    #cv.imshow(f"Matched {number}", image)
    #cv.waitKey(0)
    #cv.destroyAllWindows()

def get_matrix_place_from_coords(coords):
    x = int(coords[1] // 105)
    y = int(coords[0] // 105)

    return (x, y)

#PRETTIFY
def array_to_string(matrix_input):
    separator = ""
    string_matrix = matrix_input.astype(str)
    flattened_string_matrix = string_matrix.flatten()
    final_string = separator.join(flattened_string_matrix)
    return final_string

def string_to_array(string_input):
    separator = ","
    z = separator.join(string_input)
    t = np.array(z.split(','))
    t.shape = (9, 9) 
    x = t.astype(int)
    return x

#AUTOMATED MOVEMENT

def sudoku_iterator(string_array):
    array = string_to_array(string_array)
    print(string_array)
    

    for i in range(9):
        for j in range(9):
            pyautogui.press('right')
            pyautogui.press(f'{array[i, j]}')
        pyautogui.press('down')    

#MAIN    
keyboard.add_hotkey('F2', lambda:solve_puzzle())
keyboard.wait('esc')