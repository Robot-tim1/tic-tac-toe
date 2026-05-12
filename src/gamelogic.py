import tkinter as tk
from tkinter import ttk

from matrix import *
from globalvar import *

def playgame(root, pixel):
    global current_player
    for widget in root.winfo_children():
        widget.destroy()
    
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    pixel = tk.PhotoImage(width=1, height=1)
    place_grid(root)
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

def start_menu(root):
    pixel = tk.PhotoImage(width=1, height=1)
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

def return_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    global matrix
    global gridsize
    global current_player
    global target_num
    
    current_player = 'x'
    gridsize = 4
    matrix = None
    target_num = 4

    start_menu(root)

def destroy_window_menu_return(root, window):
    return_menu(root)
    window.destroy()

def play_move(r, c, matrix, root, gridsize):
    global current_player
    global target_num
    
    if not matrix_set(r, c, matrix, current_player):
        return
    
    frm = get_frame(root)
    update_board(matrix, frm, gridsize)

    result = check_win(matrix, gridsize, target_num)
    text = 'dummy text'
    if result == 1:   
        for children in frm.winfo_children(): # type: ignore
            children.unbind('<Button-1>')
        win_window = tk.Toplevel(root)
        win_window.geometry('200x200')
        win_window.configure(bg='#333333')
        root.eval(f'tk::PlaceWindow {str(win_window)} center')

        if current_player == 'x':
            text = "X WINS!"
        elif current_player == 'o':
            text = "O WINS!"
            
        tk.Label(win_window, text=text, bg='#333333', fg='white').place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        tk.Button(win_window, text="Back", compound="center", command=lambda: destroy_window_menu_return(root, win_window)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        return
    
    elif result == 2:
        for children in frm.winfo_children(): # type: ignore
            children.unbind('<Button-1>')
        text = 'TIE!'
        win_window = tk.Toplevel(root)
        win_window.geometry('200x200')
        win_window.configure(bg='#333333')
        root.eval(f'tk::PlaceWindow {str(win_window)} center')

        tk.Label(win_window, text=text, bg='#333333', fg='white').place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        tk.Button(win_window, text="Back", compound="center", command=lambda: destroy_window_menu_return(root, win_window)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        return
    
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

def grow_grid(root):
    global gridsize
    gridsize += 2
    
    for widget in root.winfo_children():
        widget.destroy()
    
    place_grid(root)
    show_player = tk.Label(root, text=f"Current Player is {current_player.upper()}")
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

def place_grid(root):
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
            canvas.bind("<Button-1>", lambda e, r=j, c=i: play_move(r, c, matrix, root, gridsize))
            
    frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)