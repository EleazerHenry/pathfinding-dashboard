import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import io
import csv
from a_star_pathfinding_multi import load_grid_from_txt, search, bfs, dfs
import xlsxwriter
from fpdf import FPDF

@st.cache_data
def load_results(csv_file="results.csv"):
    if not os.path.exists(csv_file):
        return pd.DataFrame()
    return pd.read_csv(csv_file)

def update_results_csv(new_entries, csv_file="results.csv"):
    headers = ["Map", "Algorithm", "Time(s)", "Nodes Expanded", "Path Length", "Total Cost", "Found"]
    file_exists = os.path.exists(csv_file)
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(new_entries)

def run_benchmark_on_upload(map_name, grid, start, goal):
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    results = []

    for algo in algorithms:
        if algo in ["a_star", "dijkstra", "greedy"]:
            path, visited = search(grid, start, goal, algorithm=algo)
        elif algo == "bfs":
            path, visited = bfs(grid, start, goal)
        elif algo == "dfs":
            path, visited = dfs(grid, start, goal)

        found = bool(path)
        path_len = len(path) if path else 0
        cost = sum([1 for _ in path]) if path else "-"
        nodes_exp = len(visited)

        results.append([
            map_name,
            algo,
            "",
            nodes_exp,
            path_len,
            f"{cost:.2f}" if found else "-",
            "Yes" if found else "No"
        ])
    return results

def export_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
        writer.save()
    return output.getvalue()

def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Pathfinding Algorithm Results", ln=True, align='C')
    for i, row in df.iterrows():
        pdf.cell(200, 8, txt=str(row.to_dict()), ln=True)
    output = io.BytesIO()
    pdf.output(output)
    return output.getvalue()

def plot_radar_live(df, selected_map):
    metrics = ["Nodes Expanded", "Path Length", "Total Cost"]
    algorithms = ["a_star", "dijkstra", "greedy", "bfs", "dfs"]
    labels = ['Nodes', 'Length', 'Cost']
    colors = ['green', 'blue', 'orange', 'purple', 'gray']

    data = df[df["Map"] == selected_map]

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]  # Loop back to start

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for algo, color in zip(algorithms, colors):
        subset = data[data["Algorithm"] == algo]
        if subset.empty:
            continue
        values = [
            subset["Nodes Expanded"].values[0],
            subset["Path Length"].values[0],
            float(subset["Total Cost"].values[0]) if subset["Total Cost"].values[0] != "-" else 0
        ]
        max_vals = [max(df[m]) for m in metrics]
        norm_values = [v / m if m > 0 else 0 for v, m in zip(values, max_vals)]
        norm_values += norm_values[:1]
        ax.plot(angles, norm_values, label=algo.upper(), color=color)
        ax.fill(angles, norm_values, alpha=0.1, color=color)

    ax.set_title(f"Radar Chart: {selected_map}")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'])
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig)

def main():
    st.set_page_config(layout="wide")
    st.title("🧭 Pathfinding Dashboard with Upload + Live Radar + Export")

    # --- Upload Section ---
    st.sidebar.header("📥 Upload New Grid Map")
    uploaded_txt = st.sidebar.file_uploader("Upload .txt Map", type="txt")
    uploaded_json = st.sidebar.file_uploader("Upload .json Metadata (optional)", type="json")

    if uploaded_txt:
        map_name = uploaded_txt.name
        grid = [[int(cell) for cell in line.strip().split()] for line in uploaded_txt.getvalue().decode().splitlines()]
        start, goal = (0, 0), (len(grid)-1, len(grid[0])-1)

        if uploaded_json:
            meta = json.load(uploaded_json)
            start = tuple(meta.get("start", start))
            goal = tuple(meta.get("goal", goal))

        st.sidebar.success(f"Running benchmark for {map_name}")
        results = run_benchmark_on_upload(map_name, grid, start, goal)
        update_results_csv(results)
        st.sidebar.success("✅ Benchmark complete! Data added.")

        # 🔁 Force reload results after benchmark
        df = pd.read_csv("results.csv")
    else:
        df = load_results()

    if df.empty:
        st.warning("⚠️ No results available. Upload a map to get started.")
        return

    # --- Visualization & Interaction Section ---
    maps = df['Map'].unique()
    selected_map = st.selectbox("Select a Map", maps)

    col1, col2 = st.columns([2, 1])
    metric = col1.radio("Metric to Compare", ["Nodes Expanded", "Path Length", "Total Cost"])
    filtered = df[df['Map'] == selected_map]
    fig, ax = plt.subplots()
    ax.bar(filtered['Algorithm'].str.upper(), filtered[metric], color='teal')
    ax.set_title(f"{metric} for {selected_map}")
    ax.set_ylabel(metric)
    col1.pyplot(fig)

    with col2:
        st.markdown("🕸 **Live Radar Chart**")
        plot_radar_live(df, selected_map)

    st.subheader("📋 Results Table")
    st.dataframe(filtered.reset_index(drop=True))

    # --- Export Section ---
    st.subheader("💾 Export Results")
    export_format = st.radio("Choose format", ["Excel", "PDF"], horizontal=True)
    if st.button("Download"):
        if export_format == "Excel":
            st.download_button("📥 Download Excel", export_excel(df), file_name="results.xlsx")
        elif export_format == "PDF":
            st.download_button("📥 Download PDF", export_pdf(df), file_name="results.pdf")

    st.markdown("---")
    st.markdown("Created by **Kobby** | Powered by Streamlit")

if __name__ == "__main__":
    main()
