from mesa import Agent
from enum import Enum
from src.combat_system import CombatSystem
from src.ai_behavior import AIController
from src.item_system import Inventory, Equipment, create_basic_equipment
from src.skills import get_skill

class AgentType(Enum):
    PLAYER = 0
    ENEMY = 1
    NEUTRAL = 2

class StatusEffect(Enum):
    POISON = 0
    WET = 1
    BURNING = 2
    STAGGERED = 3
    INVULNERABLE = 4
    PARRYING = 5

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
        self.inventory = Inventory(capacity=20)
        self.equipment = Equipment()
        self.equip_basic_gear()
        self.status_effects = []
        self.detection_range = 5
        self.skills = []

    def equip_basic_gear(self):
        """Equips the agent with basic starting gear."""
        for slot, item in create_basic_equipment().items():
            self.equipment.equip(item, slot)

    def learn_skill(self, skill_name):
        """Learns a new skill."""
        skill = get_skill(skill_name)
        if skill and skill not in self.skills:
            self.skills.append(skill)
            print(f"{self.unique_id} learned the skill: {skill.name}")

    def use_skill(self, skill_name, target=None):
        """Uses a skill."""
        skill = next((s for s in self.skills if s.name.lower() == skill_name.lower()), None)
        if skill:
            skill.use(self, target)
        else:
            print(f"{self.unique_id} doesn't know the skill: {skill_name}")

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
        return sum(item.weight for item in self.equipment.slots.values() if item is not None)

    def is_overencumbered(self):
        """Checks if the agent is overencumbered."""
        return self.calculate_equip_load() > self.max_equip_load()

    def apply_status_effect(self, effect):
        """Applies a status effect to the agent."""
        if effect not in self.status_effects:
            self.status_effects.append(effect)

    def update_status_effects(self):
        """Updates and removes expired status effects."""
        for effect in self.status_effects[:]:
            if effect == StatusEffect.POISON:
                self.take_damage(5)  # Poison deals 5 damage per turn
            elif effect == StatusEffect.BURNING:
                self.take_damage(10)  # Burning deals 10 damage per turn
            elif effect in [StatusEffect.STAGGERED, StatusEffect.INVULNERABLE, StatusEffect.PARRYING]:
                self.status_effects.remove(effect)  # These effects last only one turn

    def take_damage(self, amount):
        """Apply damage to the agent."""
        if StatusEffect.INVULNERABLE not in self.status_effects:
            defense = self.equipment.get_total_defense()
            damage_taken = max(1, amount - defense)  # Ensure at least 1 damage is taken
            self.health -= damage_taken
            if self.health <= 0:
                self.die()

    def die(self):
        """Handle agent death."""
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def max_equip_load(self):
        """Calculates the maximum equipment load."""
        return 40 + (self.endurance * 0.5)

    def update_skill_cooldowns(self):
        """Updates the cooldowns for all skills."""
        for skill in self.skills:
            skill.update_cooldown()

    def step(self):
        """The agent's step function, called every tick."""
        self.update_status_effects()
        self.update_skill_cooldowns()
        CombatSystem.regenerate_stamina(self, 1)  # Assuming 1 second per tick

class Player(SoulslikeAgent):
    """Represents the player character."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.PLAYER)
        self.learn_skill("fireball")
        self.learn_skill("healing_light")
        self.learn_skill("quick_step")

    def step(self):
        super().step()
        # Player behavior is controlled by user input, so we don't need AI here

class Enemy(SoulslikeAgent):
    """Represents hostile NPCs."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.ENEMY)
        self.learn_skill("fireball")  # Enemies can use skills too

    def step(self):
        super().step()
        AIController.update(self, self.model)

class Neutral(SoulslikeAgent):
    """Represents neutral or friendly NPCs."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, AgentType.NEUTRAL)
        self.learn_skill("healing_light")  # Neutral NPCs might have healing abilities

    def step(self):
        super().step()
        AIController.update(self, self.model)

def create_agent(agent_type, unique_id, model):
    """Factory function to create agents of different types."""
    if agent_type == AgentType.PLAYER:
        return Player(unique_id, model)
    elif agent_type == AgentType.ENEMY:
        return Enemy(unique_id, model)
    elif agent_type == AgentType.NEUTRAL:
        return Neutral(unique_id, model)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")