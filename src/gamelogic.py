import tkinter as tk
from tkinter import ttk

from matrix import *
from globalvar import *

def playgame(root, pixel):
    global current_player
    for widget in root.winfo_children():
        widget.destroy()
    global show_player
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    place_grid(root, pixel)
    show_player.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

def start_menu(root, pixel):
    tk.Button(root, image=pixel, width=150, height=50, text="Play", compound="center", command=lambda: playgame(root, pixel)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Quit", compound="center", command=root.destroy).place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    root.mainloop()

def return_menu(frm, root, pixel):
    frm.destroy()
    for widget in root.winfo_children():
        widget.destroy()
    
    global matrix
    global gridsize
    global current_player
    
    current_player = 'x'
    gridsize = 3
    matrix = None
    
    start_menu(root, pixel)

def play_move(r, c, matrix, frm, root, pixel):
    global current_player

    if not matrix_set(r, c, matrix, current_player):
        return
    print_matrix(matrix)
    if check_win(matrix):
        if current_player == 'x':
            print("X WINS!")
        elif current_player == 'o':
            print("O WINS!")
        return_menu(frm, root, pixel)
        return
    
    if current_player == 'x':
        current_player = 'o'
    elif current_player == 'o':
        current_player = 'x'
    
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    show_player.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

def grow_grid(root, pixel, frm : ttk.Frame):
    global gridsize
    gridsize += 2
    frm.destroy()
    place_grid(root, pixel)

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
            tk.Button(frm, image=pixel, width=100, height=100, compound="center", command=lambda r=j, c=i: play_move(r, c, matrix, frm, root, pixel)).grid(column=i, row=j)
    
    tk.Button(root, image=pixel, width=100, height=100, text="back", compound="center", command=lambda: return_menu(frm, root, pixel)).place(relx=0.2, rely=0.5, anchor=tk.CENTER)
    
    frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    return frm