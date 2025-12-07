# save_system.py
import sqlite3
import json
from character import Character
from datetime import datetime
import time

class SaveSystem:
    def __init__(self, db_name='nigerian_rpg.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_database()
        self.settings = self.load_settings()
    
    def init_database(self):
        """Initialize database tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                char_class TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                hp INTEGER,
                max_hp INTEGER,
                attack INTEGER,
                defense INTEGER,
                weapon TEXT,
                xp INTEGER DEFAULT 0,
                xp_to_next INTEGER DEFAULT 50,
                current_level INTEGER DEFAULT 1,
                damage_dealt INTEGER DEFAULT 0,
                sprite_path TEXT,
                skills TEXT,
                last_saved DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS combat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                enemy_name TEXT,
                level INTEGER,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # NEW: Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                sound_enabled INTEGER DEFAULT 1,
                music_enabled INTEGER DEFAULT 1,
                screen_effects INTEGER DEFAULT 1,
                difficulty TEXT DEFAULT 'Normal'
            )
        ''')
        
        # NEW: Leaderboard table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                completion_time REAL,
                total_damage INTEGER,
                enemies_defeated INTEGER,
                run_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                difficulty TEXT DEFAULT 'Normal'
            )
        ''')
        
        # Initialize default settings if not exists
        self.cursor.execute('SELECT id FROM settings WHERE id = 1')
        if not self.cursor.fetchone():
            self.cursor.execute('''
                INSERT INTO settings (id, sound_enabled, music_enabled, screen_effects, difficulty)
                VALUES (1, 1, 1, 1, 'Normal')
            ''')
        
        self.conn.commit()
    
    def save_character(self, player: Character, current_level: int):
        """Save or update character"""
        self.cursor.execute('SELECT id FROM characters WHERE name = ?', (player.name,))
        existing = self.cursor.fetchone()
        
        skills_json = json.dumps(player.skills)
        
        if existing:
            self.cursor.execute('''
                UPDATE characters 
                SET char_class=?, level=?, hp=?, max_hp=?, attack=?, defense=?,
                    weapon=?, xp=?, xp_to_next=?, current_level=?, damage_dealt=?,
                    sprite_path=?, skills=?, last_saved=?
                WHERE name=?
            ''', (player.char_class, player.level, player.hp, player.max_hp,
                  player.attack, player.defense, player.weapon, player.xp,
                  player.xp_to_next, current_level, player.damage_dealt,
                  player.sprite_path, skills_json, datetime.now(), player.name))
        else:
            self.cursor.execute('''
                INSERT INTO characters 
                (name, char_class, level, hp, max_hp, attack, defense, weapon,
                 xp, xp_to_next, current_level, damage_dealt, sprite_path, skills)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player.name, player.char_class, player.level, player.hp,
                  player.max_hp, player.attack, player.defense, player.weapon,
                  player.xp, player.xp_to_next, current_level, player.damage_dealt,
                  player.sprite_path, skills_json))
        
        self.conn.commit()
        return True
    
    def load_character(self, name: str) -> tuple:
        """Load character by name - returns (Character, current_level)"""
        self.cursor.execute('SELECT * FROM characters WHERE name = ?', (name,))
        char = self.cursor.fetchone()
        
        if not char:
            return None, None
        
        _, name, char_class, level, hp, max_hp, attack, defense, weapon, xp, xp_to_next, current_level, damage_dealt, sprite_path, skills_json, _ = char
        
        skills = json.loads(skills_json) if skills_json else {}
        
        player = Character(
            name=name,
            level=level,
            hp=hp,
            max_hp=max_hp,
            attack=attack,
            defense=defense,
            char_class=char_class,
            weapon=weapon,
            xp=xp,
            xp_to_next=xp_to_next,
            sprite_path=sprite_path,
            skills=skills,
            damage_dealt=damage_dealt
        )
        
        return player, current_level
    
    def get_all_saves(self) -> list:
        """Get all saved characters"""
        self.cursor.execute('''
            SELECT name, char_class, level, weapon, current_level, last_saved 
            FROM characters 
            ORDER BY last_saved DESC 
            LIMIT 10
        ''')
        return self.cursor.fetchall()
    
    def save_combat_result(self, player_name: str, enemy_name: str, level: int, result: str):
        """Save combat history"""
        self.cursor.execute('''
            INSERT INTO combat_history (player_name, enemy_name, level, result)
            VALUES (?, ?, ?, ?)
        ''', (player_name, enemy_name, level, result))
        self.conn.commit()
    
    def get_combat_history(self, player_name: str, limit: int = 10) -> list:
        """Get combat history for player"""
        self.cursor.execute('''
            SELECT enemy_name, level, result, timestamp 
            FROM combat_history 
            WHERE player_name = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (player_name, limit))
        return self.cursor.fetchall()
    
    def delete_save(self, name: str):
        """Delete a save file"""
        self.cursor.execute('DELETE FROM characters WHERE name = ?', (name,))
        self.cursor.execute('DELETE FROM combat_history WHERE player_name = ?', (name,))
        self.conn.commit()
    
    # ============================================
    # NEW: SETTINGS METHODS
    # ============================================
    
    def load_settings(self) -> dict:
        """Load game settings"""
        self.cursor.execute('SELECT * FROM settings WHERE id = 1')
        row = self.cursor.fetchone()
        if row:
            return {
                'sound_enabled': bool(row[1]),
                'music_enabled': bool(row[2]),
                'screen_effects': bool(row[3]),
                'difficulty': row[4]
            }
        return {
            'sound_enabled': True,
            'music_enabled': True,
            'screen_effects': True,
            'difficulty': 'Normal'
        }
    
    def save_settings(self, settings: dict):
        """Save game settings"""
        self.cursor.execute('''
            UPDATE settings 
            SET sound_enabled=?, music_enabled=?, screen_effects=?, difficulty=?
            WHERE id=1
        ''', (int(settings['sound_enabled']), 
              int(settings['music_enabled']),
              int(settings['screen_effects']),
              settings['difficulty']))
        self.conn.commit()
        self.settings = settings
    
    def get_setting(self, key: str):
        """Get specific setting value"""
        return self.settings.get(key)
    
    def toggle_setting(self, key: str):
        """Toggle a boolean setting"""
        if key in self.settings and isinstance(self.settings[key], bool):
            self.settings[key] = not self.settings[key]
            self.save_settings(self.settings)
            return self.settings[key]
        return None
    
    # ============================================
    # NEW: LEADERBOARD METHODS
    # ============================================
    
    def save_to_leaderboard(self, player_name: str, completion_time: float, 
                           total_damage: int, enemies_defeated: int):
        """Save a completed run to leaderboard"""
        difficulty = self.settings.get('difficulty', 'Normal')
        self.cursor.execute('''
            INSERT INTO leaderboard 
            (player_name, completion_time, total_damage, enemies_defeated, difficulty)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_name, completion_time, total_damage, enemies_defeated, difficulty))
        self.conn.commit()
    
    def get_leaderboard_fastest(self, limit: int = 10) -> list:
        """Get top fastest completion times"""
        self.cursor.execute('''
            SELECT player_name, completion_time, enemies_defeated, difficulty, run_date
            FROM leaderboard 
            ORDER BY completion_time ASC 
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_leaderboard_damage(self, limit: int = 10) -> list:
        """Get top damage dealers"""
        self.cursor.execute('''
            SELECT player_name, total_damage, completion_time, difficulty, run_date
            FROM leaderboard 
            ORDER BY total_damage DESC 
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_leaderboard_enemies(self, limit: int = 10) -> list:
        """Get most enemies defeated"""
        self.cursor.execute('''
            SELECT player_name, enemies_defeated, completion_time, difficulty, run_date
            FROM leaderboard 
            ORDER BY enemies_defeated DESC 
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_player_best_time(self, player_name: str) -> float:
        """Get player's best completion time"""
        self.cursor.execute('''
            SELECT MIN(completion_time) FROM leaderboard WHERE player_name = ?
        ''', (player_name,))
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else float('inf')
    
    def close(self):
        """Close database connection"""
        self.conn.close()
