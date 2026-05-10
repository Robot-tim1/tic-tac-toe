import tkinter as tk
from tkinter import ttk

from gamelogic import *

def main():
    root = tk.Tk()
    root.geometry("1280x720")
    pixel = tk.PhotoImage(width=1, height=1)
    
    frm = place_grid(root, pixel)
    tk.Button(root, image=pixel, width=100, height=100, text="grow", compound="center", command=lambda: grow_grid(root, pixel, frm)).place(relx=0.2, rely=0.5, anchor=tk.CENTER)
    root.mainloop()

if __name__ == "__main__":
    main()