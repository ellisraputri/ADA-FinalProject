import tkinter as tk
from scrollableCanvas import ScrollableCanvas

class ScrollCanvas():
    def __init__(self, root, x_input, y_input):
        self.root = root
        self.scroll_canvas = ScrollableCanvas(self.root)
        self.scroll_canvas.pack(fill="both", expand=True)
        self.scroll_canvas.place(x=x_input, y=y_input)
    

    def add_log(self, message):
        """Add a new log entry to the canvas."""
        label = tk.Label(self.scroll_canvas.scrollable_frame, text=message, font="SegoeUI 12", anchor="w")
        label.pack(fill="x", padx=10, pady=5)

        # Ensure the canvas updates with the new content
        self.scroll_canvas.update_canvas()

        # Automatically scroll to the bottom as new content is added
        self.scroll_canvas.canvas.yview_moveto(1.0)