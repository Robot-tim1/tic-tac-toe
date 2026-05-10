import tkinter as tk
from tkinter import ttk

from gamelogic import *

def main():
    root = tk.Tk()
    root.geometry("1280x720")
    pixel = tk.PhotoImage(width=1, height=1)
    start_menu(root, pixel)

if __name__ == "__main__":
    main()