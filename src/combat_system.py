from enum import Enum
import random

class AttackType(Enum):
    LIGHT = 1
    HEAVY = 2
    SKILL = 3

class DamageType(Enum):
    PHYSICAL = 1
    FIRE = 2
    LIGHTNING = 3

class CombatSystem:
    @staticmethod
    def attack(attacker, target, attack_type):
        """Performs an attack action."""
        if CombatSystem.can_perform_attack(attacker, attack_type):
            damage = CombatSystem.calculate_damage(attacker, target, attack_type)
            poise_damage = CombatSystem.calculate_poise_damage(attacker, attack_type)
            
            if not CombatSystem.is_attack_dodged(target):
                if CombatSystem.is_attack_parried(target):
                    attacker.take_damage(damage)  # Riposte
                    CombatSystem.apply_poise_damage(attacker, poise_damage)
                else:
                    target.take_damage(damage)
                    CombatSystem.apply_poise_damage(target, poise_damage)
            
            CombatSystem.consume_stamina(attacker, attack_type)

    @staticmethod
    def can_perform_attack(attacker, attack_type):
        """Checks if the attacker has enough stamina to perform the attack."""
        stamina_cost = CombatSystem.get_stamina_cost(attack_type)
        return attacker.stamina >= stamina_cost

    @staticmethod
    def get_stamina_cost(attack_type):
        """Returns the stamina cost for a given attack type."""
        if attack_type == AttackType.LIGHT:
            return 20
        elif attack_type == AttackType.HEAVY:
            return 35
        elif attack_type == AttackType.SKILL:
            return 50

    @staticmethod
    def consume_stamina(attacker, attack_type):
        """Consumes stamina based on the attack type."""
        stamina_cost = CombatSystem.get_stamina_cost(attack_type)
        attacker.stamina = max(0, attacker.stamina - stamina_cost)

    @staticmethod
    def dodge(agent, direction):
        """Performs a dodge action."""
        if agent.stamina >= 20:
            agent.stamina -= 20
            agent.apply_status_effect("invulnerable")  # Apply temporary invulnerability
            agent.move(direction)
            return True
        return False

    @staticmethod
    def parry(agent):
        """Performs a parry action."""
        if agent.stamina >= 15:
            agent.stamina -= 15
            agent.apply_status_effect("parrying")  # Apply parrying status
            return True
        return False

    @staticmethod
    def calculate_damage(attacker, target, attack_type):
        """Calculates the damage dealt in an attack."""
        base_damage = attacker.strength * 2
        if attack_type == AttackType.LIGHT:
            damage = base_damage * 1.0
        elif attack_type == AttackType.HEAVY:
            damage = base_damage * 1.5
        elif attack_type == AttackType.SKILL:
            damage = base_damage * 2.0

        if CombatSystem.calculate_critical_hit(attacker, target):
            damage *= 1.5

        damage_reduction = target.vitality * 0.5
        final_damage = max(1, damage - damage_reduction)
        return final_damage

    @staticmethod
    def calculate_poise_damage(attacker, attack_type):
        """Calculates the poise damage dealt by an attack."""
        base_poise_damage = attacker.strength
        if attack_type == AttackType.LIGHT:
            return base_poise_damage * 1.0
        elif attack_type == AttackType.HEAVY:
            return base_poise_damage * 1.5
        elif attack_type == AttackType.SKILL:
            return base_poise_damage * 2.0

    @staticmethod
    def apply_poise_damage(target, poise_damage):
        """Applies poise damage and checks for stagger."""
        target.poise -= poise_damage
        if target.poise <= 0:
            target.apply_status_effect("staggered")
            target.poise = target.max_poise  # Reset poise after stagger

    @staticmethod
    def is_attack_dodged(target):
        """Determines if an attack is dodged."""
        dodge_chance = min(70, 30 + (target.dexterity * 0.5))
        return random.random() < dodge_chance / 100

    @staticmethod
    def is_attack_parried(target):
        """Determines if an attack is parried."""
        return "parrying" in target.status_effects

    @staticmethod
    def regenerate_stamina(agent, delta_time):
        """Regenerates stamina over time."""
        regen_rate = (5 + (agent.endurance * 0.1)) * delta_time
        agent.stamina = min(agent.max_stamina, agent.stamina + regen_rate)

    @staticmethod
    def calculate_critical_hit(attacker, target):
        """Determines if an attack is a critical hit."""
        crit_chance = 5 + (attacker.dexterity * 0.2)
        return random.random() < crit_chance / 100

    @staticmethod
    def apply_status_effect(attacker, target, effect):
        """Applies status effects from weapons or skills."""
        target.apply_status_effect(effect)

# Add more combat-related functions as needed