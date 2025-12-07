#This whole file explains the Character class and its methods for an RPG game.
# character.py
from dataclasses import dataclass, field
import random
# attribute based initialization
@dataclass
class Character:
    name: str
    level: int
    hp: int
    max_hp: int
    attack: int
    defense: int
    char_class: str = "Citizen"  # Citizen, Soldier, Police
    weapon: str = "Cutlass"  # Juju, Cutlass, Gun
    xp: int = 0
    xp_to_next: int = 50
    sprite_path: str = None
    skills: dict = field(default_factory=dict)
    damage_dealt: int = 0
    
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, dmg: int):
        self.hp = max(0, self.hp - int(dmg))

    def heal(self, amt: int):
        self.hp = min(self.max_hp, self.hp + int(amt))

    def basic_attack(self, target: "Character") -> int:
        """Basic attack with weapon damage"""
        roll = random.randint(1, 6)
        weapon_dmg = self.get_weapon_damage()
        base = max(1, weapon_dmg + roll - target.defense)
        target.take_damage(base)
        self.damage_dealt += base
        return base

    def get_weapon_damage(self) -> int:
        """Get weapon base damage"""
        weapon_damages = {
            "Juju": 5,
            "Cutlass": 2,
            "Gun": 10
        }
        return weapon_damages.get(self.weapon, 2)

    def get_special_threshold(self) -> int:
        """Damage threshold for special ability"""
        thresholds = {
            "Juju": 25,
            "Cutlass": 10,
            "Gun": 50
        }
        return thresholds.get(self.weapon, 30)

    def get_special_abilities(self) -> list:
        """Get list of special abilities for weapon"""
        specials = {
            "Cutlass": ["BENIN RAMPAGE", "LAGOS ATTACK", "BARAWO BARAGE"],
            "Juju": ["OGUN STRIKE", "SANGO FATAL", "AMADIOHA SPAWN"],
            "Gun": ["BARRAGE", "AK47 FIESTA", "MK 419 BARRAGE"]
        }
        return specials.get(self.weapon, ["BASIC STRIKE"])

    def use_skill(self, skill_name: str, target: "Character"):
        """Returns (description_str, effect_value)"""
        if skill_name not in self.skills:
            return f"{self.name} tried to use {skill_name} but doesn't know it.", 0

        skill = self.skills[skill_name]
        typ = skill.get("type", "damage")
        power = skill.get("power", 0)

        if typ == "damage":
            dmg = max(1, int(self.attack * skill.get("mult", 1.0) + power - target.defense))
            target.take_damage(dmg)
            self.damage_dealt += dmg
            return f"{self.name} used {skill_name} for {dmg} damage!", dmg
        elif typ == "heal":
            heal_amt = int(power + self.level * skill.get("scale", 0))
            self.heal(heal_amt)
            return f"{self.name} used {skill_name} and healed {heal_amt} HP!", heal_amt
        else:
            return f"{self.name} used {skill_name} but nothing happened.", 0

    def use_special_attack(self, target: "Character") -> tuple:
        """Use random special ability - guaranteed hit with 2x damage"""
        ability_name = random.choice(self.get_special_abilities())
        damage = self.get_weapon_damage() * 2
        target.take_damage(damage)
        self.damage_dealt += damage
        return ability_name, damage

    def gain_xp(self, amount: int):
        self.xp += int(amount)
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()
            leveled = True
        return leveled

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack += 1
        self.defense += 1
        self.hp = self.max_hp
        self.xp_to_next = int(self.xp_to_next * 1.3)