# -*- coding: utf-8 -*-
"""
Battle GUI for Nigerian RPG - Enhanced with Damage & Victory Animations
"""
import pygame
import sys
import os
import random
import time
from character import Character
from combat import Combat
from save_system import SaveSystem
from resources import asset_manager, play_level_music

# Config
WIDTH, HEIGHT = 960, 600
FPS = 30
ASSETS_DIR = "assets"
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")

# Animation timings (in milliseconds)
DAMAGE_ANIMATION_DURATION = 300  # Show damage sprite for 300ms
VICTORY_ANIMATION_DURATION = 2000  # Show victory sprite for 2 seconds

# Helper: load image or None
def load_image(name, scale=1.0):
    """Load image with error handling"""
    if not name:
        return None
    path = os.path.join(SPRITES_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale != 1.0:
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
        return img
    except Exception as e:
        print(f"⚠️ Could not load image {name}: {e}")
        return None

def load_character_sprites(sprite_path, scale=1.0):
    """Load all sprite variants for a character (normal, damage, victory)"""
    sprites = {}
    
    if not sprite_path:
        return sprites
    
    # Extract base name without extension
    base_name = sprite_path.rsplit('.', 1)[0]
    
    # Load normal sprite
    sprites['normal'] = load_image(sprite_path, scale)
    
    # Load damage sprite
    damage_name = f"{base_name}_damage.png"
    sprites['damage'] = load_image(damage_name, scale)
    
    # Load victory sprite (optional)
    victory_name = f"{base_name}_victory.png"
    sprites['victory'] = load_image(victory_name, scale)
    
    return sprites

# Helper: load sound (optional)
def load_sound(name):
    """Load sound with error handling"""
    if not name:
        return None
    path = os.path.join(AUDIO_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠️ Could not load sound {name}: {e}")
        return None

# UI helpers
def draw_text(screen, text, x, y, font, color=(255,255,255)):
    """Draw text with error handling"""
    try:
        surf = font.render(str(text), True, color)
        screen.blit(surf, (x, y))
    except Exception as e:
        print(f"⚠️ Error drawing text: {e}")

def draw_hp_bar(screen, x, y, current, maximum, w=250, h=20):
    """Draw HP bar"""
    try:
        ratio = max(0, current) / max(1, maximum)
        pygame.draw.rect(screen, (120, 10, 10), (x, y, w, h))
        pygame.draw.rect(screen, (20, 200, 20), (x, y, int(w*ratio), h))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), 2)
    except Exception as e:
        print(f"⚠️ Error drawing HP bar: {e}")

# Nigerian-themed enemies with difficulty scaling
LEVEL_1_ENEMIES = [
    {"name":"Bandit", "level":1, "hp":100, "atk":4, "def":2, "sprite":"bandit.png"},
    {"name":"Area Boy", "level":1, "hp":90, "atk":5, "def":1, "sprite":"bandit.png"},
]

LEVEL_2_ENEMIES = [
    {"name":"Kidnapper", "level":2, "hp":150, "atk":6, "def":3, "sprite":"kidnapper.png"},
    {"name":"Armed Robber", "level":2, "hp":140, "atk":7, "def":2, "sprite":"kidnapper.png"},
]

LEVEL_3_ENEMIES = [
    {"name":"Politician", "level":3, "hp":200, "atk":8, "def":4, "sprite":"politician.png"},
]

# Preload optional sounds
SOUND_ATTACK = None
SOUND_HEAL = None
SOUND_WIN = None
SOUND_LOSE = None

def create_enemy_for_level(level: int, difficulty_multiplier: float = 1.0):
    """Create enemy based on current level with difficulty scaling"""
    try:
        if level == 1:
            base = random.choice(LEVEL_1_ENEMIES)
        elif level == 2:
            base = random.choice(LEVEL_2_ENEMIES)
        else:  # Level 3
            base = random.choice(LEVEL_3_ENEMIES)
        
        # Apply difficulty multiplier to HP
        scaled_hp = int(base["hp"] * difficulty_multiplier)
        
        e = Character(
            name=base["name"],
            level=base["level"],
            hp=scaled_hp,
            max_hp=scaled_hp,
            attack=base["atk"],
            defense=base["def"],
            sprite_path=base.get("sprite")
        )
        return e
    except Exception as e:
        print(f"❌ Error creating enemy: {e}")
        return Character(name="Enemy", level=1, hp=100, max_hp=100, attack=5, defense=2)

# Main GUI runner
def run_battle_gui_with_player(player: Character, save_system: SaveSystem, current_level: int = 1):
    """Main battle GUI loop with animations"""
    global SOUND_ATTACK, SOUND_HEAL, SOUND_WIN, SOUND_LOSE
    
    try:
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("⚔️ Escape the Streets of Nigeria")
        clock = pygame.time.Clock()
        
        # Font loading with fallback
        try:
            font = pygame.font.SysFont("Arial", 22)
            bigfont = pygame.font.SysFont("Arial", 32)
        except:
            print("⚠️ Using default font")
            font = pygame.font.Font(None, 22)
            bigfont = pygame.font.Font(None, 32)

        # Load settings
        settings = save_system.load_settings()
        
        # Get difficulty multiplier
        difficulty_multipliers = {"Easy": 0.75, "Normal": 1.0, "Hard": 1.5}
        difficulty_mult = difficulty_multipliers.get(settings['difficulty'], 1.0)

        # Load optional audio (respect settings)
        if settings['sound_enabled']:
            SOUND_ATTACK = load_sound("attack.wav")
            SOUND_HEAL = load_sound("heal.wav")
            SOUND_WIN = load_sound("victory.wav")
            SOUND_LOSE = load_sound("defeat.wav")

        # Leaderboard tracking
        run_start_time = time.time()
        total_damage_dealt = 0
        enemies_defeated = 0

        # Game state
        game_level = current_level
        enemy = create_enemy_for_level(game_level, difficulty_mult)
        combat = Combat(player, enemy)
        message = get_level_intro(game_level, enemy)
        weapon_damage_count = 0
        special_ability_count = 0

        # Load ALL sprite variants for player and enemy
        player_sprites = load_character_sprites(player.sprite_path, scale=0.7)
        enemy_sprites = load_character_sprites(enemy.sprite_path, scale=0.8)
        
        # Animation state tracking
        player_animation_state = 'normal'  # 'normal', 'damage', 'victory'
        enemy_animation_state = 'normal'
        player_animation_timer = 0
        enemy_animation_timer = 0
        
        # Load background for current level
        try:
            background_img = asset_manager.get_background(game_level)
        except:
            background_img = None
        
        # Play level music (respect settings)
        if settings['music_enabled']:
            try:
                play_level_music(game_level)
            except:
                pass

        # Buttons
        attack_btn = pygame.Rect(50, 480, 160, 56)
        defend_btn = pygame.Rect(230, 480, 160, 56)
        special_btn = pygame.Rect(410, 480, 160, 56)
        flee_btn = pygame.Rect(590, 480, 160, 56)
        pause_btn = pygame.Rect(880, 10, 60, 30)

        # Auto-save timer
        last_save_time = pygame.time.get_ticks()
        SAVE_INTERVAL = 30000  # Auto-save every 30 seconds
        
        paused = False

        running = True
        while running:
            dt = clock.tick(FPS)
            current_time = pygame.time.get_ticks()
            
            # Update animation timers
            if player_animation_timer > 0 and current_time >= player_animation_timer:
                player_animation_state = 'normal'
                player_animation_timer = 0
            
            if enemy_animation_timer > 0 and current_time >= enemy_animation_timer:
                enemy_animation_state = 'normal'
                enemy_animation_timer = 0
            
            # Auto-save
            if current_time - last_save_time > SAVE_INTERVAL:
                save_system.save_character(player, game_level)
                last_save_time = current_time
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    save_system.save_character(player, game_level)
                    try:
                        asset_manager.stop_music()
                    except:
                        pass
                    running = False
                    return
                
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE or ev.key == pygame.K_p:
                        paused = not paused

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    
                    # Pause button
                    if pause_btn.collidepoint(mx, my):
                        paused = not paused
                    
                    if paused:
                        continue
                    
                    # Attack
                    if attack_btn.collidepoint(mx, my):
                        msg = combat.player_attack()
                        damage = player.get_weapon_damage()
                        weapon_damage_count += damage
                        total_damage_dealt += damage
                        
                        # Trigger ENEMY damage animation
                        enemy_animation_state = 'damage'
                        enemy_animation_timer = current_time + DAMAGE_ANIMATION_DURATION
                        
                        if SOUND_ATTACK and settings['sound_enabled']: 
                            SOUND_ATTACK.play()
                        message = msg
                        
                        over, winner = combat.is_over()
                        if not over:
                            pygame.time.set_timer(pygame.USEREVENT+1, 500, loops=1)
                        else:
                            if winner == "player":
                                enemies_defeated += 1
                                
                                # Show PLAYER victory animation
                                player_animation_state = 'victory'
                                player_animation_timer = current_time + VICTORY_ANIMATION_DURATION
                                
                                handle_victory(player, enemy, combat, save_system, game_level)
                                
                                if game_level >= 3:
                                    # GAME COMPLETED
                                    completion_time = time.time() - run_start_time
                                    save_system.save_to_leaderboard(
                                        player.name, 
                                        completion_time, 
                                        total_damage_dealt, 
                                        enemies_defeated
                                    )
                                    
                                    message = f"🎉 GAME FINISHED! You escaped!\nTime: {int(completion_time//60)}m {int(completion_time%60)}s"
                                    if SOUND_WIN and settings['sound_enabled']: 
                                        SOUND_WIN.play()
                                    
                                    pygame.time.wait(VICTORY_ANIMATION_DURATION)
                                    
                                    show_victory_screen(screen, player, completion_time, 
                                                       total_damage_dealt, enemies_defeated, 
                                                       settings['difficulty'], font, bigfont)
                                    
                                    save_system.save_character(player, 1)
                                    try:
                                        asset_manager.stop_music(fade_ms=1000)
                                    except:
                                        pass
                                    running = False
                                else:
                                    # Wait for victory animation to complete
                                    pygame.time.wait(VICTORY_ANIMATION_DURATION)
                                    
                                    game_level += 1
                                    weapon_damage_count = 0
                                    special_ability_count = 0
                                    enemy = create_enemy_for_level(game_level, difficulty_mult)
                                    combat = Combat(player, enemy)
                                    message = get_level_intro(game_level, enemy)
                                    
                                    # Reload enemy sprites
                                    enemy_sprites = load_character_sprites(enemy.sprite_path, scale=0.8)
                                    enemy_animation_state = 'normal'
                                    player_animation_state = 'normal'
                                    
                                    try:
                                        background_img = asset_manager.get_background(game_level)
                                        if settings['music_enabled']:
                                            asset_manager.stop_music(fade_ms=500)
                                            play_level_music(game_level)
                                    except:
                                        pass

                    # Defend
                    if defend_btn.collidepoint(mx, my):
                        msg = combat.player_defend()
                        message = msg
                        
                        over, winner = combat.is_over()
                        if not over:
                            pygame.time.set_timer(pygame.USEREVENT+1, 500, loops=1)

                    # Special
                    if special_btn.collidepoint(mx, my):
                        threshold = player.get_special_threshold()
                        if weapon_damage_count >= threshold and special_ability_count < 3:
                            msg = combat.player_special_attack()
                            special_damage = player.get_weapon_damage() * 2
                            total_damage_dealt += special_damage
                            message = msg
                            weapon_damage_count = 0
                            special_ability_count += 1
                            
                            # Trigger ENEMY damage animation
                            enemy_animation_state = 'damage'
                            enemy_animation_timer = current_time + DAMAGE_ANIMATION_DURATION
                            
                            if SOUND_ATTACK and settings['sound_enabled']: 
                                SOUND_ATTACK.play()
                            
                            over, winner = combat.is_over()
                            if not over:
                                pygame.time.set_timer(pygame.USEREVENT+1, 500, loops=1)
                            else:
                                if winner == "player":
                                    enemies_defeated += 1
                                    
                                    # Show PLAYER victory animation
                                    player_animation_state = 'victory'
                                    player_animation_timer = current_time + VICTORY_ANIMATION_DURATION
                                    
                                    handle_victory(player, enemy, combat, save_system, game_level)
                                    
                                    if game_level >= 3:
                                        completion_time = time.time() - run_start_time
                                        save_system.save_to_leaderboard(
                                            player.name, 
                                            completion_time, 
                                            total_damage_dealt, 
                                            enemies_defeated
                                        )
                                        
                                        message = f"🎉 GAME FINISHED! You escaped!\nTime: {int(completion_time//60)}m {int(completion_time%60)}s"
                                        if SOUND_WIN and settings['sound_enabled']: 
                                            SOUND_WIN.play()
                                        
                                        pygame.time.wait(VICTORY_ANIMATION_DURATION)
                                        
                                        show_victory_screen(screen, player, completion_time, 
                                                           total_damage_dealt, enemies_defeated, 
                                                           settings['difficulty'], font, bigfont)
                                        
                                        save_system.save_character(player, 1)
                                        try:
                                            asset_manager.stop_music(fade_ms=1000)
                                        except:
                                            pass
                                        running = False
                                    else:
                                        pygame.time.wait(VICTORY_ANIMATION_DURATION)
                                        
                                        game_level += 1
                                        weapon_damage_count = 0
                                        special_ability_count = 0
                                        enemy = create_enemy_for_level(game_level, difficulty_mult)
                                        combat = Combat(player, enemy)
                                        message = get_level_intro(game_level, enemy)
                                        
                                        enemy_sprites = load_character_sprites(enemy.sprite_path, scale=0.8)
                                        enemy_animation_state = 'normal'
                                        player_animation_state = 'normal'
                                        
                                        try:
                                            background_img = asset_manager.get_background(game_level)
                                            if settings['music_enabled']:
                                                asset_manager.stop_music(fade_ms=500)
                                                play_level_music(game_level)
                                        except:
                                            pass
                        else:
                            if weapon_damage_count < threshold:
                                message = f"⚠️ Need {threshold - weapon_damage_count} more damage to use special!"
                            else:
                                message = "⚠️ Too much of everything is not good my friend!"
                                special_ability_count = 0

                    # Flee
                    if flee_btn.collidepoint(mx, my):
                        if random.random() < 0.6:
                            message = "🏃 You fled! Game Over."
                            save_system.save_character(player, game_level)
                            try:
                                asset_manager.stop_music(fade_ms=500)
                            except:
                                pass
                            pygame.time.wait(2000)
                            running = False
                        else:
                            message = "Couldn't escape!"
                            pygame.time.set_timer(pygame.USEREVENT+1, 500, loops=1)

                # Enemy turn event
                if ev.type == pygame.USEREVENT+1:
                    if not paused:
                        emsg = combat.enemy_turn()
                        message = emsg
                        
                        # Trigger PLAYER damage animation
                        player_animation_state = 'damage'
                        player_animation_timer = current_time + DAMAGE_ANIMATION_DURATION
                        
                        if SOUND_ATTACK and settings['sound_enabled']: 
                            SOUND_ATTACK.play()
                        
                        over, winner = combat.is_over()
                        if over and winner == "enemy":
                            message = "☠️ You were defeated..."
                            if SOUND_LOSE and settings['sound_enabled']: 
                                SOUND_LOSE.play()
                            save_system.save_combat_result(player.name, enemy.name, game_level, "Defeat")
                            try:
                                asset_manager.stop_music(fade_ms=500)
                            except:
                                pass
                            pygame.time.wait(2000)
                            running = False

            # Render - Draw background first
            if background_img:
                screen.blit(background_img, (0, 0))
            else:
                screen.fill((26, 26, 48))
            
            # Semi-transparent overlay for UI visibility
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))
            
            # Top info panel with background
            info_panel = pygame.Surface((WIDTH, 120), pygame.SRCALPHA)
            info_panel.fill((20, 20, 40, 180))
            screen.blit(info_panel, (0, 0))
            
            # Top info
            draw_text(screen, f"Player: {player.name}  Lv {player.level}", 30, 18, bigfont, (255, 255, 255))
            draw_hp_bar(screen, 30, 58, player.hp, player.max_hp)
            draw_text(screen, f"HP {player.hp}/{player.max_hp}", 300, 56, font, (255, 255, 255))
            draw_text(screen, f"Stage: {game_level}/3", 30, 95, font, (240, 200, 100))

            # Enemy info
            draw_text(screen, f"Enemy: {combat.enemy.name}  Lv {combat.enemy.level}", 600, 18, bigfont, (255, 255, 255))
            draw_hp_bar(screen, 600, 58, combat.enemy.hp, combat.enemy.max_hp)
            draw_text(screen, f"HP {combat.enemy.hp}/{combat.enemy.max_hp}", 860, 56, font, (255, 255, 255))
            
            # Pause button
            pygame.draw.rect(screen, (155, 89, 182), pause_btn)
            pause_text = font.render("⏸", True, (255, 255, 255))
            screen.blit(pause_text, (pause_btn.x + 18, pause_btn.y + 2))

            # Draw PLAYER sprite with animation
            current_player_sprite = player_sprites.get(player_animation_state)
            if not current_player_sprite or player_animation_state not in player_sprites:
                current_player_sprite = player_sprites.get('normal')
            
            if current_player_sprite:
                screen.blit(current_player_sprite, (60, 120))
            else:
                pygame.draw.rect(screen, (100, 100, 255), (60, 140, 80, 120))
                draw_text(screen, player.weapon, 65, 265, font, (255, 255, 255))
            
            # Draw ENEMY sprite with animation
            current_enemy_sprite = enemy_sprites.get(enemy_animation_state)
            if not current_enemy_sprite or enemy_animation_state not in enemy_sprites:
                current_enemy_sprite = enemy_sprites.get('normal')
            
            if current_enemy_sprite:
                screen.blit(current_enemy_sprite, (640, 120))
            else:
                pygame.draw.rect(screen, (255, 100, 100), (640, 140, 80, 120))
                draw_text(screen, enemy.name[:8], 645, 265, font, (255, 255, 255))

            # Action buttons
            pygame.draw.rect(screen, (200, 200, 200), attack_btn)
            pygame.draw.rect(screen, (200, 200, 200), defend_btn)
            
            # Special button color based on availability
            threshold = player.get_special_threshold()
            if weapon_damage_count >= threshold and special_ability_count < 3:
                pygame.draw.rect(screen, (155, 89, 182), special_btn)
            else:
                pygame.draw.rect(screen, (100, 100, 100), special_btn)
            
            pygame.draw.rect(screen, (200, 200, 200), flee_btn)
            
            draw_text(screen, "ATTACK", attack_btn.x+30, attack_btn.y+15, font, (0, 0, 0))
            draw_text(screen, "DEFEND", defend_btn.x+30, defend_btn.y+15, font, (0, 0, 0))
            draw_text(screen, "SPECIAL", special_btn.x+28, special_btn.y+15, font, (0, 0, 0))
            draw_text(screen, "FLEE", flee_btn.x+50, flee_btn.y+15, font, (0, 0, 0))

            # Stats display
            elapsed_time = time.time() - run_start_time
            draw_text(screen, f"Time: {int(elapsed_time//60)}:{int(elapsed_time%60):02d}", 30, 545, font, (200, 200, 255))
            draw_text(screen, f"Damage: {weapon_damage_count}/{threshold}", 410, 545, font, (200, 200, 255))
            draw_text(screen, f"Kills: {enemies_defeated}", 750, 545, font, (200, 200, 255))

            # Message log panel
            msg_panel = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
            msg_panel.fill((20, 20, 40, 180))
            screen.blit(msg_panel, (0, 350))
            
            draw_text(screen, "Message:", 30, 360, bigfont, (255, 255, 255))
            lines = message.split('\n')
            for i, line in enumerate(lines[:3]):
                draw_text(screen, line, 30, 400 + i*25, font, (255, 255, 255))
            
            # Pause overlay
            if paused:
                pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pause_overlay.fill((0, 0, 0, 150))
                screen.blit(pause_overlay, (0, 0))
                
                pause_title = bigfont.render("⏸ PAUSED", True, (255, 255, 255))
                screen.blit(pause_title, (WIDTH//2 - pause_title.get_width()//2, HEIGHT//2 - 50))
                
                pause_hint = font.render("Press ESC or P to resume", True, (236, 240, 241))
                screen.blit(pause_hint, (WIDTH//2 - pause_hint.get_width()//2, HEIGHT//2 + 10))

            pygame.display.flip()
        
        # Save on exit
        save_system.save_character(player, game_level)
        try:
            asset_manager.stop_music()
        except:
            pass
        
    except Exception as e:
        print(f"❌ Critical error in battle GUI: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

def show_victory_screen(screen, player, completion_time, total_damage, enemies_defeated, difficulty, font, bigfont):
    """Show victory stats screen"""
    minutes = int(completion_time // 60)
    seconds = int(completion_time % 60)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    y = 100
    title = bigfont.render("🎉 VICTORY! 🎉", True, (241, 196, 15))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, y))
    
    y += 80
    stats = [
        f"🌅 You have escaped the streets!",
        f"",
        f"⏱️ Completion Time: {minutes}m {seconds}s",
        f"💥 Total Damage: {total_damage}",
        f"⚔️ Enemies Defeated: {enemies_defeated}",
        f"🎯 Difficulty: {difficulty}",
        f"",
        f"Thanks for playing!"
    ]
    
    for stat in stats:
        text = font.render(stat, True, (236, 240, 241))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, y))
        y += 35
    
    pygame.display.flip()
    pygame.time.wait(5000)

def get_level_intro(level: int, enemy: Character) -> str:
    """Get intro text for level"""
    intros = {
        1: f"🌳 You spawned in the thick Forests of Nigeria\nA wild {enemy.name} blocks your path!",
        2: f"🏙️ You escaped the forest, but the city is dangerous!\nA {enemy.name} confronts you!",
        3: f"🏛️ FINAL LEVEL: The {enemy.name}\nThe most dangerous foe... Your last stand!"
    }
    return intros.get(level, f"⚔️ A wild {enemy.name} appears!")

def handle_victory(player: Character, enemy: Character, combat: Combat, save_system: SaveSystem, level: int):
    """Handle victory - restore HP and give XP"""
    try:
        player.hp = player.max_hp
        xp = combat.reward_xp_for_enemy()
        leveled = player.gain_xp(xp)
        save_system.save_combat_result(player.name, enemy.name, level, "Victory")
        
        settings = save_system.load_settings()
        if SOUND_WIN and settings['sound_enabled']: 
            SOUND_WIN.play()
        print(f"🎉 Victory! Gained {xp} XP")
    except Exception as e:
        print(f"❌ Error handling victory: {e}")
