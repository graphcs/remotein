#!/usr/bin/env python3
"""
Remote Control Launcher
Provides a simple menu interface for running the server or client.
"""

import subprocess
import sys
import os
import platform


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ["PIL", "pyautogui", "pygame", "numpy"]
    missing_packages = []

    for package in required_packages:
        try:
            if package == "PIL":
                import PIL
            elif package == "pyautogui":
                import pyautogui
            elif package == "pygame":
                import pygame
            elif package == "numpy":
                import numpy
        except ImportError:
            missing_packages.append(package)

    return missing_packages


def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def get_local_ip():
    """Get the local IP address"""
    try:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def run_server():
    """Run the remote control server"""
    print("\n🚀 Starting Remote Control Server...")
    print(f"📍 Your IP address: {get_local_ip()}")
    print("💡 Share this IP with the client to connect")
    print("🛑 Press Ctrl+C to stop the server\n")

    try:
        subprocess.run([sys.executable, "server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except FileNotFoundError:
        print("❌ server.py not found!")


def run_client():
    """Run the remote control client"""
    print("\n🖥️ Starting Remote Control Client...")

    # Get server IP from user
    server_ip = input("Enter server IP address (press Enter for localhost): ").strip()
    if not server_ip:
        server_ip = "localhost"

    print(f"🔗 Connecting to {server_ip}...")
    print("🛑 Close the window or press Ctrl+C to disconnect\n")

    try:
        subprocess.run([sys.executable, "client.py", server_ip])
    except KeyboardInterrupt:
        print("\n🛑 Client stopped")
    except FileNotFoundError:
        print("❌ client.py not found!")


def show_system_info():
    """Show system information and tips"""
    print("\n📊 System Information:")
    print(f"🖥️  Operating System: {platform.system()} {platform.release()}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print(f"📍 Local IP Address: {get_local_ip()}")

    print("\n💡 Platform-specific tips:")

    if platform.system() == "Darwin":  # macOS
        print("🍎 macOS:")
        print(
            "   • Grant accessibility permissions in System Preferences > Security & Privacy"
        )
        print("   • You may need to allow Python/Terminal in accessibility settings")

    elif platform.system() == "Windows":
        print("🪟 Windows:")
        print("   • Run as administrator if you encounter permission issues")
        print("   • Windows Defender might block network connections")

    elif platform.system() == "Linux":
        print("🐧 Linux:")
        print("   • You might need to install additional packages:")
        print("   • sudo apt-get install python3-tk python3-dev")
        print("   • For headless servers: sudo apt-get install xvfb")


def main_menu():
    """Display the main menu"""
    while True:
        print("\n" + "=" * 50)
        print("🖥️  PYTHON REMOTE CONTROL SOFTWARE")
        print("=" * 50)
        print("1. 🖥️  Run Server (machine to be controlled)")
        print("2. 🎮 Run Client (controlling machine)")
        print("3. 📦 Install/Check Dependencies")
        print("4. 📊 System Information")
        print("5. 📋 Quick Setup Guide")
        print("6. ❌ Exit")
        print("=" * 50)

        try:
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                # Check dependencies before running server
                missing = check_dependencies()
                if missing:
                    print(f"❌ Missing dependencies: {', '.join(missing)}")
                    print("Run option 3 to install dependencies first.")
                    continue
                run_server()

            elif choice == "2":
                # Check dependencies before running client
                missing = check_dependencies()
                if missing:
                    print(f"❌ Missing dependencies: {', '.join(missing)}")
                    print("Run option 3 to install dependencies first.")
                    continue
                run_client()

            elif choice == "3":
                missing = check_dependencies()
                if not missing:
                    print("✅ All dependencies are already installed!")
                else:
                    print(f"📦 Missing packages: {', '.join(missing)}")
                    install_choice = input("Install now? (y/n): ").strip().lower()
                    if install_choice == "y":
                        install_dependencies()

            elif choice == "4":
                show_system_info()

            elif choice == "5":
                show_quick_guide()

            elif choice == "6":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please select 1-6.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break


def show_quick_guide():
    """Show quick setup guide"""
    print("\n📋 QUICK SETUP GUIDE")
    print("=" * 40)
    print("1. 📦 Install dependencies (option 3)")
    print("2. 🖥️  On machine to control: Run Server (option 1)")
    print("3. 🎮 On controlling machine: Run Client (option 2)")
    print("4. 🔗 Enter server IP when prompted")
    print("5. 🎯 Start controlling!")
    print("")
    print("💡 TIPS:")
    print("• Both machines must be on same network")
    print("• Use firewall exceptions for port 9999")
    print("• For internet access, configure port forwarding")
    print("• Server IP is shown when starting server")


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check your Python installation and try again.")
