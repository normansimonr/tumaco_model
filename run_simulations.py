import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # Import for custom legend
import pandas as pd
from governance_model import AgentType, GovernanceAgent, GovernanceModel

FIXED_SEED = 42 # For replicable results

# Define discrete colors for each AgentType
AGENT_COLORS = {
    AgentType.GOVERNMENT: '#1f77b4',  # Blue
    AgentType.CSO: '#ff7f0e',       # Orange
    AgentType.PRIVATE_ENTERPRISE: '#2ca02c', # Green
    AgentType.ACADEMIC: '#d62728',   # Red
    AgentType.RESOURCE_NODE: '#9467bd', # Purple
}

def visualize_network(model, title="Network State", save_path=None):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(model.G, seed=42)  # For consistent layout

    # Get colors based on agent_type
    node_colors = [AGENT_COLORS[agent.agent_type] for agent in model.agent_set]
    node_sizes = [min(agent.resources * 5 + 100, 2000) for agent in model.agent_set]  # Scale resources for visibility, cap at 2000

    nx.draw_networkx_nodes(model.G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(model.G, pos, width=0.5, alpha=0.5, edge_color='gray')
    

    plt.title(title)
    
    # Create custom legend for discrete agent types
    legend_elements = [
        mpatches.Patch(color=color, label=agent_type.name.replace('_', ' ').title())
        for agent_type, color in AGENT_COLORS.items()
    ]
    plt.legend(handles=legend_elements, title="Agent Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight') # Use bbox_inches='tight' to include legend
        plt.clf()
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)

    NUM_RUNS = 100 # Number of simulation runs for statistical validity

    # Scenario 1: Facilitated Network Growth (Baseline)
    print("Running Scenario 1: Facilitated Network Growth ({} runs)".format(NUM_RUNS))
    scenario1_model_data_runs = []
    scenario1_agent_data_runs = []

    for i in range(NUM_RUNS):
        # Re-initialize model for each run
        params = {
            "num_agents_per_type": {
                AgentType.GOVERNMENT: 5,
                AgentType.CSO: 5,
                AgentType.PRIVATE_ENTERPRISE: 3,
                AgentType.ACADEMIC: 2,
            },
            "link_decay_rate": 0.02,
            "forum_frequency": 0.2,
            "project_resource_threshold": 100,
        }
        model = GovernanceModel(**params, seed=FIXED_SEED + i) # Use a different seed for each run

        # Only visualize the first run's initial and final state for representative purposes
        if i == 0:
            print("Initial Network (Run 1):")
            visualize_network(model, "Initial Network State (Run 1)", save_path="results/initial_network.png")

        for step in range(100):
            model.step()

        if i == 0:
            print("\nFinal Network (Run 1):")
            visualize_network(model, "Final Network State (Run 1)", save_path="results/final_network.png")

        scenario1_model_data_runs.append(model.datacollector.get_model_vars_dataframe())
        scenario1_agent_data_runs.append(model.datacollector.get_agent_vars_dataframe())

    # Concatenate and save aggregated data for Scenario 1
    full_scenario1_model_data = pd.concat(scenario1_model_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario1_agent_data = pd.concat(scenario1_agent_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario1_model_data.to_csv("results/scenario1_model_data_all_runs.csv")
    full_scenario1_agent_data.to_csv("results/scenario1_agent_data_all_runs.csv")
    print("Model-level data (Scenario 1, all runs) saved to results/scenario1_model_data_all_runs.csv")
    print("Agent-level data (Scenario 1, all runs) saved to results/scenario1_agent_data_all_runs.csv")

    print("\n" + "-"*30)
    print("Running Scenario 2: Institutional Fragility and Key Actor Departure ({} runs)".format(NUM_RUNS))
    scenario2_model_data_runs = []
    scenario2_agent_data_runs = []

    for i in range(NUM_RUNS):
        scenario2_params = {
            "num_agents_per_type": {
                AgentType.GOVERNMENT: 5,
                AgentType.CSO: 5,
                AgentType.PRIVATE_ENTERPRISE: 3,
                AgentType.ACADEMIC: 2,
            },
            "link_decay_rate": 0.02,
            "forum_frequency": 0.2,
            "project_resource_threshold": 100,
            "midpoint_removal_step": 50,
        }
        model2 = GovernanceModel(**scenario2_params, seed=FIXED_SEED + i) # Use a different seed for each run

        if i == 0:
            print("Initial Network (Scenario 2, Run 1):")
            visualize_network(model2, "Initial Network State (Scenario 2, Run 1)", save_path="results/scenario2_initial_network.png")

        for step in range(100):
            model2.step()

        if i == 0:
            print("\nFinal Network (Scenario 2, Run 1):")
            visualize_network(model2, "Final Network State (Scenario 2, Run 1)", save_path="results/scenario2_final_network.png")

        scenario2_model_data_runs.append(model2.datacollector.get_model_vars_dataframe())
        scenario2_agent_data_runs.append(model2.datacollector.get_agent_vars_dataframe())

    # Concatenate and save aggregated data for Scenario 2
    full_scenario2_model_data = pd.concat(scenario2_model_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario2_agent_data = pd.concat(scenario2_agent_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario2_model_data.to_csv("results/scenario2_model_data_all_runs.csv")
    full_scenario2_agent_data.to_csv("results/scenario2_agent_data_all_runs.csv")
    print("Model-level data (Scenario 2, all runs) saved to results/scenario2_model_data_all_runs.csv")
    print("Agent-level data (Scenario 2, all runs) saved to results/scenario2_agent_data_all_runs.csv")

    print("\n" + "-"*30)
    print("Running Scenario 3: The Resource Opportunity Window ({} runs)".format(NUM_RUNS))
    scenario3_model_data_runs = []
    scenario3_agent_data_runs = []

    for i in range(NUM_RUNS):
        scenario3_params = {
            "num_agents_per_type": {
                AgentType.GOVERNMENT: 5,
                AgentType.CSO: 5,
                AgentType.PRIVATE_ENTERPRISE: 3,
                AgentType.ACADEMIC: 2,
            },
            "link_decay_rate": 0.02,
            "forum_frequency": 0.2,
            "project_resource_threshold": 100,
            "resource_node_introduction_step": 50,
        }
        model3 = GovernanceModel(**scenario3_params, seed=FIXED_SEED + i) # Use a different seed for each run

        if i == 0:
            print("Initial Network (Scenario 3, Run 1):")
            visualize_network(model3, "Initial Network State (Scenario 3, Run 1)", save_path="results/scenario3_initial_network.png")

        for step in range(100):
            model3.step()

        if i == 0:
            print("\nFinal Network (Scenario 3, Run 1):")
            visualize_network(model3, "Final Network State (Scenario 3, Run 1)", save_path="results/scenario3_final_network.png")

        scenario3_model_data_runs.append(model3.datacollector.get_model_vars_dataframe())
        scenario3_agent_data_runs.append(model3.datacollector.get_agent_vars_dataframe())

    # Concatenate and save aggregated data for Scenario 3
    full_scenario3_model_data = pd.concat(scenario3_model_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario3_agent_data = pd.concat(scenario3_agent_data_runs, keys=range(NUM_RUNS), names=['Run', 'Step'])
    full_scenario3_model_data.to_csv("results/scenario3_model_data_all_runs.csv")
    full_scenario3_agent_data.to_csv("results/scenario3_agent_data_all_runs.csv")
    print("Model-level data (Scenario 3, all runs) saved to results/scenario3_model_data_all_runs.csv")
    print("Agent-level data (Scenario 3, all runs) saved to results/scenario3_agent_data_all_runs.csv")
