from enum import Enum
import random
from src.item_system import Weapon, Armor

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
            weapon = attacker.equipment.get_equipped_weapon()
            if weapon is None:
                base_damage = attacker.strength  # Unarmed attack
            else:
                base_damage = weapon.damage

            damage = CombatSystem.calculate_damage(attacker, target, attack_type, base_damage)
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
        stamina_cost = CombatSystem.get_stamina_cost(attacker, attack_type)
        return attacker.stamina >= stamina_cost

    @staticmethod
    def get_stamina_cost(attacker, attack_type):
        """Returns the stamina cost for a given attack type."""
        weapon = attacker.equipment.get_equipped_weapon()
        base_cost = 20 if weapon is None else weapon.attack_speed * 15

        if attack_type == AttackType.LIGHT:
            return base_cost
        elif attack_type == AttackType.HEAVY:
            return base_cost * 1.5
        elif attack_type == AttackType.SKILL:
            return base_cost * 2

    @staticmethod
    def consume_stamina(attacker, attack_type):
        """Consumes stamina based on the attack type."""
        stamina_cost = CombatSystem.get_stamina_cost(attacker, attack_type)
        attacker.stamina = max(0, attacker.stamina - stamina_cost)

    @staticmethod
    def dodge(agent, direction):
        """Performs a dodge action."""
        dodge_cost = 20 - (agent.dexterity * 0.2)
        if agent.stamina >= dodge_cost:
            agent.stamina -= dodge_cost
            agent.apply_status_effect("invulnerable")  # Apply temporary invulnerability
            agent.move(direction)
            return True
        return False

    @staticmethod
    def parry(agent):
        """Performs a parry action."""
        parry_cost = 15 - (agent.dexterity * 0.1)
        if agent.stamina >= parry_cost:
            agent.stamina -= parry_cost
            agent.apply_status_effect("parrying")  # Apply parrying status
            return True
        return False

    @staticmethod
    def calculate_damage(attacker, target, attack_type, base_damage):
        """Calculates the damage dealt in an attack."""
        strength_bonus = attacker.strength * 0.5
        dexterity_bonus = attacker.dexterity * 0.3

        if attack_type == AttackType.LIGHT:
            damage = base_damage * 1.0 + strength_bonus + dexterity_bonus
        elif attack_type == AttackType.HEAVY:
            damage = base_damage * 1.5 + (strength_bonus * 1.5) + dexterity_bonus
        elif attack_type == AttackType.SKILL:
            damage = base_damage * 2.0 + strength_bonus + (dexterity_bonus * 1.5)

        if CombatSystem.calculate_critical_hit(attacker, target):
            damage *= 1.5

        defense = target.equipment.get_total_defense()
        final_damage = max(1, damage - defense)  # Ensure at least 1 damage is dealt
        return final_damage

    @staticmethod
    def calculate_poise_damage(attacker, attack_type):
        """Calculates the poise damage dealt by an attack."""
        weapon = attacker.equipment.get_equipped_weapon()
        base_poise_damage = attacker.strength + (weapon.damage if weapon else 0)
        
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