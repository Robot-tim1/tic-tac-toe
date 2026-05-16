import tkinter as tk
import random
import time

from tkinter import ttk
from enum import Enum
from matrix import *
from cpu import *

font = 'Calibri 12 bold'
gridsize = 4
matrix = None
target_num = 4
current_player = 'x'
rock_count = 0
cpu_easy = False
cpu_normal = False
won = False

class Random_Event(Enum):
    MOVE_PIECE = "Move Piece"
    PLACE_PIECE = "Place Piece"
    DELETE_RANDOM = "Delete Piece"
    FLIP_PIECES = "Flip Pieces"
    DROP_PIECES = "Drop Pieces"
    LIFT_PIECES = "Lift Pieces"
    SPLIT_PIECES = "Split Pieces"
    SHUFFLE_PIECES = "Shuffle Pieces"
    GO_AGAIN = "Go Again"
    DELETE_HALF = "Snap"
    PLACE_ROCK = "Place Rock"
    GROW_GRID = "Grow Grid"

def start_menu(root):
    pixel = tk.PhotoImage(width=1, height=1)
    tk.Button(root, image=pixel, width=150, height=50, text="Play", font=font, compound="center", command=lambda: pick_mode(root, pixel)).place(relx=0.5, y=324, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Quit", font=font, compound="center", command=root.destroy).place(relx=0.5, y=468, anchor=tk.CENTER)
    
    global red_x
    global blue_o
    global rock
    global cur_player_text
    global next_event
    global next_event_text
    global event_options

    event_options = list(Random_Event)
    next_event = random.choice(event_options)
    next_event_text = tk.StringVar(value=f"Next Event:\n{next_event.value}")
    cur_player_text = tk.StringVar(value=f"Current Player is {current_player.upper()}")
    red_x = tk.PhotoImage(file='src/assets/images/tic-tac-toe-red-x.png')
    blue_o = tk.PhotoImage(file='src/assets/images/tic-tac-toe-blue-o.png')
    rock = tk.PhotoImage(file='src/assets/images/rock_graphic.png')

def pick_mode(root, pixel):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Button(root, image=pixel, width=150, height=50, text="2P Mode", font=font, compound="center", command=lambda: playgame(root, pixel)).place(relx=0.6, y=324, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="CPU Mode", font=font, compound="center", command=lambda: pick_cpu(root, pixel)).place(relx=0.4, y=324, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Back", font=font, compound="center", command=lambda: return_menu(root)).place(relx=0.5, y=468, anchor=tk.CENTER)

def pick_cpu(root, pixel):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Button(root, image=pixel, width=150, height=50, text="CPU Easy", font=font, compound="center", command=lambda: set_cpu_play(root, pixel, 1)).place(relx=0.4, y=324, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="CPU Normal", font=font, compound="center", command=lambda: set_cpu_play(root, pixel, 2)).place(relx=0.6, y=324, anchor=tk.CENTER)
    tk.Button(root, image=pixel, width=150, height=50, text="Back", font=font, compound="center", command=lambda: pick_mode(root, pixel)).place(relx=0.5, y=468, anchor=tk.CENTER)

def set_cpu_play(root, pixel, cpu):
    global cpu_easy
    global cpu_normal
    
    if cpu == 1:
        cpu_easy = True
    elif cpu == 2:
        cpu_normal = True
    playgame(root, pixel)

def return_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    global matrix
    global gridsize
    global current_player
    global target_num
    global won
    global rock_count
    global cpu_easy
    global cpu_normal

    gridsize = 4
    matrix = None
    target_num = 4
    current_player = 'x'
    rock_count = 0
    cpu_easy = False
    cpu_normal = False
    won = False

    start_menu(root)

def playgame(root, pixel):
    for widget in root.winfo_children():
        widget.destroy()
    
    show_player = tk.Label(root, textvariable=cur_player_text, font=font)
    show_event = tk.Label(root, textvariable=next_event_text, font=font)
    backdrop = tk.Canvas(root, width=200, height=120)
    
    place_grid(root)
    backdrop.place(x=166, y=104, anchor=tk.CENTER)
    show_player.place(x=166, y=72, anchor=tk.CENTER)
    show_event.place(x=166, y=126, anchor=tk.CENTER)
    show_player.tkraise(backdrop)
    show_event.tkraise(backdrop)

def do_event(root):
    global event_options
    global rock_count
    global current_player

    match next_event:
        case Random_Event.MOVE_PIECE:
            matrix_func_update(move_piece, root)
        case Random_Event.PLACE_PIECE:
            matrix_func_update(place_piece, root)
        case Random_Event.DELETE_RANDOM:
            matrix_func_update(delete_random, root)
        case Random_Event.FLIP_PIECES:
            matrix_func_update(flip_pieces, root)
        case Random_Event.PLACE_ROCK:
            matrix_func_update(place_rock, root)
            rock_count += 1
        case Random_Event.DROP_PIECES:
            matrix_func_update(drop_pieces, root)
        case Random_Event.LIFT_PIECES:
            matrix_func_update(lift_pieces, root)
        case Random_Event.SPLIT_PIECES:
            matrix_func_update(split_pieces, root)
        case Random_Event.SHUFFLE_PIECES:
            matrix_func_update(shuffle_pieces, root)
        case Random_Event.GO_AGAIN:
            if current_player == 'x':
                current_player = 'o'
            elif current_player == 'o':
                current_player = 'x'
        case Random_Event.DELETE_HALF:
            matrix_func_update(delete_half, root)
        case Random_Event.GROW_GRID:
            grow_grid(root)
            event_options.remove(Random_Event.GROW_GRID)
    
    if rock_count < gridsize - 2:
        if Random_Event.PLACE_ROCK not in event_options:
            event_options.append(Random_Event.PLACE_ROCK)
    else:
        if Random_Event.PLACE_ROCK in event_options:
            event_options.remove(Random_Event.PLACE_ROCK)

def win_state(root, frm, result):
    if result == 1 or result == 2:   
        text = 'dummy text'
        for children in frm.winfo_children():
            children.unbind('<Button-1>')
        win_window = tk.Toplevel(root)
        win_window.geometry('200x200')
        win_window.configure(bg='#333333')
        root.eval(f'tk::PlaceWindow {str(win_window)} center')    
        tk.Button(win_window, text="Back", compound="center", font=font, command=lambda: destroy_window_menu_return(root, win_window)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        
        if result == 1:
            if return_if_won(frm, 'X'):
                text = "X WINS!"
            elif return_if_won(frm, 'O'):
                text = "O WINS!"
        else:
            text = 'TIE!'
        
        tk.Label(win_window, text=text, bg='#333333', fg='white', font=font).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        return True

def play_move(r, c, root):
    global current_player
    global next_event
    global won
    
    if won:
        return

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
        won = True
        return
    
    if current_player == 'x':
        current_player = 'o'
    elif current_player == 'o':
        current_player = 'x'
    
    root.update_idletasks()
    time.sleep(0.7)
    do_event(root)
    
    next_event = random.choice(event_options)
    next_event_text.set(f"Next Event:\n{next_event.value}")
    cur_player_text.set(f"Current Player is {current_player.upper()}")
    if (cpu_easy or cpu_normal) and current_player == 'o':
        root.update_idletasks()
        time.sleep(1)
        move = (0, 0)
        if cpu_easy:
            move = cpu_easy_move(matrix, gridsize)
        elif cpu_normal:
            move = cpu_normal_move(matrix, gridsize)
        play_move(move[0], move[1], root)

def update_board(frm):
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
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(gridsize):
        for c in range(gridsize):
            if not (frm.grid_slaves(r, c)):
                continue
            elif not (frm.grid_slaves(r, c))[0].find_withtag(player):
                continue
            for dr, dc in directions:
                if target_num == 4:
                    try:
                        if c - 3 >= 0 or dc != -1:
                            if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                                (frm.grid_slaves(r+dr, c+dc))[0].find_withtag(player) and
                                (frm.grid_slaves(r+(dr*2), c+(dc*2)))[0].find_withtag(player) and 
                                (frm.grid_slaves(r+(dr*3), c+(dc*3)))[0].find_withtag(player)):
                                return True
                    except IndexError:
                        pass
                elif target_num == 5:
                    try:
                        if c - 4 >= 0 or dc != -1:
                            if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                                (frm.grid_slaves(r+dr, c+dc))[0].find_withtag(player) and
                                (frm.grid_slaves(r+(dr*2), c+(dc*2)))[0].find_withtag(player) and 
                                (frm.grid_slaves(r+(dr*3), c+(dc*3)))[0].find_withtag(player) and
                                (frm.grid_slaves(r+(dr*4), c+(dc*4)))[0].find_withtag(player)):
                                return True
                    except IndexError:
                        pass

def place_grid(root):
    frm = ttk.Frame(root)
    frm.grid()
    
    global matrix
    
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
