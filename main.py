# -*- coding: utf-8 -*-
"""
Main menu and game initialization for Nigerian RPG
Enhanced with Settings and Leaderboard
"""
import pygame
import sys
import random
import os
from character import Character
from battle_gui import run_battle_gui_with_player
from save_system import SaveSystem

def create_player(name: str, char_class: str):
    """Create a new player character"""
    class_stats = {
        "Citizen": {"hp": 100, "atk": 5, "def": 2},
        "Soldier": {"hp": 120, "atk": 7, "def": 3},
        "Police": {"hp": 110, "atk": 6, "def": 4}
    }
    
    stats = class_stats.get(char_class, class_stats["Citizen"])
    weapon = random.choice(["Juju", "Cutlass", "Gun"])
    
    sprite_map = {
        "Citizen": "hero.png",
        "Soldier": "soldier.png",
        "Police": "police.png"
    }
    
    skills = {}
    if char_class == "Soldier":
        skills["Military Strike"] = {"power": 8, "type": "damage", "mult": 1.5}
    elif char_class == "Police":
        skills["Arrest"] = {"power": 6, "type": "damage", "mult": 1.3}
    
    p = Character(
        name=name,
        level=1,
        hp=stats["hp"],
        max_hp=stats["hp"],
        attack=stats["atk"],
        defense=stats["def"],
        char_class=char_class,
        weapon=weapon,
        xp=0,
        xp_to_next=50,
        sprite_path=sprite_map.get(char_class, "hero.png"),
        skills=skills
    )
    return p

def main_menu_loop():
    """Main menu with Pygame GUI"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((640, 700))  # Increased height for new buttons
        pygame.display.set_caption("⚔️ Escape the Streets of Nigeria")
        clock = pygame.time.Clock()
        
        try:
            font = pygame.font.SysFont("Arial", 22)
            bigfont = pygame.font.SysFont("Arial", 36)
            smallfont = pygame.font.SysFont("Arial", 18)
        except:
            print("Warning: Arial font not found, using default font")
            font = pygame.font.Font(None, 22)
            bigfont = pygame.font.Font(None, 36)
            smallfont = pygame.font.Font(None, 18)
        
        save_system = SaveSystem()
        
        # Input fields
        name_input = ""
        class_options = ["Citizen", "Soldier", "Police"]
        selected_class = 0
        input_active = True
        
        # Buttons (rearranged layout)
        start_btn = pygame.Rect(220, 320, 200, 50)
        load_btn = pygame.Rect(220, 380, 200, 50)
        settings_btn = pygame.Rect(220, 440, 200, 50)
        leaderboard_btn = pygame.Rect(220, 500, 200, 50)
        quit_btn = pygame.Rect(220, 560, 200, 50)
        class_prev_btn = pygame.Rect(170, 240, 40, 40)
        class_next_btn = pygame.Rect(430, 240, 40, 40)

        running = True
        while running:
            screen.fill((28, 28, 48))
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    save_system.close()
                    running = False
                
                if ev.type == pygame.KEYDOWN:
                    if input_active:
                        if ev.key == pygame.K_BACKSPACE:
                            name_input = name_input[:-1]
                        elif ev.key == pygame.K_RETURN:
                            input_active = False
                        elif len(name_input) < 15 and ev.unicode.isprintable():
                            name_input += ev.unicode
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    
                    # Class selection
                    if class_prev_btn.collidepoint(mx, my):
                        selected_class = (selected_class - 1) % len(class_options)
                    if class_next_btn.collidepoint(mx, my):
                        selected_class = (selected_class + 1) % len(class_options)
                    
                    # Start new game
                    if start_btn.collidepoint(mx, my):
                        if name_input.strip():
                            try:
                                player = create_player(name_input.strip(), class_options[selected_class])
                                save_system.save_character(player, 1)
                                run_battle_gui_with_player(player, save_system, 1)
                                name_input = ""
                                input_active = True
                            except Exception as e:
                                print(f"Error starting game: {e}")
                    
                    # Load game
                    if load_btn.collidepoint(mx, my):
                        try:
                            show_load_menu(save_system)
                        except Exception as e:
                            print(f"Error loading game: {e}")
                    
                    # Settings
                    if settings_btn.collidepoint(mx, my):
                        try:
                            show_settings_menu(save_system)
                        except Exception as e:
                            print(f"Error opening settings: {e}")
                    
                    # Leaderboard
                    if leaderboard_btn.collidepoint(mx, my):
                        try:
                            show_leaderboard_menu(save_system)
                        except Exception as e:
                            print(f"Error opening leaderboard: {e}")
                    
                    # Quit
                    if quit_btn.collidepoint(mx, my):
                        save_system.close()
                        running = False
            
            # Title
            title_surf = bigfont.render("⚔️ ESCAPE THE STREETS", True, (231, 76, 60))
            screen.blit(title_surf, (640//2 - title_surf.get_width()//2, 30))
            
            subtitle_surf = smallfont.render("An Urban Survival RPG", True, (243, 156, 18))
            screen.blit(subtitle_surf, (640//2 - subtitle_surf.get_width()//2, 75))
            
            # Name input
            label = font.render("Your Name:", True, (236, 240, 241))
            screen.blit(label, (220, 130))
            
            input_box = pygame.Rect(220, 160, 200, 40)
            pygame.draw.rect(screen, (52, 73, 94), input_box)
            pygame.draw.rect(screen, (255, 255, 255) if input_active else (100, 100, 100), input_box, 2)
            
            name_surf = font.render(name_input, True, (236, 240, 241))
            screen.blit(name_surf, (input_box.x + 10, input_box.y + 8))
            
            # Class selection
            class_label = font.render("Choose Your Role:", True, (236, 240, 241))
            screen.blit(class_label, (220, 210))
            
            pygame.draw.rect(screen, (180, 180, 180), class_prev_btn)
            pygame.draw.rect(screen, (180, 180, 180), class_next_btn)
            prev_text = font.render("<", True, (0, 0, 0))
            next_text = font.render(">", True, (0, 0, 0))
            screen.blit(prev_text, (class_prev_btn.x + 12, class_prev_btn.y + 8))
            screen.blit(next_text, (class_next_btn.x + 12, class_next_btn.y + 8))
            
            class_surf = font.render(class_options[selected_class], True, (46, 204, 113))
            screen.blit(class_surf, (320 - class_surf.get_width()//2, 248))
            
            # Buttons
            pygame.draw.rect(screen, (231, 76, 60), start_btn)
            pygame.draw.rect(screen, (52, 152, 219), load_btn)
            pygame.draw.rect(screen, (155, 89, 182), settings_btn)
            pygame.draw.rect(screen, (241, 196, 15), leaderboard_btn)
            pygame.draw.rect(screen, (149, 165, 166), quit_btn)
            
            start_text = font.render("START NEW GAME", True, (255, 255, 255))
            load_text = font.render("CONTINUE GAME", True, (255, 255, 255))
            settings_text = font.render("⚙️ SETTINGS", True, (255, 255, 255))
            leaderboard_text = font.render("🏆 LEADERBOARD", True, (255, 255, 255))
            quit_text = font.render("QUIT", True, (255, 255, 255))
            
            screen.blit(start_text, (start_btn.x + 25, start_btn.y + 12))
            screen.blit(load_text, (load_btn.x + 30, load_btn.y + 12))
            screen.blit(settings_text, (settings_btn.x + 50, settings_btn.y + 12))
            screen.blit(leaderboard_text, (leaderboard_btn.x + 25, leaderboard_btn.y + 12))
            screen.blit(quit_text, (quit_btn.x + 82, quit_btn.y + 12))
            
            # Version/difficulty indicator
            difficulty = save_system.get_setting('difficulty')
            diff_text = smallfont.render(f"Difficulty: {difficulty}", True, (149, 165, 166))
            screen.blit(diff_text, (640//2 - diff_text.get_width()//2, 640))
            
            pygame.display.flip()
            clock.tick(30)
        
        save_system.close()
        pygame.quit()
        
    except Exception as e:
        print(f"Critical error in main menu: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

def show_settings_menu(save_system: SaveSystem):
    """Show settings menu"""
    screen = pygame.display.set_mode((640, 600))
    pygame.display.set_caption("⚙️ Settings")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("Arial", 20)
        bigfont = pygame.font.SysFont("Arial", 32)
    except:
        font = pygame.font.Font(None, 20)
        bigfont = pygame.font.Font(None, 32)
    
    settings = save_system.load_settings()
    difficulties = ["Easy", "Normal", "Hard"]
    current_diff_idx = difficulties.index(settings['difficulty'])
    
    # Buttons
    sound_btn = pygame.Rect(220, 150, 200, 50)
    music_btn = pygame.Rect(220, 220, 200, 50)
    effects_btn = pygame.Rect(220, 290, 200, 50)
    diff_prev_btn = pygame.Rect(170, 360, 40, 40)
    diff_next_btn = pygame.Rect(430, 360, 40, 40)
    back_btn = pygame.Rect(220, 480, 200, 50)
    
    running = True
    while running:
        screen.fill((28, 28, 48))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                # Toggle sound
                if sound_btn.collidepoint(mx, my):
                    settings['sound_enabled'] = not settings['sound_enabled']
                    save_system.save_settings(settings)
                
                # Toggle music
                if music_btn.collidepoint(mx, my):
                    settings['music_enabled'] = not settings['music_enabled']
                    save_system.save_settings(settings)
                
                # Toggle effects
                if effects_btn.collidepoint(mx, my):
                    settings['screen_effects'] = not settings['screen_effects']
                    save_system.save_settings(settings)
                
                # Difficulty selection
                if diff_prev_btn.collidepoint(mx, my):
                    current_diff_idx = (current_diff_idx - 1) % len(difficulties)
                    settings['difficulty'] = difficulties[current_diff_idx]
                    save_system.save_settings(settings)
                
                if diff_next_btn.collidepoint(mx, my):
                    current_diff_idx = (current_diff_idx + 1) % len(difficulties)
                    settings['difficulty'] = difficulties[current_diff_idx]
                    save_system.save_settings(settings)
                
                # Back
                if back_btn.collidepoint(mx, my):
                    running = False
        
        # Title
        title = bigfont.render("⚙️ SETTINGS", True, (155, 89, 182))
        screen.blit(title, (640//2 - title.get_width()//2, 40))
        
        # Sound toggle
        sound_color = (46, 204, 113) if settings['sound_enabled'] else (231, 76, 60)
        sound_status = "ON" if settings['sound_enabled'] else "OFF"
        pygame.draw.rect(screen, sound_color, sound_btn)
        sound_text = font.render(f"🔊 Sound: {sound_status}", True, (255, 255, 255))
        screen.blit(sound_text, (sound_btn.x + 40, sound_btn.y + 12))
        
        # Music toggle
        music_color = (46, 204, 113) if settings['music_enabled'] else (231, 76, 60)
        music_status = "ON" if settings['music_enabled'] else "OFF"
        pygame.draw.rect(screen, music_color, music_btn)
        music_text = font.render(f"🎵 Music: {music_status}", True, (255, 255, 255))
        screen.blit(music_text, (music_btn.x + 40, music_btn.y + 12))
        
        # Effects toggle
        effects_color = (46, 204, 113) if settings['screen_effects'] else (231, 76, 60)
        effects_status = "ON" if settings['screen_effects'] else "OFF"
        pygame.draw.rect(screen, effects_color, effects_btn)
        effects_text = font.render(f"✨ Effects: {effects_status}", True, (255, 255, 255))
        screen.blit(effects_text, (effects_btn.x + 30, effects_btn.y + 12))
        
        # Difficulty selector
        diff_label = font.render("🎯 Difficulty:", True, (236, 240, 241))
        screen.blit(diff_label, (240, 370))
        
        pygame.draw.rect(screen, (180, 180, 180), diff_prev_btn)
        pygame.draw.rect(screen, (180, 180, 180), diff_next_btn)
        prev_text = font.render("<", True, (0, 0, 0))
        next_text = font.render(">", True, (0, 0, 0))
        screen.blit(prev_text, (diff_prev_btn.x + 12, diff_prev_btn.y + 10))
        screen.blit(next_text, (diff_next_btn.x + 12, diff_next_btn.y + 10))
        
        diff_colors = {"Easy": (46, 204, 113), "Normal": (241, 196, 15), "Hard": (231, 76, 60)}
        diff_surf = font.render(settings['difficulty'], True, diff_colors[settings['difficulty']])
        screen.blit(diff_surf, (320 - diff_surf.get_width()//2, 415))
        
        # Difficulty descriptions
        diff_desc = {
            "Easy": "Enemies have 75% HP",
            "Normal": "Standard difficulty",
            "Hard": "Enemies have 150% HP"
        }
        desc_surf = font.render(diff_desc[settings['difficulty']], True, (149, 165, 166))
        screen.blit(desc_surf, (320 - desc_surf.get_width()//2, 445))
        
        # Back button
        pygame.draw.rect(screen, (52, 152, 219), back_btn)
        back_text = font.render("⬅️ BACK", True, (255, 255, 255))
        screen.blit(back_text, (back_btn.x + 65, back_btn.y + 12))
        
        pygame.display.flip()
        clock.tick(30)

def show_leaderboard_menu(save_system: SaveSystem):
    """Show leaderboard menu with tabs"""
    screen = pygame.display.set_mode((700, 650))
    pygame.display.set_caption("🏆 Leaderboard")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("Arial", 16)
        bigfont = pygame.font.SysFont("Arial", 32)
        smallfont = pygame.font.SysFont("Arial", 14)
    except:
        font = pygame.font.Font(None, 16)
        bigfont = pygame.font.Font(None, 32)
        smallfont = pygame.font.Font(None, 14)
    
    # Tabs
    tabs = ["⚡ Fastest", "💥 Damage", "⚔️ Kills"]
    current_tab = 0
    
    tab_btns = [
        pygame.Rect(50, 100, 200, 40),
        pygame.Rect(250, 100, 200, 40),
        pygame.Rect(450, 100, 200, 40)
    ]
    back_btn = pygame.Rect(250, 570, 200, 50)
    
    running = True
    while running:
        screen.fill((28, 28, 48))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_LEFT:
                    current_tab = max(0, current_tab - 1)
                elif ev.key == pygame.K_RIGHT:
                    current_tab = min(2, current_tab + 1)
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                # Tab selection
                for i, btn in enumerate(tab_btns):
                    if btn.collidepoint(mx, my):
                        current_tab = i
                
                # Back
                if back_btn.collidepoint(mx, my):
                    running = False
        
        # Title
        title = bigfont.render("🏆 LEADERBOARD", True, (241, 196, 15))
        screen.blit(title, (700//2 - title.get_width()//2, 30))
        
        # Tabs
        for i, (btn, tab_name) in enumerate(zip(tab_btns, tabs)):
            color = (52, 152, 219) if i == current_tab else (52, 73, 94)
            pygame.draw.rect(screen, color, btn)
            pygame.draw.rect(screen, (236, 240, 241), btn, 2)
            tab_text = font.render(tab_name, True, (255, 255, 255))
            screen.blit(tab_text, (btn.x + btn.width//2 - tab_text.get_width()//2, btn.y + 10))
        
        # Leaderboard content
        y_start = 160
        
        if current_tab == 0:  # Fastest times
            entries = save_system.get_leaderboard_fastest()
            header = font.render("Rank | Player | Time | Kills | Difficulty", True, (236, 240, 241))
            screen.blit(header, (50, y_start))
            
            for i, entry in enumerate(entries):
                name, time, kills, diff, date = entry
                minutes = int(time // 60)
                seconds = int(time % 60)
                rank_text = f"{i+1}. {name[:12]} | {minutes}m {seconds}s | {kills} | {diff}"
                color = (241, 196, 15) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else (236, 240, 241)
                entry_surf = font.render(rank_text, True, color)
                screen.blit(entry_surf, (60, y_start + 40 + i*30))
        
        elif current_tab == 1:  # Highest damage
            entries = save_system.get_leaderboard_damage()
            header = font.render("Rank | Player | Damage | Time | Difficulty", True, (236, 240, 241))
            screen.blit(header, (50, y_start))
            
            for i, entry in enumerate(entries):
                name, damage, time, diff, date = entry
                minutes = int(time // 60)
                seconds = int(time % 60)
                rank_text = f"{i+1}. {name[:12]} | {damage} DMG | {minutes}m {seconds}s | {diff}"
                color = (241, 196, 15) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else (236, 240, 241)
                entry_surf = font.render(rank_text, True, color)
                screen.blit(entry_surf, (60, y_start + 40 + i*30))
        
        else:  # Most kills
            entries = save_system.get_leaderboard_enemies()
            header = font.render("Rank | Player | Kills | Time | Difficulty", True, (236, 240, 241))
            screen.blit(header, (50, y_start))
            
            for i, entry in enumerate(entries):
                name, kills, time, diff, date = entry
                minutes = int(time // 60)
                seconds = int(time % 60)
                rank_text = f"{i+1}. {name[:12]} | {kills} | {minutes}m {seconds}s | {diff}"
                color = (241, 196, 15) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else (236, 240, 241)
                entry_surf = font.render(rank_text, True, color)
                screen.blit(entry_surf, (60, y_start + 40 + i*30))
        
        # No entries message
        if not entries:
            no_data = font.render("No records yet! Complete a run to appear here.", True, (149, 165, 166))
            screen.blit(no_data, (700//2 - no_data.get_width()//2, y_start + 100))
        
        # Back button
        pygame.draw.rect(screen, (52, 152, 219), back_btn)
        back_text = font.render("⬅️ BACK", True, (255, 255, 255))
        screen.blit(back_text, (back_btn.x + 65, back_btn.y + 15))
        
        # Hint
        hint = smallfont.render("← → to switch tabs | ESC to exit", True, (149, 165, 166))
        screen.blit(hint, (700//2 - hint.get_width()//2, 630))
        
        pygame.display.flip()
        clock.tick(30)

def show_load_menu(save_system: SaveSystem):
    """Show load game menu"""
    saves = save_system.get_all_saves()
    
    if not saves:
        show_message_box("No saved games found!")
        return
    
    screen = pygame.display.set_mode((640, 600))
    pygame.display.set_caption("Load Game")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("Arial", 18)
        bigfont = pygame.font.SysFont("Arial", 28)
    except:
        font = pygame.font.Font(None, 18)
        bigfont = pygame.font.Font(None, 28)
    
    selected_save = 0
    
    running = True
    while running:
        screen.fill((28, 28, 48))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_UP:
                    selected_save = max(0, selected_save - 1)
                elif ev.key == pygame.K_DOWN:
                    selected_save = min(len(saves) - 1, selected_save + 1)
                elif ev.key == pygame.K_RETURN:
                    try:
                        name = saves[selected_save][0]
                        player, current_level = save_system.load_character(name)
                        if player:
                            run_battle_gui_with_player(player, save_system, current_level)
                            running = False
                    except Exception as e:
                        print(f"Error loading save: {e}")
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pygame.mouse.get_pos()
                for i in range(len(saves)):
                    rect = pygame.Rect(50, 100 + i*70, 540, 60)
                    if rect.collidepoint(mx, my):
                        try:
                            name = saves[i][0]
                            player, current_level = save_system.load_character(name)
                            if player:
                                run_battle_gui_with_player(player, save_system, current_level)
                                running = False
                        except Exception as e:
                            print(f"Error loading save: {e}")
        
        title = bigfont.render("📂 LOAD GAME", True, (52, 152, 219))
        screen.blit(title, (640//2 - title.get_width()//2, 30))
        
        for i, save in enumerate(saves):
            name, char_class, level, weapon, current_level, last_saved = save
            rect = pygame.Rect(50, 100 + i*70, 540, 60)
            
            color = (52, 152, 219) if i == selected_save else (52, 73, 94)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (236, 240, 241), rect, 2)
            
            text = f"{name} ({char_class}) - Lv {level} - {weapon} - Stage {current_level}"
            text_surf = font.render(text, True, (236, 240, 241))
            screen.blit(text_surf, (rect.x + 10, rect.y + 10))
            
            date_surf = font.render(f"Last played: {last_saved[:16]}", True, (149, 165, 166))
            screen.blit(date_surf, (rect.x + 10, rect.y + 35))
        
        hint = font.render("Click to load | ESC to cancel", True, (149, 165, 166))
        screen.blit(hint, (640//2 - hint.get_width()//2, 560))
        
        pygame.display.flip()
        clock.tick(30)

def show_message_box(message: str):
    """Simple message box"""
    screen = pygame.display.set_mode((400, 200))
    try:
        font = pygame.font.SysFont("Arial", 20)
    except:
        font = pygame.font.Font(None, 20)
    
    running = True
    start_time = pygame.time.get_ticks()
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN:
                running = False
        
        if pygame.time.get_ticks() - start_time > 2000:
            running = False
        
        screen.fill((28, 28, 48))
        text = font.render(message, True, (236, 240, 241))
        screen.blit(text, (200 - text.get_width()//2, 90))
        pygame.display.flip()

if __name__ == "__main__":
    os.makedirs("assets/sprites", exist_ok=True)
    os.makedirs("assets/audio", exist_ok=True)
    print("Starting Nigerian RPG...")
    main_menu_loop()
