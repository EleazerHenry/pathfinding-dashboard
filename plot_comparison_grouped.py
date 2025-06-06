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

def plot_grouped_bar(data, metric, ylabel):
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    maps = sorted({map_name for algo_data in data.values() for map_name in algo_data})

    bar_width = 0.15
    index = np.arange(len(algorithms))
    offsets = np.linspace(-bar_width * len(maps) / 2, bar_width * len(maps) / 2, len(maps))

    plt.figure(figsize=(10, 6))

    for i, map_name in enumerate(maps):
        values = []
        for algo in algorithms:
            val = data[algo].get(map_name, {}).get(metric)
            values.append(val if val is not None else 0)
        bar_positions = index + offsets[i]
        plt.bar(bar_positions, values, width=bar_width, label=map_name)

    plt.xticks(index, [algo.upper() for algo in algorithms])
    plt.ylabel(ylabel)
    plt.title(f"{metric} Comparison Across Maps")
    plt.legend(title="Map")
    plt.tight_layout()
    filename = f"comparison_{metric}.png"
    plt.savefig(filename)
    print(f"✅ Saved: {filename}")
    plt.close()

if __name__ == "__main__":
    results = read_results("results.csv")
    plot_grouped_bar(results, "Nodes", "Nodes Expanded")
    plot_grouped_bar(results, "Length", "Path Length")
    plot_grouped_bar(results, "Cost", "Total Path Cost")
