import random
import heapq
import time

# ==========================================
# 1. DISJOINT SET UNION (FOR KRUSKAL'S MST)
# ==========================================
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1
            return True
        return False


# ==========================================
# 2. RANDOMIZED KRUSKAL'S MAZE GENERATOR
# ==========================================
def generate_kruskal_maze(rows, cols):
    """
    Generates a spanning-tree maze where 1 = Wall and 0 = Path.
    Time Complexity: O(E log E)
    """
    start_time = time.perf_counter()
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    
    # Vertices are located at odd (row, col) coordinates
    vertices = [(r, c) for r in range(1, rows, 2) for c in range(1, cols, 2)]
    for r, c in vertices:
        grid[r][c] = 0

    # Edges are walls separating adjacent vertices
    edges = []
    for r, c in vertices:
        if r + 2 < rows:
            edges.append(((r, c), (r + 2, c), (r + 1, c)))
        if c + 2 < cols:
            edges.append(((r, c), (r, c + 2), (r, c + 1)))

    # Assign random weights by shuffling edges
    random.shuffle(edges)
    dsu = DisjointSet(vertices)

    # Knock down walls if cells belong to different sets (prevents cycles)
    for cell1, cell2, wall in edges:
        if dsu.union(cell1, cell2):
            wr, wc = wall
            grid[wr][wc] = 0

    gen_time_ms = (time.perf_counter() - start_time) * 1000
    return grid, gen_time_ms


# ==========================================
# 3. DIJKSTRA'S SHORTEST PATH SOLVER
# ==========================================
def solve_dijkstra(grid, start, end):
    """
    Finds the shortest path from start to end using a Min-Heap Priority Queue.
    Time Complexity: O((V + E) log V)
    """
    start_time = time.perf_counter()
    rows, cols = len(grid), len(grid[0])
    
    pq = [(0, start)]
    distances = {start: 0}
    predecessors = {start: None}
    visited = set()

    while pq:
        curr_dist, curr_cell = heapq.heappop(pq)
        
        if curr_cell in visited:
            continue
        visited.add(curr_cell)

        if curr_cell == end:
            break

        r, c = curr_cell
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                neighbor = (nr, nc)
                # Edge relaxation: dist[v] = min(dist[v], dist[u] + 1)
                new_dist = curr_dist + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, (new_dist, neighbor))

    solve_time_ms = (time.perf_counter() - start_time) * 1000

    # Backtrack from exit to start to reconstruct path
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
    path.reverse()

    if not path or path[0] != start:
        return [], solve_time_ms, len(visited)

    return path, solve_time_ms, len(visited)