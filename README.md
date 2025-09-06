# Agent-Based Governance Network Model

## Overview
This project implements a dynamic, agent-based model (ABM) designed to simulate the evolution of a fragile governance network. The model formalizes qualitative findings about trust-building, institutional fragility, and actor motivation into a set of computational rules. Its purpose is to serve as a "thought experiment" to explore how micro-level interactions generate macro-level changes in network structure over time. The model is implemented in Python, leveraging the Mesa framework for agent scheduling and data collection, and the NetworkX library for network representation and analysis.

## How to Use

### Prerequisites
*   Python 3.9+
*   `pip` (Python package installer)

### Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/tumaco_model.git
    cd tumaco_model
    ```
2.  **Create and activate a virtual environment:**
    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    (On Windows, use `venv\Scripts\activate` instead of `source venv/bin/activate`)

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Simulations
To run the simulations and generate results (network visualizations and data CSVs), execute the `run_simulations.py` script:
```bash
python3 run_simulations.py
```
This will run all three predefined scenarios.

## Simulation Scenarios and Questions

The model explores different hypotheses through three distinct simulation scenarios:

### Scenario 1: Facilitated Network Growth (Baseline)
*   **Setup:** The model runs with an `ACADEMIC` "Catalyst" agent actively triggering Forum Events at a regular frequency, facilitating interactions.
*   **Question:** How does consistent facilitation influence the growth and density of the governance network?
*   **Hypothesis:** The network's density and average clustering coefficient will increase over time. Bridging links will form, connecting initial clusters, leading to a more cohesive network.

### Scenario 2: Institutional Fragility and Key Actor Departure
*   **Setup:** The model runs as in Scenario 1, but at a specific midpoint (step 50), a high-commitment "Environmental Management Unit" (`GOVERNMENT`) agent is removed from the model.
*   **Question:** What is the impact of the sudden departure of a key, highly committed actor on the network's cohesion and project success?
*   **Hypothesis:** The network will experience a sharp drop in cohesion (e.g., increase in shortest path length, potential disconnection of components). The overall rate of successful "Joint Projects" will decrease, highlighting institutional fragility.

### Scenario 3: The Resource Opportunity Window
*   **Setup:** The model runs as in Scenario 1, but at a midpoint (step 50), a special "Resource Opportunity" node with effectively infinite resources is introduced into the graph. Agents can attempt to form links with this new node.
*   **Question:** How does the introduction of a significant, external resource opportunity affect resource distribution and network structure, particularly benefiting well-resourced and well-connected agents?
*   **Hypothesis:** Agents that are already well-resourced and well-connected will be the primary beneficiaries, capturing the opportunity and potentially increasing resource inequality within the system.

## Outputs
Upon running `run_simulations.py`, the following outputs will be generated in the `results/` directory:
*   `initial_network.png`: Visualization of the network at the start of Scenario 1.
*   `final_network.png`: Visualization of the network at the end of Scenario 1.
*   `scenario2_initial_network.png`: Visualization of the network at the start of Scenario 2.
*   `scenario2_final_network.png`: Visualization of the network at the end of Scenario 2.
*   `scenario3_initial_network.png`: Visualization of the network at the start of Scenario 3.
*   `scenario3_final_network.png`: Visualization of the network at the end of Scenario 3.
*   `scenario3_model_data.csv`: Model-level data collected during Scenario 3.
*   `scenario3_agent_data.csv`: Agent-level data collected during Scenario 3.