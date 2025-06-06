import heapq
import math
import time
from collections import deque
import numpy as np

# Core grid utilities
def octile_distance(pos1, pos2):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

def get_neighbors(grid, node_pos):
    rows, cols = len(grid), len(grid[0])
    row, col = node_pos
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    neighbors = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
            move_cost = math.sqrt(2) if dr and dc else 1
            neighbors.append(((r, c), move_cost))
    return neighbors

# Node for A*, Dijkstra, Greedy
class Node:
    __slots__ = ('pos', 'g_cost', 'h_cost', 'parent')
    def __init__(self, pos, g_cost=float('inf'), h_cost=0, parent=None):
        self.pos = pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parent = parent
    @property
    def f_cost(self):
        return self.g_cost + self.h_cost
    def __lt__(self, other):
        return self.f_cost < other.f_cost

# Shared path recovery
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.pos)
        node = node.parent
    return path[::-1]

# A*, Dijkstra, Greedy
def search(grid, start, goal, algorithm="a_star"):
    start_time = time.time()
    open_set = []
    visited = {start: 0}
    visited_nodes = []

    use_g = algorithm in ['a_star', 'dijkstra']
    use_h = algorithm in ['a_star', 'greedy']

    h = octile_distance(start, goal) if use_h else 0
    start_node = Node(start, 0 if use_g else 0, h)
    heapq.heappush(open_set, (start_node.f_cost, start_node))

    while open_set:
        _, current = heapq.heappop(open_set)
        visited_nodes.append(current.pos)

        if current.pos == goal:
            end_time = time.time()
            path = reconstruct_path(current)
            print_metrics(algorithm, visited_nodes, path, current.g_cost, end_time - start_time)
            return path, visited_nodes

        for neighbor_pos, move_cost in get_neighbors(grid, current.pos):
            g_cost = current.g_cost + move_cost if use_g else 0
            if neighbor_pos not in visited or g_cost < visited[neighbor_pos]:
                visited[neighbor_pos] = g_cost
                h_cost = octile_distance(neighbor_pos, goal) if use_h else 0
                neighbor_node = Node(neighbor_pos, g_cost, h_cost, current)
                heapq.heappush(open_set, (neighbor_node.f_cost, neighbor_node))

    end_time = time.time()
    print_metrics(algorithm, visited_nodes, None, 0, end_time - start_time)
    return None, visited_nodes

# BFS
def bfs(grid, start, goal):
    start_time = time.time()
    queue = deque()
    visited = set()
    came_from = {}
    visited_nodes = []

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()
        visited_nodes.append(current)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            end_time = time.time()
            path = path[::-1]
            print_metrics("bfs", visited_nodes, path, len(path), end_time - start_time)
            return path, visited_nodes

        for neighbor, _ in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    end_time = time.time()
    print_metrics("bfs", visited_nodes, None, 0, end_time - start_time)
    return None, visited_nodes

# DFS
def dfs(grid, start, goal):
    start_time = time.time()
    stack = [start]
    visited = set()
    came_from = {}
    visited_nodes = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        visited_nodes.append(current)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            end_time = time.time()
            path = path[::-1]
            print_metrics("dfs", visited_nodes, path, len(path), end_time - start_time)
            return path, visited_nodes

        for neighbor, _ in get_neighbors(grid, current):
            if neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)

    end_time = time.time()
    print_metrics("dfs", visited_nodes, None, 0, end_time - start_time)
    return None, visited_nodes

# Log metrics
def print_metrics(name, visited_nodes, path, cost, duration):
    print(f"\n--- {name.upper()} Performance ---")
    print(f"Time taken: {duration:.6f} sec")
    print(f"Nodes expanded: {len(visited_nodes)}")
    if path:
        print(f"Path length: {len(path)}")
        print(f"Total cost: {cost:.2f}")
    else:
        print("No path found.")

# Load grid from txt
def load_grid_from_txt(file_path):
    with open(file_path, 'r') as f:
        return [[int(cell) for cell in line.strip().split()] for line in f]
