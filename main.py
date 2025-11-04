#!/usr/bin/env python3
"""
Photo Enhancement Tool - Main Launcher
=====================================

This is the main entry point for the Photo Enhancement Tool application.
It handles the complete application lifecycle:

1. Shows a beautiful 60 FPS video splash screen
2. Launches the main photo enhancement interface
3. Handles errors gracefully

Usage:
    python main.py

Author: Photo Enhancement Tool Team
"""

import sys
import os
import traceback

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        ('pygame', 'pygame'),
        ('cv2', 'opencv-python'),
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('tkinter', 'tkinter (usually built-in)')
    ]
    
    missing_modules = []
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(package_name)
    
    if missing_modules:
        print("Missing required dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\nInstall missing dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def launch_splash_screen():
    """Launch the splash screen with error handling"""
    try:
        from SplashScreen import show_splash_screen
        print("Starting splash screen...")
        show_splash_screen(on_complete=launch_main_application)
    except ImportError as e:
        print(f"Could not import splash screen: {e}")
        print("Launching main application directly...")
        launch_main_application()
    except Exception as e:
        print(f"Splash screen error: {e}")
        print("Launching main application directly...")
        launch_main_application()

def launch_main_application():
    """Launch the main photo interface application"""
    try:
        from Interfaz import PhotoInterface
        print("Launching Photo Enhancement Interface...")
        app = PhotoInterface()
        app.run()
        print("Application closed successfully")
    except ImportError as e:
        print(f"Could not import main interface: {e}")
        print("Make sure Interfaz.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error in main application: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point - orchestrates the entire application"""
    print("=" * 50)
    print("Photo Enhancement Tool")
    print("=" * 50)
    print("Starting application...")
    
    # Check dependencies first
    if not check_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Launch splash screen (which will then launch main app)
    launch_splash_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
