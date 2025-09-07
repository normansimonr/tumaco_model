
import enum
import random
import networkx as nx
import mesa
from mesa.agent import AgentSet
from mesa.datacollection import DataCollector

class AgentType(enum.Enum):
    GOVERNMENT = 1
    CSO = 2
    PRIVATE_ENTERPRISE = 3
    ACADEMIC = 4
    RESOURCE_NODE = 5

class GovernanceAgent(mesa.Agent):
    """An agent representing an organizational actor in the governance network."""

    def __init__(self, model, agent_type, resources, commitment, motivation_profile):
        super().__init__(model)
        self.agent_type = agent_type
        self.resources = resources
        self.commitment = commitment
        self.motivation_profile = motivation_profile

    def step(self):
        """Agent's step function."""
        self.attempt_new_collaboration()
        self.propose_joint_project()

    def attempt_new_collaboration(self):
        """Attempt to form a new link with another agent."""
        if self.random.random() < self.commitment:
            possible_partners = [
                agent
                for agent in self.model.agent_set
                if agent.unique_id != self.unique_id and not self.model.G.has_edge(self.unique_id, agent.unique_id)
            ]

            # Add resource node as a possible partner if it exists and is not connected
            if hasattr(self.model, 'resource_node') and self.model.resource_node.unique_id != self.unique_id and not self.model.G.has_edge(self.unique_id, self.model.resource_node.unique_id):
                possible_partners.append(self.model.resource_node)

            if possible_partners:
                partner = self.random.choice(possible_partners)
                
                # Simplified probability calculation
                if hasattr(partner, "is_resource_node"):
                    # Probability for resource node: proportional to agent's resources and degree
                    agent_degree = self.model.G.degree[self.unique_id] if self.unique_id in self.model.G else 0
                    prob = (self.resources / 100.0) * (agent_degree / (len(self.model.agent_set) - 1)) # Normalize resources and degree
                else:
                    homophily_score = 1 if self.agent_type == partner.agent_type else 0
                    resource_seeking_score = max(0, (partner.resources - self.resources) / 100)
                    
                    # Motivation profile weighs the scores
                    prob = (self.motivation_profile * homophily_score + 
                            (1 - self.motivation_profile) * resource_seeking_score)
                
                if self.random.random() < prob:
                    self.model.G.add_edge(self.unique_id, partner.unique_id, relationship_strength=0.05)

    def propose_joint_project(self):
        """Propose a joint project with a neighbor."""
        if self.random.random() < self.commitment:
            neighbors = list(self.model.G.neighbors(self.unique_id))
            if neighbors:
                partner = self.random.choice(neighbors)
                if self.model.G[self.unique_id][partner]['relationship_strength'] > 0.6:
                    if (self.resources + self.model.G.nodes[partner]['agent'].resources) > self.model.project_resource_threshold:
                        self.model.successful_projects.append((self.unique_id, partner))


class GovernanceModel(mesa.Model):
    """The main model for the governance network simulation."""

    def __init__(self, num_agents_per_type, link_decay_rate, forum_frequency, project_resource_threshold, midpoint_removal_step=None, resource_node_introduction_step=None, seed=None):
        super().__init__(seed=seed)
        self.num_agents_per_type = num_agents_per_type
        self.link_decay_rate = link_decay_rate
        self.forum_frequency = forum_frequency
        self.project_resource_threshold = project_resource_threshold
        self.midpoint_removal_step = midpoint_removal_step
        self.resource_node_introduction_step = resource_node_introduction_step
        self.agent_set = AgentSet([], self.random)
        self.G = nx.Graph()
        self.space = mesa.space.NetworkGrid(self.G)
        self.successful_projects = []
        self.running = True # Control simulation loop
        self.schedule = mesa.time.RandomActivation(self) # Initialize scheduler

        # Create agents
        self.create_agents()

        # Initialize network
        self.initialize_network()

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Network Density": lambda m: nx.density(m.G),
                "Average Clustering": lambda m: nx.average_clustering(m.G),
                "Number of Active Edges": lambda m: m.G.number_of_edges(),
                "Successful Projects": lambda m: len(m.successful_projects),
                "Largest Connected Component Size": lambda m: len(max(nx.connected_components(m.G), key=len)) if m.G.nodes else 0,
                "Resource Node Degree": lambda m: m.G.degree[m.resource_node.unique_id] if hasattr(m, 'resource_node') and m.resource_node.unique_id in m.G else 0,
                "Gini Coefficient": lambda m: self.calculate_gini(m.agent_set),
            },
            agent_reporters={
                "agent_type": "agent_type",
                "resources": "resources",
                "commitment": "commitment",
                "Degree Centrality": lambda a: a.model.G.degree[a.unique_id] if a.unique_id in a.model.G else 0,
            },
        )

    def calculate_gini(self, agent_set):
        """Calculates the Gini coefficient for agent resources."""
        if not agent_set:
            return 0.0
        resources = sorted([agent.resources for agent in agent_set])
        n = len(resources)
        if n <= 1:
            return 0.0
        
        numerator = sum((2 * i + 1 - n) * resources[i] for i in range(n))
        denominator = n * sum(resources)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator

    def create_agents(self):
        """Create the agents for the model."""
        for agent_type in AgentType:
            if agent_type == AgentType.RESOURCE_NODE: # Resource node is created dynamically
                continue
            for _ in range(self.num_agents_per_type[agent_type]):
                resources = self.random.uniform(10, 50)
                commitment = self.random.uniform(0.2, 0.8)
                motivation_profile = self.random.uniform(0.2, 0.8)

                if agent_type == AgentType.CSO:
                    commitment = self.random.uniform(0.7, 0.9)
                    resources = self.random.uniform(10, 30)
                    motivation_profile = self.random.uniform(0.8, 0.9)
                elif agent_type == AgentType.GOVERNMENT:
                    commitment = self.random.uniform(0.2, 0.5)
                elif agent_type == AgentType.PRIVATE_ENTERPRISE:
                    resources = self.random.uniform(50, 100)
                    motivation_profile = self.random.uniform(0.1, 0.3)
                elif agent_type == AgentType.ACADEMIC:
                    commitment = self.random.uniform(0.8, 1.0)

                agent = GovernanceAgent(self, agent_type, resources, commitment, motivation_profile)
                self.agent_set.add(agent)
                self.G.add_node(agent.unique_id, agent=agent)
        
        # Designate special agents
        govt_agents = [a for a in self.agent_set if a.agent_type == AgentType.GOVERNMENT]
        if govt_agents:
            emu = self.random.choice(govt_agents)
            emu.commitment = 0.95
            # Add an attribute to identify it
            setattr(emu, "is_emu", True)

        academic_agents = [a for a in self.agent_set if a.agent_type == AgentType.ACADEMIC]
        if academic_agents:
            catalyst = self.random.choice(academic_agents)
            # Add an attribute to identify it
            setattr(catalyst, "is_catalyst", True)


    def initialize_network(self):
        """Create a sparse graph with high bonding and low bridging capital."""
        agent_map = {agent_type: [] for agent_type in AgentType}
        for agent in self.agent_set:
            agent_map[agent.agent_type].append(agent.unique_id)

        # Create cliques
        for agent_type, agents in agent_map.items():
            for i in range(len(agents)):
                for j in range(i + 1, len(agents)):
                    self.G.add_edge(agents[i], agents[j], relationship_strength=0.7)
        
        # Add bridging edges
        for _ in range(3): # Add 3 random bridging edges
            agent1 = self.random.choice(self.agent_set)
            agent2 = self.random.choice(self.agent_set)
            if agent1.agent_type != agent2.agent_type:
                self.G.add_edge(agent1.unique_id, agent2.unique_id, relationship_strength=0.1)


    def trigger_forum_event(self):
        """Trigger a forum event."""
        if self.random.random() < self.forum_frequency:
            catalyst = next((a for a in self.agent_set if hasattr(a, "is_catalyst")), None)
            if catalyst:
                attendees = [catalyst]
                for agent in self.agent_set:
                    if agent != catalyst and self.random.random() < agent.commitment:
                        attendees.append(agent)
                
                for i in range(len(attendees)):
                    for j in range(i + 1, len(attendees)):
                        u, v = attendees[i].unique_id, attendees[j].unique_id
                        if self.G.has_edge(u, v):
                            self.G[u][v]['relationship_strength'] = min(1.0, self.G[u][v]['relationship_strength'] + 0.1)
                        else:
                            self.G.add_edge(u, v, relationship_strength=0.1)

    def link_decay(self):
        """Decay the relationship strength of all edges."""
        for u, v, d in self.G.edges(data=True):
            d['relationship_strength'] *= (1 - self.link_decay_rate)

    def execute_joint_projects(self):
        """Execute successful joint projects."""
        for u, v in self.successful_projects:
            agent_u = self.G.nodes[u]['agent']
            agent_v = self.G.nodes[v]['agent']
            
            agent_u.resources += 10
            agent_v.resources += 10
            
            if self.G.has_edge(u, v):
                self.G[u][v]['relationship_strength'] = min(1.0, self.G[u][v]['relationship_strength'] + 0.2)
        
        self.successful_projects = []


    def step(self):
        """Advance the model by one step."""
        self.schedule.step() # Advance the scheduler

        if self.midpoint_removal_step and self.schedule.steps == self.midpoint_removal_step:
            emu_agent = next((a for a in self.agent_set if hasattr(a, "is_emu")), None)
            if emu_agent:
                print(f"Removing EMU agent {emu_agent.unique_id} at step {self.schedule.steps}")
                self.agent_set.remove(emu_agent)
                self.G.remove_node(emu_agent.unique_id)

        if self.resource_node_introduction_step and self.schedule.steps == self.resource_node_introduction_step:
            resource_node_agent = GovernanceAgent(self, AgentType.RESOURCE_NODE, 1000000.0, 1.0, 0.5) # High resources, high commitment
            self.agent_set.add(resource_node_agent)
            self.G.add_node(resource_node_agent.unique_id, agent=resource_node_agent)
            self.resource_node = resource_node_agent
            setattr(resource_node_agent, "is_resource_node", True)
            print(f"Introducing Resource Node {resource_node_agent.unique_id} at step {self.schedule.steps}")

        self.trigger_forum_event()
        self.link_decay()
        self.execute_joint_projects()
        self.datacollector.collect(self)



