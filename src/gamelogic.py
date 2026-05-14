import tkinter as tk
import random
import time

from tkinter import ttk
from enum import Enum
from matrix import *

gridsize = 4
matrix = None
target_num = 4
current_player = 'x'
rock_count = 0

class Random_Event(Enum):
    FLIP_PIECES = "Flip Pieces"
    GROW_GRID = "Grow Grid"
    DROP_PIECES = "Drop Pieces"
    LIFT_PIECES = "Lift Pieces"
    SPLIT_PIECES = "Split Pieces"
    PLACE_ROCK = "Place Rock"
    DELETE_RANDOM = "Delete Random"
    PLACE_PIECE = "Place Piece"

def start_menu(root):
    pixel = tk.PhotoImage(width=1, height=1)
    tk.Button(root, image=pixel, width=150, height=50, text="Play", compound="center", command=lambda: playgame(root, pixel)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Quit", compound="center", command=root.destroy).place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    
    global red_x
    global blue_o
    global rock
    global cur_player_text
    global next_event
    global next_event_text
    global event_options

    event_options = list(Random_Event)
    next_event = random.choice(event_options)
    next_event_text = tk.StringVar(value=f"Next Event\n{next_event.value}")
    cur_player_text = tk.StringVar(value=f"Current Player is {current_player.upper()}")
    red_x = tk.PhotoImage(file='src/assets/images/tic-tac-toe-red-x.png')
    blue_o = tk.PhotoImage(file='src/assets/images/tic-tac-toe-blue-o.png')
    rock = tk.PhotoImage(file='src/assets/images/rock_graphic.png')

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

def playgame(root, pixel):
    global current_player
    
    for widget in root.winfo_children():
        widget.destroy()
    
    show_player = tk.Label(root, textvariable=cur_player_text)
    show_event = tk.Label(root, textvariable=next_event_text)
    
    place_grid(root)
    show_player.place(relx=0.2, rely=0.1, anchor=tk.CENTER)
    show_event.place(relx=0.8, rely=0.1, anchor=tk.CENTER)

def do_event(root):
    global next_event
    global event_options
    global gridsize
    global rock_count
    
    if rock_count < gridsize - 2:
        if Random_Event.PLACE_ROCK not in event_options:
            event_options.append(Random_Event.PLACE_ROCK)
    else:
        if Random_Event.PLACE_ROCK in event_options:
            event_options.remove(Random_Event.PLACE_ROCK)
    
    match next_event:
        case Random_Event.FLIP_PIECES:
            matrix_func_update(flip_pieces, root)
        case Random_Event.GROW_GRID:
            grow_grid(root)
            event_options.remove(Random_Event.GROW_GRID)
        case Random_Event.DROP_PIECES:
            matrix_func_update(drop_pieces, root)
        case Random_Event.LIFT_PIECES:
            matrix_func_update(lift_pieces, root)
        case Random_Event.SPLIT_PIECES:
            matrix_func_update(split_pieces, root)
        case Random_Event.PLACE_ROCK:
            matrix_func_update(place_rock, root)
            rock_count += 1
        case Random_Event.DELETE_RANDOM:
            matrix_func_update(delete_random, root)
        case Random_Event.PLACE_PIECE:
            matrix_func_update(place_piece, root)

def win_state(root, frm, result):
    global current_player
    
    if result == 1 or result == 2:   
        text = 'dummy text'
        for children in frm.winfo_children():
            children.unbind('<Button-1>')
        win_window = tk.Toplevel(root)
        win_window.geometry('200x200')
        win_window.configure(bg='#333333')
        root.eval(f'tk::PlaceWindow {str(win_window)} center')    
        tk.Button(win_window, text="Back", compound="center", command=lambda: destroy_window_menu_return(root, win_window)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        
        if result == 1:
            if return_if_won(frm, 'X'):
                text = "X WINS!"
            elif return_if_won(frm, 'O'):
                text = "O WINS!"
        else:
            text = 'TIE!'
        
        tk.Label(win_window, text=text, bg='#333333', fg='white').place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        return True

def play_move(r, c, root):
    global current_player
    global target_num
    global matrix
    global gridsize
    global next_event

    if not matrix_set(r, c, matrix, current_player):
        return
    
    frm = get_frame(root)
    update_board(frm)
    
    result = 0
    
    if check_full(matrix, gridsize):
        result = 2
    
    if return_if_won(frm, 'X') or return_if_won(frm, 'O'):
        if return_if_won(frm, 'X') and return_if_won(frm, 'O'):
            result = 2
        else:
            result = 1
    
    if win_state(root, frm, result):
        return
    
    if current_player == 'x':
        current_player = 'o'
    elif current_player == 'o':
        current_player = 'x'
    
    root.update_idletasks()
    
    time.sleep(0.3)
    do_event(root)
    
    next_event = random.choice(event_options)
    next_event_text.set(f"Next Event\n{next_event.value}")
    cur_player_text.set(f"Current Player is {current_player.upper()}")

def update_board(frm):
    global red_x
    global blue_o
    global rock
    global matrix
    global gridsize
    
    if matrix == None:
        return  
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                canvas = (frm.grid_slaves(r, c))[0]
                if canvas.find_all():
                    canvas.delete('all')

            elif matrix[r][c] == 1:
                canvas = (frm.grid_slaves(r, c))[0]
                if not canvas.find_withtag('X'):
                    canvas.delete('all')
                    canvas.create_image(4, 3, anchor=tk.NW, image=red_x, tag='X')

            elif matrix[r][c] == 2:
                canvas = (frm.grid_slaves(r, c))[0]
                if not canvas.find_withtag('O'):
                    canvas.delete('all')
                    canvas.create_image(3, 4, anchor=tk.NW, image=blue_o, tag='O')
            
            elif matrix[r][c] == 3:
                canvas = (frm.grid_slaves(r, c))[0]
                if not canvas.find_withtag('rock'):
                    canvas.delete('all')
                    canvas.create_image(3, 4, anchor=tk.NW, image=rock, tag='rock')

def return_if_won(frm, player):
    global gridsize
    global target_num

    for r in range(gridsize):
        for c in range(gridsize):
            if not (frm.grid_slaves(r, c)):
                continue
            elif not (frm.grid_slaves(r, c))[0].find_withtag(player):
                continue
            
            if target_num == 4:
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r, c+1))[0].find_withtag(player) and
                        (frm.grid_slaves(r, c+2))[0].find_withtag(player) and 
                        (frm.grid_slaves(r, c+3))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+1, c))[0].find_withtag(player) and
                        (frm.grid_slaves(r+2, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+3, c))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+1, c+1))[0].find_withtag(player) and
                        (frm.grid_slaves(r+2, c+2))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+3, c+3))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if c - 3 >= 0:
                        if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                            (frm.grid_slaves(r+1, c-1))[0].find_withtag(player) and
                            (frm.grid_slaves(r+2, c-2))[0].find_withtag(player) and 
                            (frm.grid_slaves(r+3, c-3))[0].find_withtag(player)):
                            return True
                except IndexError:
                    pass
            elif target_num == 5:
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r, c+1))[0].find_withtag(player) and
                        (frm.grid_slaves(r, c+2))[0].find_withtag(player) and 
                        (frm.grid_slaves(r, c+3))[0].find_withtag(player) and
                        (frm.grid_slaves(r, c+4))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+1, c))[0].find_withtag(player) and
                        (frm.grid_slaves(r+2, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+3, c))[0].find_withtag(player) and
                        (frm.grid_slaves(r+4, c))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+1, c+1))[0].find_withtag(player) and
                        (frm.grid_slaves(r+2, c+2))[0].find_withtag(player) and 
                        (frm.grid_slaves(r+3, c+3))[0].find_withtag(player) and
                        (frm.grid_slaves(r+4, c+4))[0].find_withtag(player)):
                        return True
                except IndexError:
                    pass
                try:
                    if c - 4 >= 0:
                        if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                            (frm.grid_slaves(r+1, c-1))[0].find_withtag(player) and
                            (frm.grid_slaves(r+2, c-2))[0].find_withtag(player) and 
                            (frm.grid_slaves(r+3, c-3))[0].find_withtag(player) and
                            (frm.grid_slaves(r+4, c-4))[0].find_withtag(player)):
                            return True
                except IndexError:
                    pass

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
            canvas.bind("<Button-1>", lambda e, r=j, c=i: play_move(r, c, root))
    
    frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def destroy_window_menu_return(root, window):
    return_menu(root)
    window.destroy()

def get_frame(root):
    for children in root.winfo_children():
        if isinstance(children, ttk.Frame):
            return children

def grow_grid(root):
    global gridsize
    global target_num
    gridsize += 2
    target_num = 5

    frm = get_frame(root)
    frm.destroy() # type: ignore
    
    place_grid(root)
    frm = get_frame(root)
    update_board(frm)

def matrix_func_update(func, root):
    global matrix
    global gridsize

    func(matrix, gridsize)
    frm = get_frame(root)
    update_board(frm)
    result = 0
    
    if check_full(matrix, gridsize):
        result = 2
    
    if return_if_won(frm, 'X') or return_if_won(frm, 'O'):
        if return_if_won(frm, 'X') and return_if_won(frm, 'O'):
            result = 2
        else:
            result = 1 
    
    win_state(root, frm, result)
