#!/usr/bin/env python3
"""
Remote Control Setup Test
Verifies that all dependencies are working correctly.
"""

import sys
import platform
import socket


def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    else:
        print("✅ Python version compatible")
        return True


def test_dependencies():
    """Test all required dependencies"""
    dependencies = {
        "PIL": "Pillow (Image processing)",
        "pyautogui": "PyAutoGUI (Screen capture and automation)",
        "pygame": "Pygame (GUI framework)",
        "numpy": "NumPy (Numerical operations)",
    }

    print("\n📦 Testing Dependencies:")
    all_good = True

    for module, description in dependencies.items():
        try:
            if module == "PIL":
                import PIL
                from PIL import Image

                print(f"✅ {module} ({PIL.__version__}) - {description}")
            elif module == "pyautogui":
                import pyautogui

                print(f"✅ {module} ({pyautogui.__version__}) - {description}")
            elif module == "pygame":
                import pygame

                print(f"✅ {module} ({pygame.version.ver}) - {description}")
            elif module == "numpy":
                import numpy

                print(f"✅ {module} ({numpy.__version__}) - {description}")

        except ImportError as e:
            print(f"❌ {module} - {description} - NOT FOUND")
            print(f"   Error: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {module} - {description} - ERROR")
            print(f"   Error: {e}")
            all_good = False

    return all_good


def test_screen_capture():
    """Test screen capture functionality"""
    print("\n🖼️ Testing Screen Capture:")
    try:
        import pyautogui
        from PIL import Image

        # Take a small screenshot
        screenshot = pyautogui.screenshot(region=(0, 0, 100, 100))
        print(f"✅ Screen capture successful: {screenshot.size}")

        # Test image processing
        screenshot.thumbnail((50, 50))
        print("✅ Image processing successful")

        return True

    except Exception as e:
        print(f"❌ Screen capture failed: {e}")
        return False


def test_pygame():
    """Test pygame functionality"""
    print("\n🎮 Testing Pygame:")
    try:
        import pygame

        # Initialize pygame
        pygame.init()

        # Create a small test surface
        test_surface = pygame.Surface((100, 100))
        test_surface.fill((255, 0, 0))
        print("✅ Pygame surface creation successful")

        # Test font rendering
        font = pygame.font.Font(None, 24)
        text = font.render("Test", True, (255, 255, 255))
        print("✅ Pygame font rendering successful")

        pygame.quit()
        return True

    except Exception as e:
        print(f"❌ Pygame test failed: {e}")
        return False


def test_network():
    """Test network capabilities"""
    print("\n🌐 Testing Network:")
    try:
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"✅ Local IP address: {local_ip}")

        # Test socket creation
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.close()
        print("✅ Socket creation successful")

        return True

    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration:")
    try:
        import config

        print("✅ Configuration file loaded successfully")
        print(f"   Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
        print(f"   Quality: {config.SCREEN_QUALITY}%, Scale: {config.SCREEN_SCALE}")
        return True
    except ImportError:
        print("⚠️  Configuration file not found (using defaults)")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def show_system_info():
    """Display system information"""
    print("\n📊 System Information:")
    print(f"🖥️  OS: {platform.system()} {platform.release()}")
    print(f"🏗️  Architecture: {platform.machine()}")
    print(f"🖥️  Processor: {platform.processor()}")

    # Platform-specific advice
    if platform.system() == "Darwin":  # macOS
        print("\n🍎 macOS Specific Notes:")
        print("   • Grant accessibility permissions for screen control")
        print("   • Go to: System Preferences > Security & Privacy > Accessibility")
        print("   • Add Python or Terminal to the allowed applications")

    elif platform.system() == "Windows":
        print("\n🪟 Windows Specific Notes:")
        print("   • Run as administrator if needed")
        print("   • Check Windows Defender firewall settings")
        print("   • Allow Python through firewall for network access")

    elif platform.system() == "Linux":
        print("\n🐧 Linux Specific Notes:")
        print("   • Install required system packages:")
        print("   • sudo apt-get install python3-tk python3-dev")
        print("   • For headless: sudo apt-get install xvfb")


def run_quick_test():
    """Run a quick functionality test"""
    print("\n🚀 Running Quick Test:")
    try:
        import pyautogui
        import pygame
        from PIL import Image

        # Quick screen capture
        screenshot = pyautogui.screenshot(region=(0, 0, 50, 50))

        # Quick pygame test
        pygame.init()
        surface = pygame.Surface((50, 50))
        pygame.quit()

        print("✅ Quick test passed - Basic functionality working")
        return True

    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False


def main():
    print("🧪 REMOTE CONTROL SETUP TEST")
    print("=" * 40)

    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Screen Capture", test_screen_capture),
        ("Pygame", test_pygame),
        ("Network", test_network),
        ("Configuration", test_configuration),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Show system info
    show_system_info()

    # Summary
    print("\n📋 TEST RESULTS:")
    print("=" * 40)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\n📊 Summary: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("💡 You can now run the remote control software:")
        print("   • Server: python server.py")
        print("   • Client: python client.py")
        print("   • Launcher: python launcher.py")
    elif passed >= total - 1:
        print("\n⚠️  Most tests passed. Minor issues detected.")
        print("💡 The software should still work, but check the failed tests.")
    else:
        print("\n❌ Multiple tests failed. Please install missing dependencies:")
        print("💡 Run: pip install -r requirements.txt")

    # Quick functionality test
    if passed >= total - 1:
        run_quick_test()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        print("Please check your Python installation.")
