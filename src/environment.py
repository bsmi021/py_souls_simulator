from mesa import Model
from mesa.space import MultiGrid
import numpy as np
from enum import Enum

class TerrainType(Enum):
    DEFAULT = 0
    GRASS = 1
    STONE = 2
    WATER = 3
    LAVA = 4
    POISON_SWAMP = 5

class ObstacleType(Enum):
    WALL = 0
    TREE = 1
    ROCK = 2
    CHEST = 3
    BONFIRE = 4

class Cell:
    """Represents a single cell in the world grid."""
    def __init__(self, x, y, terrain_type=TerrainType.DEFAULT):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.obstacle = None

class World(Model):
    """Represents the game world."""
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, True)
        self.cells = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.initialize_world()

    def initialize_world(self):
        """Initialize the world with terrain and obstacles."""
        self.generate_terrain()
        self.place_obstacles()
        self.place_bonfires()

    def generate_terrain(self):
        """Generate terrain for the world."""
        for x in range(self.width):
            for y in range(self.height):
                terrain_type = np.random.choice(list(TerrainType), p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
                self.set_terrain(x, y, terrain_type)

    def place_obstacles(self):
        """Place obstacles in the world."""
        num_obstacles = int(self.width * self.height * 0.1)  # 10% of cells have obstacles
        for _ in range(num_obstacles):
            x, y = self.random.randrange(self.width), self.random.randrange(self.height)
            if not self.cells[x][y].obstacle:
                obstacle_type = np.random.choice(list(ObstacleType), p=[0.4, 0.3, 0.2, 0.1, 0])
                self.add_obstacle(x, y, obstacle_type)

    def place_bonfires(self):
        """Place bonfires in the world."""
        num_bonfires = max(1, int(self.width * self.height * 0.01))  # At least 1 bonfire, up to 1% of cells
        for _ in range(num_bonfires):
            x, y = self.random.randrange(self.width), self.random.randrange(self.height)
            if not self.cells[x][y].obstacle:
                self.add_obstacle(x, y, ObstacleType.BONFIRE)

    def add_obstacle(self, x, y, obstacle_type):
        """Adds an obstacle to the world."""
        self.cells[x][y].obstacle = obstacle_type

    def set_terrain(self, x, y, terrain_type):
        """Sets the terrain type for a cell."""
        self.cells[x][y].terrain_type = terrain_type

    def is_valid_move(self, x, y):
        """Check if a move to (x, y) is valid."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.cells[x][y].obstacle or self.cells[x][y].obstacle == ObstacleType.BONFIRE
        return False

    def get_path(self, start, end):
        """Finds a path between two points using A* algorithm."""
        # Implement A* algorithm here
        pass

    def apply_environmental_effect(self, agent):
        """Applies environmental effects to an agent."""
        x, y = agent.pos
        terrain = self.cells[x][y].terrain_type
        if terrain == TerrainType.LAVA:
            agent.take_damage(10)  # Lava deals 10 damage per step
        elif terrain == TerrainType.POISON_SWAMP:
            agent.apply_status_effect("poison")  # Apply poison effect
        elif terrain == TerrainType.WATER:
            agent.apply_status_effect("wet")  # Apply wet effect

    def get_distance(self, pos1, pos2):
        """Calculate the Manhattan distance between two positions."""
        if pos1 is None or pos2 is None:
            return float('inf')  # Return infinity if either position is None
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Add more environment-related classes and functions as needed