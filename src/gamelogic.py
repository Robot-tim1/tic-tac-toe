import tkinter as tk
import random
import time

from tkinter import ttk
from enum import Enum
from matrix import *
from cpu import *

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

class Game():
    def __init__(self, root) -> None:
        self.root = root

        self.font = 'Calibri 12 bold'
        self.gridsize = 4
        self.matrix = None
        self.target_num = 4
        self.current_player = 'x'
        self.rock_count = 0
        self.cpu_easy = False
        self.cpu_normal = False
        self.won = False
        self.event_weights = [13.5, 13, 12.5, 11, 10, 10, 7.5, 5, 3, 2, 7.5, 5]

        self.red_x = tk.PhotoImage(file='src/assets/images/tic-tac-toe-red-x.png')
        self.blue_o = tk.PhotoImage(file='src/assets/images/tic-tac-toe-blue-o.png')
        self.rock = tk.PhotoImage(file='src/assets/images/rock_graphic.png')

    def reset_values(self) -> None:
        self.font = 'Calibri 12 bold'
        self.gridsize = 4
        self.matrix = None
        self.target_num = 4
        self.current_player = 'x'
        self.rock_count = 0
        self.cpu_easy = False
        self.cpu_normal = False
        self.won = False
        self.event_weights = [13.5, 13, 12.5, 11, 10, 10, 7.5, 5, 3, 2, 7.5, 5]

    def start(self) -> None:
        self.start_menu()
        self.root.mainloop()

    def start_menu(self):
        self.pixel = tk.PhotoImage(width=1, height=1)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="Play", font=self.font, compound="center", command=lambda: self.pick_mode()).place(relx=0.5, y=324, anchor=tk.CENTER)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="Quit", font=self.font, compound="center", command=self.root.destroy).place(relx=0.5, y=468, anchor=tk.CENTER)
        
        self.title_screen = tk.PhotoImage(file='src/assets/images/ttt-title-screen.png')
        canvas = tk.Canvas(self.root, width=500, height=200, bg="#292828")
        canvas.place(relx=0.5, y=150, anchor=tk.CENTER)
        canvas.create_image(0, -6, anchor=tk.NW, image=self.title_screen)

        self.event_options = list(Random_Event)
        self.next_event = random.choices(self.event_options, weights=self.event_weights, k=1)[0]
        self.next_event_text = tk.StringVar(value=f"Next Event:\n{self.next_event.value}")
        self.cur_player_text = tk.StringVar(value=f"Current Player is {self.current_player.upper()}")

    def pick_mode(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="2P Mode", font=self.font, compound="center", command=lambda: self.playgame()).place(relx=0.6, y=324, anchor=tk.CENTER)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="CPU Mode", font=self.font, compound="center", command=lambda: self.pick_cpu()).place(relx=0.4, y=324, anchor=tk.CENTER)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="Back", font=self.font, compound="center", command=lambda: self.return_menu()).place(relx=0.5, y=468, anchor=tk.CENTER)

    def pick_cpu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, image=self.pixel, width=150, height=50, text="CPU Easy", font=self.font, compound="center", command=lambda: self.set_cpu_play(1)).place(relx=0.4, y=324, anchor=tk.CENTER)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="CPU Normal", font=self.font, compound="center", command=lambda: self.set_cpu_play(2)).place(relx=0.6, y=324, anchor=tk.CENTER)
        tk.Button(self.root, image=self.pixel, width=150, height=50, text="Back", font=self.font, compound="center", command=lambda: self.pick_mode()).place(relx=0.5, y=468, anchor=tk.CENTER)

    def set_cpu_play(self, cpu):  
        if cpu == 1:
            self.cpu_easy = True
        elif cpu == 2:
            self.cpu_normal = True
        self.playgame()

    def return_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.reset_values()
        self.start_menu()

    def playgame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        show_player = tk.Label(self.root, textvariable=self.cur_player_text, font=self.font)
        show_event = tk.Label(self.root, textvariable=self.next_event_text, font=self.font)
        backdrop = tk.Canvas(self.root, width=200, height=120)
        
        self.place_grid()
        backdrop.place(x=166, y=104, anchor=tk.CENTER)
        show_player.place(x=166, y=72, anchor=tk.CENTER)
        show_event.place(x=166, y=126, anchor=tk.CENTER)
        show_player.tkraise(backdrop)
        show_event.tkraise(backdrop)

    def do_event(self):
        match self.next_event:
            case Random_Event.MOVE_PIECE:
                self.matrix_func_update(move_piece)
            case Random_Event.PLACE_PIECE:
                self.matrix_func_update(place_piece)
            case Random_Event.DELETE_RANDOM:
                self.matrix_func_update(delete_random)
            case Random_Event.FLIP_PIECES:
                self.matrix_func_update(flip_pieces)
            case Random_Event.PLACE_ROCK:
                self.matrix_func_update(place_rock)
                self.rock_count += 1
            case Random_Event.DROP_PIECES:
                self.matrix_func_update(drop_pieces)
            case Random_Event.LIFT_PIECES:
                self.matrix_func_update(lift_pieces)
            case Random_Event.SPLIT_PIECES:
                self.matrix_func_update(split_pieces)
            case Random_Event.SHUFFLE_PIECES:
                self.matrix_func_update(shuffle_pieces)
            case Random_Event.GO_AGAIN:
                if self.current_player == 'x':
                    self.current_player = 'o'
                elif self.current_player == 'o':
                    self.current_player = 'x'
            case Random_Event.DELETE_HALF:
                self.matrix_func_update(delete_half)
            case Random_Event.GROW_GRID:
                self.grow_grid()
                self.event_options.remove(Random_Event.GROW_GRID)
        
        if self.rock_count < self.gridsize - 2:
            if Random_Event.PLACE_ROCK not in self.event_options:
                self.event_options.append(Random_Event.PLACE_ROCK)
        else:
            if Random_Event.PLACE_ROCK in self.event_options:
                self.event_options.remove(Random_Event.PLACE_ROCK)

        if len(self.event_options) == 11 and Random_Event.GROW_GRID in self.event_options:
            self.event_weights = [13.5, 13, 12.5, 11, 10, 10, 10, 5, 3, 2, 10]
        elif len(self.event_options) == 11 and Random_Event.PLACE_ROCK in self.event_options:
            self.event_weights = [13, 13, 10.5, 11.5, 11, 11, 10, 5, 3, 2, 10]
        elif len(self.event_options) == 10:
            self.event_weights = [13.5, 13, 12.5, 13, 13, 13, 10, 5, 4, 3]

    def win_state(self, frm, result):
        if result == 1 or result == 2:   
            text = 'dummy text'
            for children in frm.winfo_children():
                children.unbind('<Button-1>')
            win_window = tk.Toplevel(self.root)
            win_window.geometry('200x200')
            win_window.configure(bg='#333333')
            self.root.eval(f'tk::PlaceWindow {str(win_window)} center')    
            tk.Button(win_window, text="Back", compound="center", font=self.font, command=lambda: self.destroy_window_menu_return(win_window)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
            
            if result == 1:
                if self.return_if_won(frm, 'X'):
                    text = "X WINS!"
                elif self.return_if_won(frm, 'O'):
                    text = "O WINS!"
            else:
                text = 'TIE!'
            
            tk.Label(win_window, text=text, bg='#333333', fg='white', font=self.font).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            return True

    def play_move(self, r, c):
        
        if self.won:
            return

        if not matrix_set(r, c, self.matrix, self.current_player):
            return
        
        frm = self.get_frame()
        self.update_board(frm)
        
        result = 0
        
        if check_full(self.matrix, self.gridsize):
            result = 2
        
        if self.return_if_won(frm, 'X') or self.return_if_won(frm, 'O'):
            if self.return_if_won(frm, 'X') and self.return_if_won(frm, 'O'):
                result = 2
            else:
                result = 1
        
        if self.win_state(frm, result):
            won = True
            return
        
        if self.current_player == 'x':
            self.current_player = 'o'
        elif self.current_player == 'o':
            self.current_player = 'x'
        
        self.root.update_idletasks()
        time.sleep(0.7)
        self.do_event()
        
        last_event = self.next_event
        while last_event == self.next_event:
            self.next_event = random.choices(self.event_options, weights=self.event_weights, k=1)[0]
        self.next_event_text.set(f"Next Event:\n{self.next_event.value}")
        self.cur_player_text.set(f"Current Player is {self.current_player.upper()}")
        if (self.cpu_easy or self.cpu_normal) and self.current_player == 'o':
            self.root.update_idletasks()
            time.sleep(1)
            move = (0, 0)
            if self.cpu_easy:
                move = cpu_easy_move(self.matrix, self.gridsize)
            elif self.cpu_normal:
                move = cpu_normal_move(self.matrix, self.gridsize)
            self.play_move(move[0], move[1])

    def update_board(self, frm):
        if self.matrix == None:
            return  
        for r in range(self.gridsize):
            for c in range(self.gridsize):
                if self.matrix[r][c] == 0:
                    canvas = (frm.grid_slaves(r, c))[0]
                    if canvas.find_all():
                        canvas.delete('all')

                elif self.matrix[r][c] == 1:
                    canvas = (frm.grid_slaves(r, c))[0]
                    if not canvas.find_withtag('X'):
                        canvas.delete('all')
                        canvas.create_image(4, 3, anchor=tk.NW, image=self.red_x, tag='X')

                elif self.matrix[r][c] == 2:
                    canvas = (frm.grid_slaves(r, c))[0]
                    if not canvas.find_withtag('O'):
                        canvas.delete('all')
                        canvas.create_image(3, 4, anchor=tk.NW, image=self.blue_o, tag='O')
                
                elif self.matrix[r][c] == 3:
                    canvas = (frm.grid_slaves(r, c))[0]
                    if not canvas.find_withtag('rock'):
                        canvas.delete('all')
                        canvas.create_image(3, 4, anchor=tk.NW, image=self.rock, tag='rock')

    def return_if_won(self, frm, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.gridsize):
            for c in range(self.gridsize):
                if not (frm.grid_slaves(r, c)):
                    continue
                elif not (frm.grid_slaves(r, c))[0].find_withtag(player):
                    continue
                for dr, dc in directions:
                    if self.target_num == 4:
                        try:
                            if c - 3 >= 0 or dc != -1:
                                if ((frm.grid_slaves(r, c))[0].find_withtag(player) and 
                                    (frm.grid_slaves(r+dr, c+dc))[0].find_withtag(player) and
                                    (frm.grid_slaves(r+(dr*2), c+(dc*2)))[0].find_withtag(player) and 
                                    (frm.grid_slaves(r+(dr*3), c+(dc*3)))[0].find_withtag(player)):
                                    return True
                        except IndexError:
                            pass
                    elif self.target_num == 5:
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

    def place_grid(self):
        frm = ttk.Frame(self.root)
        frm.grid()
        
        if not self.matrix:
            self.matrix = [[0 for _ in range(self.gridsize)] for _ in range(self.gridsize)]
        else:
            new_matrix = [[0 for _ in range(self.gridsize)] for _ in range(self.gridsize)]
            for i in range(self.gridsize - 2):
                for j in range(self.gridsize - 2):
                    new_matrix[j+1][i+1] = self.matrix[j][i]
            self.matrix = new_matrix
        
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                canvas = tk.Canvas(frm, width=100, height=100, bg='white')
                canvas.grid(row=j, column=i)
                canvas.bind("<Button-1>", lambda e, r=j, c=i: self.play_move(r, c))
        
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def destroy_window_menu_return(self, window):
        self.return_menu()
        window.destroy()

    def get_frame(self):
        for children in self.root.winfo_children():
            if isinstance(children, ttk.Frame):
                return children

    def grow_grid(self):
        self.gridsize += 2
        self.target_num = 5

        frm = self.get_frame()
        frm.destroy() # type: ignore
        
        self.place_grid()
        frm = self.get_frame()
        self.update_board(frm)

    def matrix_func_update(self, func):
        func(self.matrix, self.gridsize)
        frm = self.get_frame()
        self.update_board(frm)
        result = 0
        
        if check_full(self.matrix, self.gridsize):
            result = 2
        
        if self.return_if_won(frm, 'X') or self.return_if_won(frm, 'O'):
            if self.return_if_won(frm, 'X') and self.return_if_won(frm, 'O'):
                result = 2
            else:
                result = 1 
        
        self.win_state(frm, result)
