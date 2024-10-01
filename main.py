import mesa
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from src.environment import World, TerrainType, ObstacleType
from src.agents import Player, Enemy, Neutral, create_agent, AgentType
from src.combat_system import CombatSystem
from src.ai_behavior import AIController

class SoulslikeModel(World):
    """A model with some number of agents."""
    def __init__(self, width, height, num_players, num_enemies, num_neutrals):
        super().__init__(width, height)
        self.num_players = num_players
        self.num_enemies = num_enemies
        self.num_neutrals = num_neutrals
        self.schedule = RandomActivation(self)
        
        self.initialize_agents()

        self.datacollector = DataCollector(
            model_reporters={
                "Player Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Player)]),
                "Enemy Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Enemy)]),
                "Neutral Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Neutral)])
            },
            agent_reporters={
                "Health": lambda a: a.health if hasattr(a, 'health') else None,
                "Stamina": lambda a: a.stamina if hasattr(a, 'stamina') else None,
                "Poise": lambda a: a.poise if hasattr(a, 'poise') else None,
                "Position": lambda a: a.pos
            }
        )

    def initialize_agents(self):
        """Initialize agents in the world."""
        for agent_type, count in [
            (AgentType.PLAYER, self.num_players),
            (AgentType.ENEMY, self.num_enemies),
            (AgentType.NEUTRAL, self.num_neutrals)
        ]:
            for _ in range(count):
                agent = create_agent(agent_type, self.next_id(), self)
                self.place_agent(agent)
                self.schedule.add(agent)

    def place_agent(self, agent):
        """Place an agent in a valid position in the world."""
        attempts = 0
        max_attempts = 100
        while attempts < max_attempts:
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            if self.is_valid_move(x, y):
                self.grid.place_agent(agent, (x, y))
                return True
            attempts += 1
        print(f"Warning: Could not place agent {agent.unique_id} after {max_attempts} attempts")
        return False

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.update_environment()

    def update_environment(self):
        """Update environmental effects and world state."""
        for agent in self.schedule.agents:
            self.apply_environmental_effect(agent)

    def get_distance(self, pos1, pos2):
        """Calculate the Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_model(width, height, num_players, num_enemies, num_neutrals, steps):
    """Run the model with the given parameters."""
    model = SoulslikeModel(width, height, num_players, num_enemies, num_neutrals)
    for i in range(steps):
        model.step()
    
    return model

if __name__ == "__main__":
    width, height = 20, 20
    num_players = 1
    num_enemies = 10
    num_neutrals = 5
    steps = 100

    model = run_model(width, height, num_players, num_enemies, num_neutrals, steps)
    print("Simulation completed successfully.")
    
    # Print final agent counts
    final_counts = model.datacollector.get_model_vars_dataframe().iloc[-1]
    print("Final agent counts:")
    for agent_type, count in final_counts.items():
        print(f"  {agent_type}: {count}")
    
    # Print some statistics about the agents
    agent_data = model.datacollector.get_agent_vars_dataframe()
    print("\nAgent Statistics:")
    for stat in ["Health", "Stamina", "Poise"]:
        if stat in agent_data.columns:
            print(f"  Average {stat}: {agent_data[stat].mean():.2f}")
    
    # Print the positions of remaining agents
    print("\nRemaining agent positions:")
    for agent in model.schedule.agents:
        print(f"  Agent {agent.unique_id} ({type(agent).__name__}): {agent.pos}")