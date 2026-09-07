import tkinter as tk

def get_coords(event):
    # Print the x and y coordinates relative to the canvas
    print(f"Coordinates: x={event.x}, y={event.y}")

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Bind left mouse click to print coordinates
canvas.bind("<Button-1>", get_coords)

root.mainloop()