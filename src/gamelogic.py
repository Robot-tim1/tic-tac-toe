import tkinter as tk
from tkinter import ttk

from matrix import *
from globalvar import *

def playgame(root, pixel):
    global current_player
    for widget in root.winfo_children():
        widget.destroy()
    
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    
    place_grid(root, pixel)
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

def start_menu(root, pixel):
    tk.Button(root, image=pixel, width=150, height=50, text="Play", compound="center", command=lambda: playgame(root, pixel)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Quit", compound="center", command=root.destroy).place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    global running
    
    global red_x
    global blue_o

    red_x = tk.PhotoImage(file='src/assets/images/tic-tac-toe-red-x.png')
    blue_o = tk.PhotoImage(file='src/assets/images/tic-tac-toe-blue-o.png')
    if not running:
        running = True
        root.mainloop()

def return_menu(root, pixel):
    for widget in root.winfo_children():
        widget.destroy()
    
    global matrix
    global gridsize
    global current_player
    global target_num
    
    current_player = 'x'
    gridsize = 4
    matrix = None
    target_num = 3

    start_menu(root, pixel)

def play_move(r, c, matrix, root, pixel, gridsize):
    global current_player
    global target_num

    if not matrix_set(r, c, matrix, current_player):
        return
    
    result = check_win(matrix, gridsize, target_num)
    if result == 1:
        if current_player == 'x':
            print("X WINS!")
        elif current_player == 'o':
            print("O WINS!")
        return_menu(root, pixel)
        return
    
    elif result == 2:
        print('TIE!')
        return_menu(root, pixel)
        return
    
    frm = get_frame(root)
    update_board(matrix, frm, gridsize)
    
    if current_player == 'x':
        current_player = 'o'
    elif current_player == 'o':
        current_player = 'x'
    
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

def get_frame(root):
    for children in root.winfo_children():
        if isinstance(children, ttk.Frame):
            return children

def update_board(matrix, frm, gridsize):
    global red_x
    global blue_o
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                continue

            if matrix[r][c] == 1:
                canvas = (frm.grid_slaves(r, c))[0]
                canvas.create_image(4, 3, anchor=tk.NW, image=red_x)

            if matrix[r][c] == 2:
                canvas = (frm.grid_slaves(r, c))[0]
                canvas.create_image(3, 4, anchor=tk.NW, image=blue_o)

def grow_grid(root, pixel):
    global gridsize
    gridsize += 2
    
    for widget in root.winfo_children():
        widget.destroy()
    
    place_grid(root, pixel)
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

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
            canvas = tk.Canvas(frm, width=100, height=100, bg='white')
            canvas.grid(row=j, column=i)
            canvas.bind("<Button-1>", lambda e, r=j, c=i: play_move(r, c, matrix, root, pixel, gridsize))
            
    tk.Button(root, image=pixel, width=100, height=100, text="back", compound="center", command=lambda: return_menu(root, pixel)).place(relx=0.2, rely=0.5, anchor=tk.CENTER)
    frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)