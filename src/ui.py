import pygame
from src.environment import TerrainType, ObstacleType
from src.agents import Player, Enemy, Neutral

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)

class SoulslikeUI:
    def __init__(self, model, width=800, height=600):
        self.model = model
        self.width = width
        self.height = height
        self.cell_size = min(width // model.grid.width, height // model.grid.height)

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Soulslike Simulator")
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.model.step()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_agents()

    def draw_grid(self):
        for x in range(self.model.grid.width):
            for y in range(self.model.grid.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                   self.cell_size, self.cell_size)
                cell = self.model.cells[x][y]
                color = self.get_cell_color(cell)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)  # Grid lines

    def get_cell_color(self, cell):
        if cell.obstacle is not None:
            return self.get_obstacle_color(cell.obstacle)
        return self.get_terrain_color(cell.terrain_type)

    def get_terrain_color(self, terrain_type):
        if terrain_type == TerrainType.GRASS:
            return GREEN
        elif terrain_type == TerrainType.STONE:
            return GRAY
        elif terrain_type == TerrainType.WATER:
            return BLUE
        elif terrain_type == TerrainType.LAVA:
            return RED
        elif terrain_type == TerrainType.POISON_SWAMP:
            return (0, 100, 0)  # Dark green
        return BLACK  # Default

    def get_obstacle_color(self, obstacle_type):
        if obstacle_type == ObstacleType.WALL:
            return GRAY
        elif obstacle_type == ObstacleType.TREE:
            return (0, 100, 0)  # Dark green
        elif obstacle_type == ObstacleType.ROCK:
            return (100, 100, 100)  # Light gray
        elif obstacle_type == ObstacleType.CHEST:
            return YELLOW
        elif obstacle_type == ObstacleType.BONFIRE:
            return (255, 69, 0)  # Orange-red
        return BROWN  # Default

    def draw_agents(self):
        for agent in self.model.schedule.agents:
            if agent.pos is None:
                continue  # Skip agents with invalid positions
            x, y = agent.pos
            center = ((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size)
            if isinstance(agent, Player):
                color = BLUE
            elif isinstance(agent, Enemy):
                color = RED
            elif isinstance(agent, Neutral):
                color = YELLOW
            else:
                color = WHITE
            pygame.draw.circle(self.screen, color, center, self.cell_size // 3)

            # Draw health bar
            health_percentage = agent.health / agent.max_health
            bar_width = self.cell_size * 0.8
            bar_height = self.cell_size * 0.1
            bar_pos = (center[0] - bar_width / 2, center[1] - self.cell_size / 2 - bar_height)
            pygame.draw.rect(self.screen, RED, (*bar_pos, bar_width, bar_height))
            pygame.draw.rect(self.screen, GREEN, (*bar_pos, bar_width * health_percentage, bar_height))