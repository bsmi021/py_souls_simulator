from mesa.time import RandomActivation
from src.environment import World, TerrainType, ObstacleType
from src.agents import Player, Enemy, Neutral, create_agent, AgentType
from src.combat_system import CombatSystem
from src.ai_behavior import AIController
from src.ui import SoulslikeUI

class SoulslikeModel(World):
    """A model with some number of agents."""
    def __init__(self, width, height, num_players, num_enemies, num_neutrals):
        super().__init__(width, height)
        self.schedule = RandomActivation(self)
        self.num_players = num_players
        self.num_enemies = num_enemies
        self.num_neutrals = num_neutrals
        self.initialize_agents()

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
        while True:
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            if self.is_valid_move(x, y):
                self.grid.place_agent(agent, (x, y))
                return True
        
    def step(self):
        self.schedule.step()
        self.update_environment()

    def update_environment(self):
        """Update environmental effects and world state."""
        for agent in self.schedule.agents:
            self.apply_environmental_effect(agent)

def run_model(width, height, num_players, num_enemies, num_neutrals):
    """Run the model with the given parameters."""
    model = SoulslikeModel(width, height, num_players, num_enemies, num_neutrals)
    ui = SoulslikeUI(model)
    ui.run()

if __name__ == "__main__":
    width, height = 20, 20
    num_players = 1
    num_enemies = 5
    num_neutrals = 2

    run_model(width, height, num_players, num_enemies, num_neutrals)