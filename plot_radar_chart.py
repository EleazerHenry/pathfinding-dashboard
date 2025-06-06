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
                "Cost": float(row['Total Cost']) if row['Total Cost'] != '-' else None,
                "Found": row['Found'] == "Yes"
            }
    return data

def normalize(values):
    max_val = max(values)
    return [v / max_val if max_val != 0 else 0 for v in values]

def plot_radar(metrics_data, map_name):
    labels = ['Nodes', 'Length', 'Cost']
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    colors = ['green', 'blue', 'orange', 'purple', 'gray']

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # loop back to start

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for algo, color in zip(algorithms, colors):
        if algo in metrics_data:
            raw = metrics_data[algo]
            values = [raw['Nodes'], raw['Length'], raw['Cost'] if raw['Cost'] is not None else 0]
            values = normalize(values)
            values += values[:1]
            ax.plot(angles, values, label=algo.upper(), color=color)
            ax.fill(angles, values, alpha=0.1, color=color)

    ax.set_title(f"Radar Chart: {map_name}")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'])
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()

    filename = f"{map_name.replace('.txt', '')}_radar.png"
    plt.savefig(filename)
    print(f"✅ Saved: {filename}")
    plt.close()

if __name__ == "__main__":
    results = read_results("results.csv")
    for map_name, metrics in results.items():
        plot_radar(metrics, map_name)
