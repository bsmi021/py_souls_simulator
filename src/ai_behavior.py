from enum import Enum
import random
from src.combat_system import CombatSystem, AttackType

class AIState(Enum):
    IDLE = 1
    PATROL = 2
    CHASE = 3
    ATTACK = 4
    FLEE = 5

class AIController:
    @staticmethod
    def update(agent, world):
        """Updates the AI agent's behavior."""
        # Lazy import to avoid circular import issues.
        from src.agents import Enemy, Neutral  # Moved here to avoid circular import
        
        if isinstance(agent, Enemy):
            AIController.update_enemy(agent, world)
        elif isinstance(agent, Neutral):
            AIController.update_neutral(agent, world)

    @staticmethod
    def update_enemy(agent, world):
        """Updates the behavior of an enemy agent."""
        target = AIController.find_nearest_player(agent, world)
        
        if target:
            distance = world.get_distance(agent.pos, target.pos)
            
            if distance <= 1:  # Adjacent to target
                AIController.perform_attack(agent, target)
            elif distance <= agent.detection_range:
                AIController.chase(agent, target.pos, world)
            else:
                AIController.patrol(agent, world)
        else:
            AIController.patrol(agent, world)

    @staticmethod
    def update_neutral(agent, world):
        """Updates the behavior of a neutral agent."""
        AIController.wander(agent, world)

    @staticmethod
    def find_nearest_player(agent, world):
        """Finds the nearest player to the agent."""
        # Lazy import to avoid circular import issues.
        from src.agents import Player  # Only imported when actually needed

        players = [a for a in world.schedule.agents if isinstance(a, Player)]
        if players:
            return min(players, key=lambda p: world.get_distance(agent.pos, p.pos))
        return None

    @staticmethod
    def patrol(agent, world):
        """Makes the agent patrol in a random direction."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        direction = random.choice(directions)
        new_pos = (agent.pos[0] + direction[0], agent.pos[1] + direction[1])
        if world.is_valid_move(*new_pos):
            agent.move(direction)

    @staticmethod
    def chase(agent, target_pos, world):
        """Makes the agent move towards the target position."""
        path = world.get_path(agent.pos, target_pos)
        if path and len(path) > 1:
            next_pos = path[1]
            direction = (next_pos[0] - agent.pos[0], next_pos[1] - agent.pos[1])
            agent.move(direction)

    @staticmethod
    def wander(agent, world):
        """Makes the agent wander randomly."""
        AIController.patrol(agent, world)  # For now, wandering is the same as patrolling

    @staticmethod
    def perform_attack(agent, target):
        """Makes the agent perform an attack on the target."""
        attack_type = random.choice(list(AttackType))
        CombatSystem.attack(agent, target, attack_type)

    @staticmethod
    def flee(agent, threat, world):
        """Makes the agent flee from a threat."""
        opposite_direction = (
            agent.pos[0] - threat.pos[0],
            agent.pos[1] - threat.pos[1]
        )
        normalized_direction = (
            AIController.normalize(opposite_direction[0]),
            AIController.normalize(opposite_direction[1])
        )
        new_pos = (
            agent.pos[0] + normalized_direction[0],
            agent.pos[1] + normalized_direction[1]
        )
        if world.is_valid_move(*new_pos):
            agent.move(normalized_direction)

    @staticmethod
    def normalize(value):
        """Normalizes a value to -1, 0, or 1."""
        return 1 if value > 0 else -1 if value < 0 else 0

# Add more AI-related functions as needed
