import tkinter as tk
from tkinter import ttk

from gamelogic import *

def center_window(root, width=1280, height=720):

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()


    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    root.configure(bg='#333333')
    center_window(root)
    root.geometry()
    start_menu(root)

if __name__ == "__main__":
    main()