class Skill:
    def __init__(self, name, description, requirements):
        self.name = name
        self.description = description
        self.requirements = requirements

class SkillTree:
    def __init__(self):
        self.skills = {}

    def add_skill(self, skill):
        self.skills[skill.name] = skill

class ProgressionManager:
    @staticmethod
    def gain_experience(agent, amount):
        """Adds experience points to the agent."""
        agent.experience += amount
        if ProgressionManager.check_level_up(agent):
            ProgressionManager.level_up(agent)

    @staticmethod
    def check_level_up(agent):
        """Checks if the agent has enough XP to level up."""
        return agent.experience >= agent.level * 100

    @staticmethod
    def level_up(agent):
        """Increases the agent's level and allows attribute allocation."""
        agent.level += 1
        agent.experience -= (agent.level - 1) * 100
        # Implement attribute allocation logic here

    @staticmethod
    def allocate_attribute_point(agent, attribute):
        """Allocates a point to the specified attribute."""