import os
import csv
from a_star_pathfinding_multi import load_grid_from_txt, search, bfs, dfs

# 📂 Define your maps here
maps = [
    {"file": "map.txt", "start": (0, 0), "goal": (9, 9)},
    {"file": "maze1.txt", "start": (0, 0), "goal": (4, 6)},
    {"file": "open_space.txt", "start": (0, 0), "goal": (4, 4)},
    {"file": "blocked.txt", "start": (0, 0), "goal": (3, 4)}
]

# 📌 Supported algorithms
algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]

# Output file
output_csv = "results.csv"

# CSV headers
headers = ["Map", "Algorithm", "Time(s)", "Nodes Expanded", "Path Length", "Total Cost", "Found"]

def benchmark():
    results = []

    for map_data in maps:
        grid_file = map_data["file"]
        start = map_data["start"]
        goal = map_data["goal"]

        try:
            grid = load_grid_from_txt(grid_file)
        except FileNotFoundError:
            print(f"❌ Map file not found: {grid_file}")
            continue

        for algo in algorithms:
            print(f"\n▶ Running {algo.upper()} on {grid_file}")

            # Run the correct algorithm
            if algo in ["a_star", "dijkstra", "greedy"]:
                path, visited = search(grid, start, goal, algorithm=algo)
            elif algo == "bfs":
                path, visited = bfs(grid, start, goal)
            elif algo == "dfs":
                path, visited = dfs(grid, start, goal)
            else:
                continue

            found = bool(path)
            path_len = len(path) if path else 0
            cost = sum([1 for _ in path]) if path else "-"
            nodes_exp = len(visited)

            results.append([
                grid_file,
                algo,
                "",  # Time already printed in function
                nodes_exp,
                path_len,
                f"{cost:.2f}" if found else "-",
                "Yes" if found else "No"
            ])

    # Save CSV
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(results)

    print(f"\n✅ Results saved to {output_csv}")

if __name__ == "__main__":
    benchmark()
