# -*- coding: utf-8 -*-
"""
Setup script for Nigerian RPG
Creates necessary folders and checks dependencies
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        print(f"✅ Pygame is installed (version {pygame.version.ver})")
        return True
    except ImportError:
        print("❌ Pygame is not installed")
        return False

def install_pygame():
    """Install pygame using pip"""
    print("\n📦 Installing pygame...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✅ Pygame installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install pygame")
        print("   Try manually: pip install pygame")
        return False

def create_directories():
    """Create necessary game directories"""
    directories = [
        "assets",
        "assets/sprites",
        "assets/audio"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created/verified: {directory}/")
        except Exception as e:
            print(f"❌ Failed to create {directory}/: {e}")
            return False
    return True

def create_placeholder_sprites():
    """Create simple placeholder sprite images"""
    print("\n🎨 Creating placeholder sprites...")
    try:
        import pygame
        pygame.init()
        
        sprites = {
            "hero.png": (100, 150, 255),      # Blue
            "soldier.png": (100, 200, 100),    # Green
            "police.png": (50, 100, 255),      # Dark blue
            "bandit.png": (255, 100, 100),     # Red
            "kidnapper.png": (200, 50, 50),    # Dark red
            "politician.png": (150, 50, 150),  # Purple
        }
        
        for filename, color in sprites.items():
            path = os.path.join("assets", "sprites", filename)
            if not os.path.exists(path):
                # Create a simple colored rectangle
                surface = pygame.Surface((80, 120))
                surface.fill(color)
                # Add a simple border
                pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
                pygame.image.save(surface, path)
                print(f"✅ Created: {filename}")
            else:
                print(f"⏭️  Exists: {filename}")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create sprites: {e}")
        print("   Game will run without images (showing colored boxes)")
        return True  # Not critical

def verify_game_files():
    """Verify all game files exist"""
    print("\n📄 Verifying game files...")
    required_files = [
        "main.py",
        "character.py",
        "combat.py",
        "battle_gui.py",
        "save_system.py"
    ]
    
    all_exist = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ Found: {filename}")
        else:
            print(f"❌ Missing: {filename}")
            all_exist = False
    
    return all_exist

def print_summary():
    """Print setup summary"""
    print("\n" + "="*50)
    print("🎮 NIGERIAN RPG - SETUP COMPLETE")
    print("="*50)
    print("\n📖 To start the game:")
    print("   python main.py")
    print("\n📚 For more information:")
    print("   See README.md")
    print("\n💡 Tips:")
    print("   - Assets (images/sounds) are optional")
    print("   - Game auto-saves every 30 seconds")
    print("   - Use CONTINUE GAME to load saves")
    print("\n" + "="*50)

def main():
    """Main setup routine"""
    print("="*50)
    print("🎮 NIGERIAN RPG - SETUP WIZARD")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Verify game files
    if not verify_game_files():
        print("\n❌ Some game files are missing!")
        print("   Please ensure all game files are in the same directory")
        sys.exit(1)
    
    # Check/install pygame
    if not check_pygame():
        response = input("\n❓ Would you like to install pygame now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_pygame():
                sys.exit(1)
        else:
            print("\n⚠️  Pygame is required to run the game")
            print("   Install it manually: pip install pygame")
            sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Failed to create directories")
        sys.exit(1)
    
    # Create placeholder sprites
    create_placeholder_sprites()
    
    # Print summary
    print_summary()
    
    # Ask if user wants to start the game
    response = input("\n❓ Would you like to start the game now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("\n🚀 Starting game...\n")
        try:
            import main
            main.main_menu_loop()
        except Exception as e:
            print(f"\n❌ Error starting game: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
