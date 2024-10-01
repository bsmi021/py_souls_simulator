from enum import Enum

class ItemType(Enum):
    WEAPON = 1
    ARMOR = 2
    CONSUMABLE = 3

class EquipmentSlot(Enum):
    MAIN_HAND = 1
    OFF_HAND = 2
    HEAD = 3
    CHEST = 4
    LEGS = 5
    FEET = 6

class Item:
    def __init__(self, name, item_type, weight, value):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.value = value

class Weapon(Item):
    def __init__(self, name, damage, attack_speed, weight, value):
        super().__init__(name, ItemType.WEAPON, weight, value)
        self.damage = damage
        self.attack_speed = attack_speed

class Armor(Item):
    def __init__(self, name, defense, slot, weight, value):
        super().__init__(name, ItemType.ARMOR, weight, value)
        self.defense = defense
        self.slot = slot

class Consumable(Item):
    def __init__(self, name, effect, weight, value):
        super().__init__(name, ItemType.CONSUMABLE, weight, value)
        self.effect = effect

    def use(self, agent):
        self.effect(agent)

class Inventory:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_weight(self):
        return sum(item.weight for item in self.items)

class Equipment:
    def __init__(self):
        self.slots = {slot: None for slot in EquipmentSlot}

    def equip(self, item, slot):
        if isinstance(item, Weapon) and slot in [EquipmentSlot.MAIN_HAND, EquipmentSlot.OFF_HAND]:
            self.slots[slot] = item
            return True
        elif isinstance(item, Armor) and item.slot == slot:
            self.slots[slot] = item
            return True
        return False

    def unequip(self, slot):
        item = self.slots[slot]
        self.slots[slot] = None
        return item

    def get_total_defense(self):
        return sum(item.defense for item in self.slots.values() if isinstance(item, Armor))

    def get_equipped_weapon(self):
        return self.slots[EquipmentSlot.MAIN_HAND]

# Example items
sword = Weapon("Iron Sword", damage=10, attack_speed=1.0, weight=5, value=50)
shield = Armor("Wooden Shield", defense=5, slot=EquipmentSlot.OFF_HAND, weight=3, value=30)
helmet = Armor("Leather Helmet", defense=3, slot=EquipmentSlot.HEAD, weight=2, value=25)
health_potion = Consumable("Health Potion", effect=lambda agent: setattr(agent, 'health', min(agent.health + 50, agent.max_health)), weight=0.5, value=20)

def create_basic_equipment():
    """Creates a set of basic equipment for new agents."""
    return {
        EquipmentSlot.MAIN_HAND: Weapon("Rusty Sword", damage=5, attack_speed=1.0, weight=4, value=10),
        EquipmentSlot.OFF_HAND: Armor("Worn Shield", defense=2, slot=EquipmentSlot.OFF_HAND, weight=3, value=5),
        EquipmentSlot.HEAD: Armor("Cloth Cap", defense=1, slot=EquipmentSlot.HEAD, weight=1, value=5),
        EquipmentSlot.CHEST: Armor("Tattered Shirt", defense=2, slot=EquipmentSlot.CHEST, weight=2, value=5),
        EquipmentSlot.LEGS: Armor("Worn Pants", defense=1, slot=EquipmentSlot.LEGS, weight=2, value=5),
        EquipmentSlot.FEET: Armor("Old Boots", defense=1, slot=EquipmentSlot.FEET, weight=2, value=5),
    }