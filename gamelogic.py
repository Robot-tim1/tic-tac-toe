import tkinter as tk
from tkinter import ttk

gridsize = 3
matrix = None

def matrix_set(r, c, matrix):
    if matrix[r][c] == 0:
        matrix[r][c] = 1

def print_matrix(matrix):
    for row in matrix:
        print(row)

def place_grid(root, pixel):
    frm = ttk.Frame(root)
    frm.grid()
    global matrix
    global gridsize
    if not matrix:
        matrix = [[0 for _ in range(gridsize)] for _ in range(gridsize)]
    else:
        new_matrix = [[0 for _ in range(gridsize)] for _ in range(gridsize)]
        for i in range(gridsize - 2):
            for j in range(gridsize - 2):
                new_matrix[j+1][i+1] = matrix[j][i]
        matrix = new_matrix
    for i in range(gridsize):
        for j in range(gridsize):
            tk.Button(frm, image=pixel, width=100, height=100, text="button", compound="center", command=lambda r=j, c=i: matrix_set(r, c, matrix)).grid(column=i, row=j)
    tk.Button(root, image=pixel, width=100, height=100, text="print", compound="center", command=lambda: print_matrix(matrix)).place(relx=0.8, rely=0.5, anchor=tk.CENTER)
    frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    return frm

def grow_grid(root, pixel, frm : ttk.Frame):
    global gridsize
    gridsize += 2
    frm.destroy()
    place_grid(root, pixel)
