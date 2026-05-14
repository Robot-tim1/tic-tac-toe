import tkinter as tk

from gamelogic import *

def center_window(window, width=1280, height=720):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    root.configure(bg='#333333')
    center_window(root)
    start_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()