import tkinter as tk
from tkinter import ttk

from globalvar import *

def matrix_set(r, c, matrix):
    if matrix[r][c] == 0:
        matrix[r][c] = 1

def print_matrix(matrix):
    for row in matrix:
        print(row)