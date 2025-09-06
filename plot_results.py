import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_time_series(metric_name, df1, df2, df3, scenario_names, save_path):
    plt.figure(figsize=(12, 7))
    plt.plot(df1.index, df1[metric_name], label=scenario_names[0])
    plt.plot(df2.index, df2[metric_name], label=scenario_names[1])
    plt.plot(df3.index, df3[metric_name], label=scenario_names[2])

    plt.xlabel("Step")
    plt.ylabel(metric_name)
    plt.title(f"Time Series of {metric_name} Across Scenarios")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.clf()
    plt.close()

if __name__ == "__main__":
    os.makedirs('results', exist_ok=True)

    # Load data for each scenario
    df_s1 = pd.read_csv("results/scenario1_model_data.csv", index_col=0)
    df_s2 = pd.read_csv("results/scenario2_model_data.csv", index_col=0)
    df_s3 = pd.read_csv("results/scenario3_model_data.csv", index_col=0)

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
        if metric not in df_s1.columns:
            df_s1[metric] = 0
        if metric not in df_s2.columns:
            df_s2[metric] = 0
        if metric not in df_s3.columns:
            df_s3[metric] = 0

        plot_time_series(
            metric,
            df_s1,
            df_s2,
            df_s3,
            scenario_names,
            f"results/{metric.replace(' ', '_').replace('/', '_')}_time_series.png"
        )
    print("Time series plots generated in the results/ directory.")
