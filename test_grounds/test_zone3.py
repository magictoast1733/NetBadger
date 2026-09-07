import tkinter as tk


def draw_connecting_line():
    # Get the bounding box coordinates (x0, y0, x1, y1) for both rectangles
    shape1_coords = canvas.coords(rect1)
    shape2_coords = canvas.coords(rect2)

    # Calculate the center (x, y) of the right face of the first rectangle
    x1 = shape1_coords[2]  # right x-coordinate
    y1 = (shape1_coords[1] + shape1_coords[3]) / 2  # vertical midpoint

    # Calculate the center (x, y) of the left face of the second rectangle
    x2 = shape2_coords[0]  # left x-coordinate
    y2 = (shape2_coords[1] + shape2_coords[3]) / 2  # vertical midpoint

    # Draw a line between the two calculated face points
    canvas.create_line(x1, y1, x2, y2, fill="red", width=3)


# Setup Tkinter Window
root = tk.Tk()
root.title("Connect Shape Faces")
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(pady=20)

# Draw Shape 1 (Rectangle)
rect1 = canvas.create_rectangle(50, 100, 150, 200, fill="lightblue", outline="blue")

# Draw Shape 2 (Rectangle)
rect2 = canvas.create_rectangle(250, 50, 350, 150, fill="lightgreen", outline="green")

# Button to trigger the line drawing
btn = tk.Button(root, text="Draw Line Between Faces", command=draw_connecting_line)
btn.pack(pady=10)

root.mainloop()
