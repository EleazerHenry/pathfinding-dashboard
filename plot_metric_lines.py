import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def read_results(csv_file):
    data = defaultdict(lambda: defaultdict(dict))
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            map_name = row['Map']
            algo = row['Algorithm']
            data[algo][map_name] = {
                "Nodes": int(row['Nodes Expanded']),
                "Length": int(row['Path Length']),
                "Cost": float(row['Total Cost']) if row['Total Cost'] != '-' else None,
                "Found": row['Found'] == "Yes"
            }
    return data

def plot_line_for_metric(data, metric, ylabel):
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    map_names = sorted({m for algo in data.values() for m in algo})

    plt.figure(figsize=(10, 6))

    for algo in algorithms:
        y_vals = []
        for map_name in map_names:
            val = data[algo].get(map_name, {}).get(metric)
            y_vals.append(val if val is not None else 0)
        plt.plot(map_names, y_vals, marker='o', label=algo.upper())

    plt.title(f"{metric} Trend Across Maps")
    plt.xlabel("Map")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    filename = f"line_{metric}.png"
    plt.savefig(filename)
    print(f"✅ Saved: {filename}")
    plt.close()

if __name__ == "__main__":
    results = read_results("results.csv")
    plot_line_for_metric(results, "Nodes", "Nodes Expanded")
    plot_line_for_metric(results, "Length", "Path Length")
    plot_line_for_metric(results, "Cost", "Total Path Cost")
