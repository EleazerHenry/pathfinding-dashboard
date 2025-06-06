import csv
import matplotlib.pyplot as plt
import numpy as np

def read_results(csv_file):
    data = {}
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            map_name = row['Map']
            algo = row['Algorithm']
            if map_name not in data:
                data[map_name] = {}
            data[map_name][algo] = {
                "Nodes": int(row['Nodes Expanded']),
                "Length": int(row['Path Length']),
                "Cost": float(row['Total Cost']) if row['Total Cost'] != '-' else 0
            }
    return data

def plot_stacked_bar(data, map_name):
    metrics = ['Nodes', 'Length', 'Cost']
    colors = ['skyblue', 'orange', 'lightgreen']
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    
    values = {metric: [] for metric in metrics}

    for algo in algorithms:
        entry = data[map_name].get(algo, {"Nodes": 0, "Length": 0, "Cost": 0})
        for metric in metrics:
            values[metric].append(entry[metric])

    bar_width = 0.6
    x = np.arange(len(algorithms))

    bottom = np.zeros(len(algorithms))
    plt.figure(figsize=(10, 6))
    
    for metric, color in zip(metrics, colors):
        plt.bar(x, values[metric], bar_width, bottom=bottom, label=metric, color=color)
        bottom += np.array(values[metric])

    plt.title(f"Stacked Bar Chart: {map_name}")
    plt.xlabel("Algorithm")
    plt.ylabel("Total Effort")
    plt.xticks(x, [a.upper() for a in algorithms])
    plt.legend()
    plt.tight_layout()

    filename = f"{map_name.replace('.txt', '')}_stacked_bar.png"
    plt.savefig(filename)
    print(f"✅ Saved: {filename}")
    plt.close()

if __name__ == "__main__":
    results = read_results("results.csv")
    for map_name in results:
        plot_stacked_bar(results, map_name)
