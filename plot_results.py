import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def read_results(csv_file):
    data = defaultdict(lambda: defaultdict(dict))
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            map_name = row['Map']
            algo = row['Algorithm']
            data[map_name][algo] = {
                "Nodes": int(row['Nodes Expanded']),
                "Length": int(row['Path Length']),
                "Cost": float(row['Total Cost']) if row['Total Cost'] != '-' else None,
                "Found": row['Found'] == "Yes"
            }
    return data

def plot_metric(data, metric, ylabel):
    for map_name, results in data.items():
        labels = []
        values = []
        for algo in ["a_star", "dijkstra", "greedy"]:
            if algo in results:
                value = results[algo][metric]
                labels.append(algo)
                values.append(value if value is not None else 0)

        plt.figure()
        plt.bar(labels, values, color=["green", "blue", "orange"])
        plt.title(f"{metric} on {map_name}")
        plt.ylabel(ylabel)
        plt.xlabel("Algorithm")
        plt.tight_layout()
        filename = f"{map_name}_{metric}.png".replace(".txt", "")
        plt.savefig(filename)
        print(f"✅ Saved plot: {filename}")
        plt.close()

if __name__ == "__main__":
    csv_file = "results.csv"
    data = read_results(csv_file)
    
    plot_metric(data, metric="Nodes", ylabel="Nodes Expanded")
    plot_metric(data, metric="Length", ylabel="Path Length")
    plot_metric(data, metric="Cost", ylabel="Total Path Cost")
