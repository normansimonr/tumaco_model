## LLM Prompt for Code Generation

You are an expert Python programmer specializing in agent-based modeling using the Mesa and NetworkX libraries. Your task is to write the complete Python code for a dynamic governance network model based on the detailed technical specification provided below. The goal is to create a clean, well-commented, and runnable script that implements the specified logic as simply as possible. Do not overcomplicate the model implementation.

**Instructions:**
1.  **Use the Provided Specification:** Adhere strictly to the agent attributes, model rules, and initialization logic described in the technical specification.
2.  **Technology Stack:** Use `mesa` for the ABM framework (Agent, Model, RandomActivation, NetworkGrid, DataCollector) and `networkx` for the graph.
3.  **Code Structure:** Organize the code into a single Python script (`governance_model.py`). This script should contain:
    *   An `AgentType` Enum.
    *   The `GovernanceAgent(mesa.Agent)` class.
    *   The `GovernanceModel(mesa.Model)` class.
    *   A `main` execution block that runs a simulation for **Scenario 1** by default.
4.  **Implementation Details:**
    *   **Initialization:** For the initial network, create a helper function that generates the specified "sparse bridging and dense bonding" structure. A simple way is to create N cliques (one for each agent type or subgroup) and then add a few random edges between these cliques.
    *   **Decision Logic:** Use simple probabilistic rules for agent decisions. For example, the probability of an agent `A` forming a link with agent `B` could be a weighted sum: `P(link) = w1 * homophily_score + w2 * resource_seeking_score`, where `homophily_score` is 1 if they are the same type and 0 otherwise, and `resource_seeking_score` is proportional to `(B.resources - A.resources)`.
    *   **Data Output:** At the end of the simulation run, print the model-level and agent-level data collected by the `DataCollector` as pandas DataFrames.
5.  **Visualization (Optional but Highly Recommended):** Include a function that uses Matplotlib and `networkx.draw()` to visualize the network state at the beginning and end of the simulation. In the visualization:
    *   Color nodes based on `agent_type`.
    *   Vary node size based on `resources`.
    *   Vary edge width or color intensity based on `relationship_strength`.

Please provide the full, runnable Python code with clear comments explaining the implementation of the core dynamics, such as forum events, link decay, collaboration attempts, and joint projects.

## Technical Specification: Agent-Based Governance Network Model

### 1. Overview
This document specifies a dynamic, agent-based model (ABM) designed to simulate the evolution of a fragile governance network. The model formalises qualitative findings about trust-building, institutional fragility, and actor motivation into a set of computational rules. Its purpose is to serve as a "thought experiment" to explore how micro-level interactions generate macro-level changes in network structure over time. The model will be implemented in Python, leveraging the Mesa framework for agent scheduling and data collection, and the NetworkX library for network representation and analysis.

### 2. Core Technologies
*   **Language:** Python 3.9+
*   **ABM Framework:** Mesa
*   **Network Management:** NetworkX
*   **Data Handling:** Pandas
*   **Visualization (Optional):** Matplotlib, Seaborn

### 3. Model Components

#### 3.1. Agents (Nodes)
The core entity of the model is the `GovernanceAgent`, which will be a subclass of `mesa.Agent`. Each agent represents an organizational actor and is a node in the NetworkX graph.

**Attributes:**

*   `unique_id` (int): Unique identifier for the agent, required by Mesa.
*   `model` (Model): A reference to the main model instance, required by Mesa.
*   `agent_type` (Enum): The agent's category.
    *   Enum values: `GOVERNMENT`, `CSO`, `PRIVATE_ENTERPRISE`, `ACADEMIC`.
*   `resources` (float): A value (e.g., 0.0 to 100.0) representing the agent's access to financial, technical, and logistical capital. Dynamically changes based on model events.
*   `commitment` (float): A value from 0.0 to 1.0 representing the agent's intrinsic willingness to engage. This influences its proactivity in initiating actions.
    *   CSOs: High initial commitment (e.g., 0.7-0.9).
    *   'Environmental Management Unit' (a single `GOVERNMENT` agent): High, fixed commitment (e.g., 0.95).
    *   Other `GOVERNMENT` agents: Low to medium, possibly variable commitment (e.g., 0.2-0.5).
    *   `PRIVATE_ENTERPRISE`: Medium commitment, driven by `motivation_profile`.
    *   `ACADEMIC` (Catalyst): High commitment (e.g., 0.8-1.0).
*   `motivation_profile` (float): A value from 0.0 to 1.0 balancing economic vs. socio-affective goals.
    *   `0.0`: Purely economic (maximise `resources`).
    *   `1.0`: Purely socio-affective (maximise `relationship_strength` and community benefit).
    *   This will be a parameter in decision-making functions. For example, `PRIVATE_ENTERPRISE` agents will have a low value (e.g., 0.1-0.3), while CSOs will have a high value (e.g., 0.8-0.9).

#### 3.2. Environment & Network (The Model Class)
The `GovernanceModel` will be a subclass of `mesa.Model` and will manage the overall simulation state, agent scheduling, and the network itself.

**Attributes:**

*   `schedule` (mesa.time.BaseScheduler): A scheduler to manage the order of agent activation at each step (e.g., `RandomActivation`).
*   `space` (mesa.space.NetworkGrid): A Mesa space that uses a NetworkX graph to define agent positions and connections.
*   `G` (networkx.Graph): The core NetworkX graph where agents are nodes and relationships are edges.
*   `datacollector` (mesa.DataCollector): To collect model- and agent-level data at each step.
*   Model Parameters: These will be passed to the `__init__` method to allow for flexible scenario testing. Examples include: `num_agents_per_type`, `link_decay_rate`, `forum_frequency`, `project_resource_threshold`.

#### 3.3. Links (Edges)
Links in the `G` graph represent working relationships between agents. They are weighted and directed or undirected (simple undirected graph is sufficient to start).

**Edge Attributes:**

*   `relationship_strength` (float): A value from 0.0 (no relationship) to 1.0 (strong, trusted collaboration). This is the primary dynamic attribute of an edge.

### 4. Model Dynamics & Rules (The `step()` method)
The simulation proceeds in discrete time steps (e.g., "months"). At each step, the following sequence of events occurs:

1.  **Trigger Forum Event (Model-level):**
    *   A probabilistic event occurs at each step, determined by a `forum_frequency` parameter.
    *   If triggered, the designated `ACADEMIC` "Catalyst" agent convenes a forum.
    *   A subset of agents "attend" the forum (e.g., the Catalyst and a random selection of agents, with attendance probability weighted by `commitment`).
    *   For every pair of agents attending the forum, the `relationship_strength` of the link between them is increased by a fixed amount (e.g., +0.1), capped at 1.0. If no link exists, one is created with an initial strength.

2.  **Link Decay (Model-level):**
    *   The `relationship_strength` of all existing edges in the network is multiplied by a decay factor (e.g., 0.98). This models the fragility of relationships that are not actively maintained. `strength_t+1 = strength_t * (1 - link_decay_rate)`.

3.  **Agent Activation (Agent-level `step()` method):**
    *   The scheduler activates each agent once per model step. The agent performs the following actions based on its attributes:
    *   **a. Attempt New Collaboration (Link Formation):**
        *   An agent decides whether to seek a new connection based on its `commitment`.
        *   If it decides to seek, it evaluates potential partners from the pool of agents it is not yet connected to.
        *   The probability of attempting to form a link with a target agent is a function of:
            *   **Homophily:** Higher probability if the target is the same `agent_type`.
            *   **Resource Seeking:** Higher probability if the agent's `resources` are low and the target's `resources` are high.
            *   The `motivation_profile` can weigh these two factors.
        *   If a link is successfully formed, a new edge is added to the graph with a small initial `relationship_strength` (e.g., 0.05).
    *   **b. Propose Joint Project:**
        *   The agent scans its existing neighbours.
        *   If it finds a neighbour with a `relationship_strength` above a certain threshold (e.g., > 0.6), it may propose a "Joint Project". The probability of proposing is again driven by `commitment`.
        *   A project is successfully initiated if the combined `resources` of the two agents exceed a `project_resource_threshold`.
        *   Successful projects are stored in a model-level list to be executed.

4.  **Execute Joint Projects (Model-level):**
    *   After all agents have acted, the model iterates through the list of successful projects initiated in the current step.
    *   For each project, the participating agents receive a "payoff":
        *   Their `resources` increase by a certain amount.
        *   The `relationship_strength` of the link between them increases significantly (e.g., +0.2), capped at 1.0. This creates a positive feedback loop.

### 5. Initialization (`__init__` method)
At the start of the simulation (t=0):

1.  **Agent Creation:** Create the specified number of agents for each of the four types, assigning their initial `resources`, `commitment`, and `motivation_profile` from predefined distributions that reflect the stylised facts (e.g., CSOs low resources, high commitment; Private Enterprise high resources, low motivation profile value). Designate one `GOVERNMENT` agent as the "Environmental Management Unit" and one `ACADEMIC` agent as the "Catalyst".
2.  **Network Initialization:**
    *   Create a sparse graph with high bonding and low bridging capital.
    *   **Method:** Create several small, dense clusters (cliques) where each cluster contains agents of the same type (e.g., a CSO cluster, a Government cluster).
    *   Add a few (1-3) random "bridging" edges between agents in different clusters to create an initially fragmented but connected graph.
    *   Initial `relationship_strength` is high for within-cluster edges (e.g., 0.7) and low for between-cluster edges (e.g., 0.1).

### 6. Simulation Scenarios & Experiments

#### Scenario 1: Facilitated Network Growth (Baseline)
*   **Setup:** Run the model with the `ACADEMIC` Catalyst agent actively triggering Forum Events at a regular frequency.
*   **Hypothesis:** The network's density and average clustering coefficient will increase over time. Bridging links will form, connecting the initial clusters.
*   **Metrics:** Network density, average clustering coefficient, number of components, distribution of agent `resources`.

#### Scenario 2: Institutional Fragility and Key Actor Departure
*   **Setup:** Run the model as in Scenario 1. At a specific midpoint in the simulation (e.g., step 50 of 100), remove the high-commitment "Environmental Management Unit" `GOVERNMENT` agent from the model.
*   **Hypothesis:** The network will see a sharp drop in cohesion (e.g., increase in shortest path length, potential disconnection of components). The overall rate of successful "Joint Projects" will decrease.
*   **Metrics:** All metrics from Scenario 1, plus tracking the size of the largest connected component.

#### Scenario 3: The Resource Opportunity Window
*   **Setup:** Run the model as in Scenario 1. At a midpoint (e.g., step 50), introduce a special "Resource Opportunity" node into the graph. This node has infinite resources.
*   **Dynamics:** Agents can now attempt to form links with this new node. The probability of successfully connecting is proportional to an agent's current total `resources` and its network centrality (e.g., degree or betweenness centrality).
*   **Hypothesis:** Agents that are already well-resourced and well-connected will be the primary beneficiaries, capturing the opportunity and potentially increasing resource inequality within the system.
*   **Metrics:** Gini coefficient of agent `resources` over time, degree distribution of the resource node.

### 7. Data Collection
The `mesa.DataCollector` will be configured to collect:
*   **Model-level reporters:**
    *   Network Density (`nx.density`)
    *   Average Clustering Coefficient (`nx.average_clustering`)
    *   Number of Active Edges
    *   Number of Successful Projects per Step
*   **Agent-level reporters:**
    *   `agent_type`
    *   `resources`
    *   `commitment`
    *   Degree Centrality of each agent (`G.degree[agent.unique_id]`)
