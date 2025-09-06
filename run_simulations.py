import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from governance_model import AgentType, GovernanceAgent, GovernanceModel

def visualize_network(model, title="Network State", save_path=None):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(model.G, seed=42)  # For consistent layout

    node_colors = [agent.agent_type.value for agent in model.agent_set]
    node_sizes = [agent.resources * 5 + 100 for agent in model.agent_set]  # Scale resources for visibility

    nx.draw_networkx_nodes(model.G, pos, node_color=node_colors, node_size=node_sizes, cmap=plt.cm.get_cmap('viridis'), alpha=0.8)
    nx.draw_networkx_edges(model.G, pos, width=0.5, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(model.G, pos, font_size=8)

    plt.title(title)
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.get_cmap('viridis')), ax=plt.gca(), label='Agent Type')
    
    if save_path:
        plt.savefig(save_path)
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

    model = GovernanceModel(**params)

    print("Initial Network:")
    visualize_network(model, "Initial Network State", save_path="results/initial_network.png")

    for i in range(100):
        model.step()

    print("\nFinal Network:")
    visualize_network(model, "Final Network State", save_path="results/final_network.png")

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

    model2 = GovernanceModel(**scenario2_params)

    print("Initial Network (Scenario 2):")
    visualize_network(model2, "Initial Network State (Scenario 2)", save_path="results/scenario2_initial_network.png")

    for i in range(100):
        model2.step()

    print("\nFinal Network (Scenario 2):")
    visualize_network(model2, "Final Network State (Scenario 2)", save_path="results/scenario2_final_network.png")

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

    model3 = GovernanceModel(**scenario3_params)

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
