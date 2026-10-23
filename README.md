# Algorithmic Maze Generator & Solver with PL/SQL Analytics

A Design and Analysis of Algorithms (DAA) mini-project that demonstrates procedural maze generation using **Randomized Kruskal's Algorithm** and optimal pathfinding using **Dijkstra's Algorithm**, integrated with an **Oracle PL/SQL** backend for gameplay metrics and leaderboard analytics.

---

## 📌 Project Overview
- **Maze Generation:** Uses **Randomized Kruskal's Algorithm** with a Disjoint Set Union (DSU) structure to create spanning-tree mazes with no closed loops or isolated areas.
- **Shortest Path Solver:** Uses **Dijkstra's Algorithm** with a Min-Heap priority queue to compute and highlight the optimal route from Start to Exit.
- **Backend Analytics:** An Oracle PL/SQL database layer featuring:
  - Table: `GAME_SESSIONS`
  - Trigger: `trg_validate_session` (validates move counts and execution time)
  - Function: `calc_efficiency` (calculates performance efficiency scores)
  - Stored Procedure: `record_maze_run` (logs completed sessions)
- **GUI Visualizer:** A responsive desktop interface built with Python's built-in `tkinter` that includes real-time algorithm metrics and a dynamic leaderboard.

---

## 📊 Algorithmic Complexity

| Component | Algorithm / Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Maze Generation** | Randomized Kruskal's (MST with DSU) | $O(E \log E)$ | $O(V)$ |
| **Pathfinding** | Dijkstra's Algorithm (Min-Heap) | $O((V + E) \log V)$ | $O(V)$ |

---

## 🗂️ Project Structure

```text
maze-solver-daa/
├── algorithms.py       # Core DAA algorithms (Kruskal's MST & Dijkstra's Shortest Path)
├── database.sql        # Oracle PL/SQL tables, triggers, functions, and procedures
├── db_manager.py       # Database connector (with graceful offline simulation mode)
├── main.py             # Desktop UI visualizer and interactive controller
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from version control
└── README.md           # Project documentation