# combat.py
import random
from character import Character

class Combat:
    def __init__(self, player: Character, enemy: Character):
        self.player = player
        self.enemy = enemy
        self.log = []
        self.turn_count = 0
        self.player_defended = False

    def player_attack(self):
        """Player attacks - 90% hit rate"""
        hit_chance = random.randint(1, 100)
        
        if hit_chance > 10:  # 90% success
            dmg = self.player.basic_attack(self.enemy)
            
            # Enemy reactions on successful hit
            reactions = {
                "Bandit": ["💢 You no fit kill me!", "🤬 You dey try me!"],
                "Kidnapper": ["😤 I no fit die!", "🔥 I go move your family!"],
                "Politician": ["🎭 You are a fool!", "💼 I belong to the people!"]
            }
            reaction = random.choice(reactions.get(self.enemy.name, ["😡 Arrgh!"]))
            msg = f"✅ You attacked! +{dmg}xp damage dealt!\n{reaction}"
        else:  # Miss - player takes minor damage
            self.player.take_damage(2)
            
            fail_reactions = {
                "Bandit": ["😆 Odeshi! You missed!", "🤣 Miss tire!"],
                "Kidnapper": ["😂 I go move your family!", "💀 Slow motion attack!"],
                "Politician": ["🎪 I belong to the people!", "🎯 Miss!"]
            }
            reaction = random.choice(fail_reactions.get(self.enemy.name, ["😂 You missed!"]))
            msg = f"❌ Attack FAILED! -2xp HP\n{reaction}"
        
        self.log.append(msg)
        self.turn_count += 1
        return msg

    def player_defend(self):
        """Player defends - 90% success rate"""
        defend_chance = random.randint(1, 100)
        
        if defend_chance > 10:  # 90% success
            self.player_defended = True
            
            defense_reactions = {
                "Bandit": ["🛡️ You no wan die abi?", "😤 Sharp boy!"],
                "Kidnapper": ["🙅 You go still die", "⚡ But I go find you!"],
                "Politician": ["🎭 It is better you fall now", "💼 This won't save you!"]
            }
            reaction = random.choice(defense_reactions.get(self.enemy.name, ["😠 Hmph!"]))
            msg = f"🛡️ DEFENSE SUCCESSFUL! You blocked the attack!\n{reaction}"
        else:  # Failed defense
            self.player.take_damage(5)
            
            fail_def_reactions = {
                "Bandit": ["😱 Wallahi, I go kill you!!", "💥 See as you scatter!"],
                "Kidnapper": ["😈 How much ransom dem go pay for you", "🔗 You go see pepper!"],
                "Politician": ["🎯 Na me dey here", "💀 Power overwhelms you!"]
            }
            reaction = random.choice(fail_def_reactions.get(self.enemy.name, ["💥 Boom!"]))
            msg = f"❌ DEFENSE FAILED! -5xp HP\n{reaction}"
        
        self.log.append(msg)
        self.turn_count += 1
        return msg

    def player_special_attack(self):
        """Player uses special ability - guaranteed hit"""
        ability_name, damage = self.player.use_special_attack(self.enemy)
        msg = f"⚡ SPECIAL ABILITY: {ability_name}!\n💥 {damage}xp damage dealt! (GUARANTEED HIT)"
        self.log.append(msg)
        self.turn_count += 1
        return msg

    def enemy_turn(self):
        """Enemy attacks player"""
        if self.player_defended:
            # Reduced damage if player defended
            damage = random.randint(1, 2)
            self.player_defended = False
        else:
            # Normal damage
            damage = random.randint(2, 6)
        
        self.player.take_damage(damage)
        msg = f"🔥 {self.enemy.name} counter-attacks for {damage}xp damage!"
        self.log.append(msg)
        return msg

    def is_over(self):
        if not self.player.is_alive():
            return True, "enemy"
        if not self.enemy.is_alive():
            return True, "player"
        return False, None

    def reward_xp_for_enemy(self):
        # XP reward based on enemy level
        base_xp = self.enemy.level * 25
        bonus = random.randint(5, 15)
        return base_xp + bonus