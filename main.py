import mesa
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from src.environment import World, TerrainType, ObstacleType
from src.agents import Player, Enemy, Neutral

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
            model_reporters={"Player Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Player)]),
                             "Enemy Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Enemy)]),
                             "Neutral Count": lambda m: len([a for a in m.schedule.agents if isinstance(a, Neutral)])},
            agent_reporters={"Health": lambda a: a.health if hasattr(a, 'health') else None}
        )

    def initialize_agents(self):
        """Initialize agents in the world."""
        # Create players
        for i in range(self.num_players):
            player = Player(self.next_id(), self)
            self.place_agent(player)
            self.schedule.add(player)

        # Create enemies
        for i in range(self.num_enemies):
            enemy = Enemy(self.next_id(), self)
            self.place_agent(enemy)
            self.schedule.add(enemy)

        # Create neutral NPCs
        for i in range(self.num_neutrals):
            neutral = Neutral(self.next_id(), self)
            self.place_agent(neutral)
            self.schedule.add(neutral)

    def place_agent(self, agent):
        """Place an agent in a valid position in the world."""
        while True:
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            if self.is_valid_move(x, y):
                self.grid.place_agent(agent, (x, y))
                break

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

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
    print(f"Final agent counts: {model.datacollector.get_model_vars_dataframe().iloc[-1]}")