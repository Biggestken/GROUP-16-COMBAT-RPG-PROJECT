# -*- coding: utf-8 -*-
"""
resources.py - Asset management for Nigerian RPG
Handles loading and caching of all game assets (images, sounds, etc.)
"""
import pygame
import os
from functools import lru_cache

ASSETS_DIR = "assets"
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")

# Create directories if they don't exist
os.makedirs(SPRITES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(BACKGROUNDS_DIR, exist_ok=True)

class AssetManager:
    """Manages all game assets with caching"""
    
    def __init__(self):
        self.image_cache = {}
        self.sound_cache = {}
        self.background_cache = {}
        
    def load_image(self, filename, scale=1.0, category="sprites"):
        """
        Load image with caching
        Args:
            filename: Image filename
            scale: Scale factor (1.0 = original size)
            category: "sprites", "backgrounds", etc.
        """
        cache_key = (filename, scale, category)
        
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        if category == "sprites":
            path = os.path.join(SPRITES_DIR, filename)
        elif category == "backgrounds":
            path = os.path.join(BACKGROUNDS_DIR, filename)
        else:
            path = os.path.join(ASSETS_DIR, filename)
        
        try:
            img = pygame.image.load(path).convert_alpha()
            if scale != 1.0:
                w, h = img.get_size()
                img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
            self.image_cache[cache_key] = img
            print(f"✅ Loaded image: {filename}")
            return img
        except Exception as e:
            print(f"⚠️  Could not load image {filename}: {e}")
            return None
    
    def load_sound(self, filename):
        """
        Load sound with caching
        Args:
            filename: Sound filename
        """
        if filename in self.sound_cache:
            return self.sound_cache[filename]
        
        path = os.path.join(AUDIO_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            self.sound_cache[filename] = sound
            print(f"✅ Loaded sound: {filename}")
            return sound
        except Exception as e:
            print(f"⚠️  Could not load sound {filename}: {e}")
            return None
    
    def load_music(self, filename):
        """
        Load background music (streamed, not cached)
        Args:
            filename: Music filename
        """
        path = os.path.join(AUDIO_DIR, filename)
        try:
            pygame.mixer.music.load(path)
            print(f"✅ Loaded music: {filename}")
            return True
        except Exception as e:
            print(f"⚠️  Could not load music {filename}: {e}")
            return False
    
    def get_background(self, level):
        """Get background image for level"""
        background_map = {
            1: "level1_bg.png",
            2: "level2_bg.png",
            3: "level3_bg.png"
        }
        
        filename = background_map.get(level, "level1_bg.png")
        return self.load_image(filename, category="backgrounds")
    
    def get_level_music(self, level):
        """Get background music for level"""
        music_map = {
            1: "level1_bg.mp3",
            2: "level2_bg.mp3",
            3: "level3_bg.mp3"
        }
        
        filename = music_map.get(level, "level1_bg.mp3")
        return filename
    
    def play_music(self, level, loops=-1, fade_ms=0):
        """Play level music"""
        music_file = self.get_level_music(level)
        path = os.path.join(AUDIO_DIR, music_file)
        
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            print(f"🎵 Playing: {music_file}")
            return True
        except Exception as e:
            print(f"⚠️  Could not play music: {e}")
            return False
    
    def stop_music(self, fade_ms=0):
        """Stop background music"""
        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
            return True
        except Exception as e:
            print(f"⚠️  Error stopping music: {e}")
            return False
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        try:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
        except Exception as e:
            print(f"⚠️  Error setting music volume: {e}")
    
    def clear_cache(self):
        """Clear all cached assets"""
        self.image_cache.clear()
        self.sound_cache.clear()
        print("✅ Asset cache cleared")

# Global asset manager instance
asset_manager = AssetManager()

# Convenience functions
def load_background(level):
    """Load background for level"""
    return asset_manager.get_background(level)

def play_level_music(level):
    """Play music for level"""
    return asset_manager.play_music(level)

def load_sound_effect(filename):
    """Load sound effect"""
    return asset_manager.load_sound(filename)

def play_sound(filename):
    """Load and play sound effect"""
    sound = load_sound_effect(filename)
    if sound:
        sound.play()
