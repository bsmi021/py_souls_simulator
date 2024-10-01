from mesa import Agent
from enum import Enum

class AgentType(Enum):
    PLAYER = 0
    ENEMY = 1
    NEUTRAL = 2

class StatusEffect(Enum):
    POISON = 0
    WET = 1
    BURNING = 2

class SoulslikeAgent(Agent):
    """Base class for all agents (players and NPCs)."""
    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.health = 100.0
        self.max_health = 100.0
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.poise = 50.0
        self.max_poise = 50.0
        self.strength = 10
        self.dexterity = 10
        self.vitality = 10
        self.endurance = 10
        self.level = 1
        self.experience = 0
        self.equipment = {}
        self.inventory = []
        self.status_effects = []

    def move(self, direction):
        """Moves the agent in the specified direction."""
        new_x = self.pos[0] + direction[0]
        new_y = self.pos[1] + direction[1]
        if self.model.is_valid_move(new_x, new_y):
            self.model.grid.move_agent(self, (new_x, new_y))
            self.model.apply_environmental_effect(self)

    def update_stats(self):
        """Updates the agent's stats based on equipment and level."""
        self.max_health = 100 + (self.vitality * 10)
        self.max_stamina = 100 + (self.endurance * 5)
        self.max_poise = 50 + (self.vitality * 2) + (self.strength * 1)

    def level_up(self):
        """Increases the agent's level and allows attribute allocation."""
        self.level += 1
        self.strength += 1
        self.dexterity += 1
        self.vitality += 1
        self.endurance += 1
        self.update_stats()

    def calculate_equip_load(self):
        """Calculates the current equipment load."""
        return sum(item.weight for item in self.equipment.values())

    def is_overencumbered(self):
        """Checks if the agent is overencumbered."""
        return self.calculate_equip_load() > self.max_equip_load()

    def apply_status_effect(self, effect):
        """Applies a status effect to the agent."""
        if effect not in self.status_effects:
            self.status_effects.append(effect)

    def update_status_effects(self):
        """Updates and removes expired status effects."""
        for effect in self.status_effects:
            if effect == StatusEffect.POISON:
                self.take_damage(5)  # Poison deals 5 damage per turn
            elif effect == StatusEffect.BURNING:
                self.take_damage(10)  # Burning deals 10 damage per turn

    def take_damage(self, amount):
        """Apply damage to the agent."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Handle agent death."""
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def max_equip_load(self):
        """Calculates the maximum equipment load."""
        return 40 + (self.endurance * 0.5)

    def step(self):
        """The agent's step function, called every tick."""
        self.update_status_effects()
        self.regenerate_stamina()

    def regenerate_stamina(self):
        """Regenerates stamina over time."""
        regen_rate = 5 + (self.endurance * 0.1)
        self.stamina = min(self.max_stamina, self.stamina + regen_rate)

class Player(SoulslikeAgent):
    """Represents the player character."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.PLAYER)

    def step(self):
        super().step()
        # Implement player-specific behavior here

class Enemy(SoulslikeAgent):
    """Represents hostile NPCs."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.ENEMY)

    def step(self):
        super().step()
        # Implement enemy AI behavior here

class Neutral(SoulslikeAgent):
    """Represents neutral or friendly NPCs."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.NEUTRAL)

    def step(self):
        super().step()
        # Implement neutral NPC behavior here

# Add more agent-related classes and functions as needed