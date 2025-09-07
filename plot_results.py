import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

def lighten_color(color, amount=0.5):
    """Lightens the given color by multiplying (1-amount) by the color + amount."""
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = mcolors.to_rgb(c)
    c = [(1 - amount) * x + amount for x in c] # Lighten by moving towards white
    return c

def plot_time_series(metric_name, df_s1_all_runs, df_s2_all_runs, df_s3_all_runs, scenario_names, save_path):
    plt.figure(figsize=(12, 7))

    # Define colors for each scenario
    color_s1 = 'blue'
    color_s2 = 'orange'
    color_s3 = 'green'

    # Calculate mean and standard deviation for each scenario
    mean_s1 = df_s1_all_runs.groupby('Step')[metric_name].mean()
    std_s1 = df_s1_all_runs.groupby('Step')[metric_name].std()

    mean_s2 = df_s2_all_runs.groupby('Step')[metric_name].mean()
    std_s2 = df_s2_all_runs.groupby('Step')[metric_name].std()

    mean_s3 = df_s3_all_runs.groupby('Step')[metric_name].mean()
    std_s3 = df_s3_all_runs.groupby('Step')[metric_name].std()

    # Plot mean lines
    plt.plot(mean_s1.index, mean_s1, label=scenario_names[0], color=color_s1)
    plt.plot(mean_s2.index, mean_s2, label=scenario_names[1], color=color_s2)
    plt.plot(mean_s3.index, mean_s3, label=scenario_names[2], color=color_s3)

    # Plot spread (shadowed areas) with transparent fill and lighter borders
    plt.fill_between(mean_s1.index, mean_s1 - std_s1, mean_s1 + std_s1, color=color_s1, alpha=0.0)
    plt.plot(mean_s1.index, mean_s1 - std_s1, color=lighten_color(color_s1, 0.7), linestyle='--', linewidth=0.8)
    plt.plot(mean_s1.index, mean_s1 + std_s1, color=lighten_color(color_s1, 0.7), linestyle='--', linewidth=0.8)

    plt.fill_between(mean_s2.index, mean_s2 - std_s2, mean_s2 + std_s2, color=color_s2, alpha=0.0)
    plt.plot(mean_s2.index, mean_s2 - std_s2, color=lighten_color(color_s2, 0.7), linestyle='--', linewidth=0.8)
    plt.plot(mean_s2.index, mean_s2 + std_s2, color=lighten_color(color_s2, 0.7), linestyle='--', linewidth=0.8)

    plt.fill_between(mean_s3.index, mean_s3 - std_s3, mean_s3 + std_s3, color=color_s3, alpha=0.0)
    plt.plot(mean_s3.index, mean_s3 - std_s3, color=lighten_color(color_s3, 0.7), linestyle='--', linewidth=0.8)
    plt.plot(mean_s3.index, mean_s3 + std_s3, color=lighten_color(color_s3, 0.7), linestyle='--', linewidth=0.8)

    plt.xlabel("Step")
    plt.ylabel(metric_name)
    plt.title(f"Time Series of {metric_name} Across Scenarios (Mean +/- Std Dev)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.clf()
    plt.close()

if __name__ == "__main__":
    os.makedirs('results', exist_ok=True)

    # Load data for each scenario
    df_s1_all_runs = pd.read_csv("results/scenario1_model_data_all_runs.csv", index_col=[0, 1])
    df_s2_all_runs = pd.read_csv("results/scenario2_model_data_all_runs.csv", index_col=[0, 1])
    df_s3_all_runs = pd.read_csv("results/scenario3_model_data_all_runs.csv", index_col=[0, 1])

    scenario_names = ["Scenario 1: Baseline", "Scenario 2: EMU Departure", "Scenario 3: Resource Opportunity"]

    # Metrics to plot
    metrics_to_plot = [
        "Network Density",
        "Average Clustering",
        "Number of Active Edges",
        "Successful Projects",
        "Largest Connected Component Size",
        "Resource Node Degree",
        "Gini Coefficient",
    ]

    for metric in metrics_to_plot:
        # Handle cases where a metric might not be present in all dataframes (e.g., Resource Node Degree in S1/S2)
        # Fill missing columns with 0 for consistent plotting
        if metric not in df_s1_all_runs.columns:
            df_s1_all_runs[metric] = 0
        if metric not in df_s2_all_runs.columns:
            df_s2_all_runs[metric] = 0
        if metric not in df_s3_all_runs.columns:
            df_s3_all_runs[metric] = 0

        plot_time_series(
            metric,
            df_s1_all_runs,
            df_s2_all_runs,
            df_s3_all_runs,
            scenario_names,
            f"results/{metric.replace(' ', '_').replace('/', '_')}_time_series.png"
        )
    print("Time series plots generated in the results/ directory.")
