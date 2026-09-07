import tkinter as tk


class DraggableResizableCircle:
    def __init__(self, canvas, x, y, r, color="blue"):
        self.canvas = canvas
        # Create the circle
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=2)
        # Create a text item for coordinates
        self.text = canvas.create_text(x, y - r - 10, text=f"({x}, {y})")

        # Make it draggable
        self.canvas.tag_bind(self.circle, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.on_drag)

        # Make it resizable (right-click and drag)
        self.canvas.tag_bind(self.circle, "<Button-3>", self.on_click)
        self.canvas.tag_bind(self.circle, "<B3-Motion>", self.on_resize)

    def on_click(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.circle, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self.x = event.x
        self.y = event.y
        self.update_text()

    def on_resize(self, event):
        # Resize based on distance from center
        coords = self.canvas.coords(self.circle)
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2

        new_r = abs(event.x - center_x)
        self.canvas.coords(self.circle, center_x - new_r, center_y - new_r, center_x + new_r, center_y + new_r)
        self.update_text()

    def update_text(self):
        coords = self.canvas.coords(self.circle)
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2
        self.canvas.itemconfig(self.text, text=f"({int(center_x)}, {int(center_y)})")


# Set up the window
root = tk.Tk()
root.title("Draggable/Resizable Circle")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Create the object
circle = DraggableResizableCircle(canvas, 100, 100, 30)

root.mainloop()




#parking

class Router:
    def __init__(self, canvas, x, y, r, color="gray", ip="0.0.0.0", name="Default"):
        self.canvas = canvas
        # Create the circle
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="white", width=2)

        # Make it draggable
        self.canvas.tag_bind(self.circle, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.on_drag)

        # Text color for name and ip
        self.name_label = tk.Label(self, text=name, bg="red", fg="white")
        self.name_label.place(pady=5, padx=10)

        self.ip_label = tk.Label(self, text=ip, bg="red", fg="white")
        self.ip_label.place(pady=5, padx=10)

    def on_click(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.circle, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self.x = event.x
        self.y = event.y
        self.update_text()

    def set_status(self, is_online):
        if is_online:
            self.name_label.config(bg="green")
            self.ip_label.config(bg="green")
        else:
            self.name_label.config(bg="red")
            self.ip_label.config(bg="red")
