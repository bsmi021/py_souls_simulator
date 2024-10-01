from enum import Enum
from src.combat_system import CombatSystem, DamageType

class SkillType(Enum):
    OFFENSIVE = 1
    DEFENSIVE = 2
    UTILITY = 3

class Skill:
    def __init__(self, name, description, skill_type, stamina_cost, cooldown):
        self.name = name
        self.description = description
        self.skill_type = skill_type
        self.stamina_cost = stamina_cost
        self.cooldown = cooldown

    def can_use(self, agent):
        return agent.stamina >= self.stamina_cost and agent.skill_cooldowns[self.name] == 0

    def use(self, agent, target=None):
        if self.can_use(agent):
            agent.stamina -= self.stamina_cost
            self.effect(agent, target)
        else:
            print(f"{agent.unique_id} cannot use {self.name} at this time.")

    def effect(self, agent, target):
        pass  # To be implemented by subclasses

class FireballSkill(Skill):
    def __init__(self):
        super().__init__("Fireball", "Launches a ball of fire at the target", SkillType.OFFENSIVE, 30, 3)

    def effect(self, agent, target):
        if target:
            damage = 20 + (agent.strength * 0.5)
            target.take_damage(damage)
            target.apply_status_effect("burning")
            print(f"{agent.unique_id} cast Fireball on {target.unique_id} for {damage} damage!")

class HealingLightSkill(Skill):
    def __init__(self):
        super().__init__("Healing Light", "Restores some health to the user", SkillType.DEFENSIVE, 25, 5)

    def effect(self, agent, target):
        heal_amount = 30 + (agent.vitality * 0.5)
        agent.health = min(agent.max_health, agent.health + heal_amount)
        print(f"{agent.unique_id} used Healing Light and restored {heal_amount} health!")

class QuickStepSkill(Skill):
    def __init__(self):
        super().__init__("Quick Step", "Performs a quick dodge in any direction", SkillType.UTILITY, 15, 1)

    def effect(self, agent, target):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            if CombatSystem.dodge(agent, direction):
                print(f"{agent.unique_id} performed a Quick Step!")
                break

# Add more skills as needed

skill_catalog = {
    "fireball": FireballSkill(),
    "healing_light": HealingLightSkill(),
    "quick_step": QuickStepSkill(),
}

def get_skill(skill_name):
    return skill_catalog.get(skill_name.lower())