import tkinter as tk
from tkinter import ttk

from globalvar import *

def matrix_set(r, c, matrix):
    if matrix[r][c] == 0:
        matrix[r][c] = 1
    print_matrix(matrix)
    
def print_matrix(matrix):
    for row in matrix:
        print(row)

def check_win(matrix):
    pass
    
def play_move(r, c, matrix):
    matrix_set(r, c, matrix)
    check_win(matrix)