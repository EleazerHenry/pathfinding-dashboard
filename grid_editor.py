import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = 40

class GridEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Grid Editor")

        self.canvas = tk.Canvas(root, width=GRID_COLS * CELL_SIZE, height=GRID_ROWS * CELL_SIZE, bg='white')
        self.canvas.pack()

        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.start = None
        self.goal = None
        self.last_clicked = None
        self.filename = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("s", self.set_start)
        self.root.bind("g", self.set_goal)
        self.root.bind("<Return>", self.save_grid)

        # Load Button
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        load_btn = tk.Button(btn_frame, text="Load Map", command=self.load_map)
        load_btn.pack()

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                fill = 'white'
                if self.grid[r][c] == 1:
                    fill = 'black'
                elif (r, c) == self.start:
                    fill = 'green'
                elif (r, c) == self.goal:
                    fill = 'red'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='gray')

    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            self.last_clicked = (row, col)
            if (row, col) != self.start and (row, col) != self.goal:
                self.grid[row][col] = 1 - self.grid[row][col]
        self.draw_grid()

    def set_start(self, event):
        if self.last_clicked:
            row, col = self.last_clicked
            if self.grid[row][col] == 0 and (row, col) != self.goal:
                self.start = (row, col)
                print(f"Start set to: {self.start}")
            self.draw_grid()

    def set_goal(self, event):
        if self.last_clicked:
            row, col = self.last_clicked
            if self.grid[row][col] == 0 and (row, col) != self.start:
                self.goal = (row, col)
                print(f"Goal set to: {self.goal}")
            self.draw_grid()

    def save_grid(self, event=None):
        if not self.start or not self.goal:
            messagebox.showwarning("Missing Start/Goal", "Set both start (S) and goal (G) before saving.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, "w") as f:
            for row in self.grid:
                f.write(" ".join(map(str, row)) + "\n")

        # Save start/goal metadata
        meta_path = filepath.replace(".txt", ".json")
        with open(meta_path, "w") as meta:
            json.dump({"start": self.start, "goal": self.goal}, meta)

        print(f"✅ Grid saved to {filepath}")
        print(f"✅ Metadata saved to {meta_path}")
        self.filename = filepath

    def load_map(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, "r") as f:
            lines = f.readlines()

        grid = []
        for line in lines:
            row = list(map(int, line.strip().split()))
            grid.append(row)

        self.grid = grid
        self.start = None
        self.goal = None
        self.filename = filepath

        # Update grid dimensions (optional)
        global GRID_ROWS, GRID_COLS
        GRID_ROWS = len(grid)
        GRID_COLS = len(grid[0])

        self.canvas.config(width=GRID_COLS * CELL_SIZE, height=GRID_ROWS * CELL_SIZE)

        # Try loading metadata
        meta_path = filepath.replace(".txt", ".json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as meta:
                meta_data = json.load(meta)
                self.start = tuple(meta_data.get("start", [None, None]))
                self.goal = tuple(meta_data.get("goal", [None, None]))
                print(f"📂 Metadata loaded from {meta_path}")
                print(f"Start: {self.start} | Goal: {self.goal}")
        else:
            print("ℹ️ No metadata file found for start/goal")

        self.draw_grid()

# Run the editor
if __name__ == "__main__":
    root = tk.Tk()
    app = GridEditor(root)
    root.mainloop()
