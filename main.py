import tkinter as tk
from tkinter import ttk
from algorithms import generate_kruskal_maze, solve_dijkstra
from db_manager import DatabaseManager

class MazeVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithmic Maze Generator & Solver (DAA Mini Project)")
        self.root.configure(bg="#0F172A")
        
        self.db = DatabaseManager()
        self.rows, self.cols = 25, 25
        self.cell_size = 20
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        
        self.grid = []
        self.solution_path = []
        self.run_count = 1

        self.build_ui()
        self.generate_new_maze()

    def build_ui(self):
        main_frame = tk.Frame(self.root, bg="#0F172A", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- LEFT PANEL: CONTROLS & STATS ---
        left_panel = tk.Frame(main_frame, bg="#1E293B", width=220, padx=12, pady=12)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        tk.Label(left_panel, text="MAZE CONTROLLER", fg="#38BDF8", bg="#1E293B", font=("Segoe UI", 11, "bold")).pack(pady=(0, 10))

        btn_gen = tk.Button(left_panel, text="1. Generate (Kruskal)", command=self.generate_new_maze,
                            bg="#0284C7", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, pady=6, width=22)
        btn_gen.pack(pady=5)

        btn_solve = tk.Button(left_panel, text="2. Solve (Dijkstra)", command=self.solve_current_maze,
                              bg="#059669", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, pady=6, width=22)
        btn_solve.pack(pady=5)

        tk.Frame(left_panel, bg="#334155", height=2).pack(fill=tk.X, pady=15)
        tk.Label(left_panel, text="PERFORMANCE METRICS", fg="#38BDF8", bg="#1E293B", font=("Segoe UI", 11, "bold")).pack(pady=(0, 10))

        self.lbl_gen_time = tk.Label(left_panel, text="Kruskal Time: -- ms", fg="#E2E8F0", bg="#1E293B", font=("Consolas", 10))
        self.lbl_gen_time.pack(anchor="w", pady=3)

        self.lbl_solve_time = tk.Label(left_panel, text="Dijkstra Time: -- ms", fg="#E2E8F0", bg="#1E293B", font=("Consolas", 10))
        self.lbl_solve_time.pack(anchor="w", pady=3)

        self.lbl_steps = tk.Label(left_panel, text="Optimal Steps: --", fg="#10B981", bg="#1E293B", font=("Consolas", 10, "bold"))
        self.lbl_steps.pack(anchor="w", pady=3)

        self.lbl_visited = tk.Label(left_panel, text="Nodes Explored: --", fg="#E2E8F0", bg="#1E293B", font=("Consolas", 10))
        self.lbl_visited.pack(anchor="w", pady=3)

        # --- CENTER PANEL: MAZE CANVAS ---
        canvas_w = self.cols * self.cell_size
        canvas_h = self.rows * self.cell_size
        self.canvas = tk.Canvas(main_frame, width=canvas_w, height=canvas_h, bg="#0F172A", highlightthickness=2, highlightbackground="#38BDF8")
        self.canvas.pack(side=tk.LEFT)

        # --- RIGHT PANEL: PL/SQL LEADERBOARD ---
        right_panel = tk.Frame(main_frame, bg="#1E293B", width=280, padx=12, pady=12)
        right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 0))

        tk.Label(right_panel, text="PL/SQL LEADERBOARD", fg="#38BDF8", bg="#1E293B", font=("Segoe UI", 11, "bold")).pack(pady=(0, 10))

        cols = ("Player", "Steps", "Time(ms)", "Score")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings", height=16)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=65, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def render_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "#1E293B" if self.grid[r][c] == 1 else "#0F172A"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0F172A")

        # Draw Start (Blue) and Exit (Red)
        sx, sy = self.start[1] * self.cell_size, self.start[0] * self.cell_size
        ex, ey = self.end[1] * self.cell_size, self.end[0] * self.cell_size
        self.canvas.create_rectangle(sx+2, sy+2, sx+self.cell_size-2, sy+self.cell_size-2, fill="#38BDF8", outline="")
        self.canvas.create_rectangle(ex+2, ey+2, ex+self.cell_size-2, ey+self.cell_size-2, fill="#EF4444", outline="")

    def generate_new_maze(self):
        self.grid, gen_time = generate_kruskal_maze(self.rows, self.cols)
        self.solution_path = []
        self.render_grid()
        self.lbl_gen_time.config(text=f"Kruskal Time: {gen_time:.2f} ms")
        self.lbl_solve_time.config(text="Dijkstra Time: -- ms")
        self.lbl_steps.config(text="Optimal Steps: --")
        self.lbl_visited.config(text="Nodes Explored: --")

    def solve_current_maze(self):
        if not self.grid:
            return
        self.solution_path, solve_time, visited_count = solve_dijkstra(self.grid, self.start, self.end)
        self.render_grid()

        # Draw glowing green solution path
        for i in range(len(self.solution_path) - 1):
            r1, c1 = self.solution_path[i]
            r2, c2 = self.solution_path[i + 1]
            x1 = c1 * self.cell_size + self.cell_size // 2
            y1 = r1 * self.cell_size + self.cell_size // 2
            x2 = c2 * self.cell_size + self.cell_size // 2
            y2 = r2 * self.cell_size + self.cell_size // 2
            self.canvas.create_line(x1, y1, x2, y2, fill="#10B981", width=4)

        steps = len(self.solution_path)
        self.lbl_solve_time.config(text=f"Dijkstra Time: {solve_time:.3f} ms")
        self.lbl_steps.config(text=f"Optimal Steps: {steps}")
        self.lbl_visited.config(text=f"Nodes Explored: {visited_count}")

        # Log to PL/SQL Manager and update Leaderboard
        player_tag = f"Run_{self.run_count}"
        self.run_count += 1
        self.db.log_session(player_tag, f"{self.rows}x{self.cols}", steps, solve_time)
        self.refresh_leaderboard()

    def refresh_leaderboard(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.db.history[:15]:
            self.tree.insert("", tk.END, values=(item["player"], item["steps"], item["time_ms"], item["score"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeVisualizerApp(root)
    root.mainloop()