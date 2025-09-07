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

    # Scenario 1: Facilitated Network Growth (Baseline)
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

    model = GovernanceModel(**params, seed=FIXED_SEED)

    print("Initial Network:")
    visualize_network(model, "Initial Network State", save_path="results/initial_network.png")

    for i in range(100):
        model.step()

    print("\nFinal Network:")
    visualize_network(model, "Final Network State", save_path="results/final_network.png")

    model1_model_data = model.datacollector.get_model_vars_dataframe()
    model1_agent_data = model.datacollector.get_agent_vars_dataframe()
    model1_model_data.to_csv("results/scenario1_model_data.csv")
    model1_agent_data.to_csv("results/scenario1_agent_data.csv")
    print("Model-level data (Scenario 1) saved to results/scenario1_model_data.csv")
    print("Agent-level data (Scenario 1) saved to results/scenario1_agent_data.csv")

    print("\n" + "-"*30)
    print("Running Scenario 2: Institutional Fragility and Key Actor Departure")
    print("-"*30 + "\n")

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

    model2 = GovernanceModel(**scenario2_params, seed=FIXED_SEED)

    print("Initial Network (Scenario 2):")
    visualize_network(model2, "Initial Network State (Scenario 2)", save_path="results/scenario2_initial_network.png")

    for i in range(100):
        model2.step()

    print("\nFinal Network (Scenario 2):")
    visualize_network(model2, "Final Network State (Scenario 2)", save_path="results/scenario2_final_network.png")

    model2_model_data = model2.datacollector.get_model_vars_dataframe()
    model2_agent_data = model2.datacollector.get_agent_vars_dataframe()
    model2_model_data.to_csv("results/scenario2_model_data.csv")
    model2_agent_data.to_csv("results/scenario2_agent_data.csv")
    print("Model-level data (Scenario 2) saved to results/scenario2_model_data.csv")
    print("Agent-level data (Scenario 2) saved to results/scenario2_agent_data.csv")

    print("\n" + "-"*30)
    print("Running Scenario 3: The Resource Opportunity Window")
    print("-"*30)

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

    model3 = GovernanceModel(**scenario3_params, seed=FIXED_SEED)

    print("Initial Network (Scenario 3):")
    visualize_network(model3, "Initial Network State (Scenario 3)", save_path="results/scenario3_initial_network.png")

    for i in range(100):
        model3.step()

    print("\nFinal Network (Scenario 3):")
    visualize_network(model3, "Final Network State (Scenario 3)", save_path="results/scenario3_final_network.png")

    model3_data = model3.datacollector.get_model_vars_dataframe()
    agent3_data = model3.datacollector.get_agent_vars_dataframe()

    print("\nModel-level Data (Scenario 3):")
    model3_data.to_csv("results/scenario3_model_data.csv")
    print("Model-level data saved to results/scenario3_model_data.csv")

    print("\nAgent-level Data (Scenario 3):")
    agent3_data.to_csv("results/scenario3_agent_data.csv")
    print("Agent-level data saved to results/scenario3_agent_data.csv")
