#!/bin/python3

import tkinter as tk

root = tk.Tk()
root.attributes('-zoomed', True)
root.title("Network Map")
#height = 1600, width = 1200
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)



root.mainloop()




