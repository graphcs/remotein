#!/usr/bin/env python3
"""
Setup script for Python Remote Control Software
Handles virtual environment creation and dependency installation.
"""

import sys
import subprocess
import os
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr.strip()}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    else:
        print("✅ Python version compatible")
        return True


def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("venv")

    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True

    print("📦 Creating virtual environment...")

    # Try different venv creation methods
    commands = [
        f"{sys.executable} -m venv venv",
        "python3 -m venv venv",
        "python -m venv venv",
    ]

    for cmd in commands:
        if run_command(cmd, "Creating virtual environment"):
            return True

    print("❌ Failed to create virtual environment")
    return False


def get_activation_command():
    """Get the correct activation command for the platform"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def install_dependencies():
    """Install dependencies in the virtual environment"""
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"

    # Upgrade pip first
    if not run_command(f"{pip_path} install --upgrade pip", "Upgrading pip"):
        return False

    # Install requirements
    if not run_command(
        f"{pip_path} install -r requirements.txt", "Installing dependencies"
    ):
        return False

    return True


def test_installation():
    """Test the installation"""
    if platform.system() == "Windows":
        python_path = "venv\\Scripts\\python"
    else:
        python_path = "venv/bin/python"

    return run_command(f"{python_path} test_setup.py", "Testing installation")


def show_usage_instructions():
    """Show how to use the software"""
    activation_cmd = get_activation_command()

    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"

    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("📝 To use the remote control software:")
    print("")
    print("1. Activate the virtual environment:")
    print(f"   {activation_cmd}")
    print("")
    print("2. Run the software:")
    print(f"   {python_cmd} launcher.py    # Interactive launcher")
    print(f"   {python_cmd} server.py      # Server (machine to control)")
    print(f"   {python_cmd} client.py      # Client (controlling machine)")
    print("")
    print("💡 Alternative: Use the run scripts (no activation needed):")
    if platform.system() == "Windows":
        print("   run_server.bat")
        print("   run_client.bat")
        print("   run_launcher.bat")
    else:
        print("   ./run_server.sh")
        print("   ./run_client.sh")
        print("   ./run_launcher.sh")


def create_run_scripts():
    """Create convenience scripts to run without activating venv"""
    if platform.system() == "Windows":
        # Windows batch files
        scripts = {
            "run_server.bat": "venv\\Scripts\\python server.py\npause",
            "run_client.bat": '@echo off\nset /p ip="Enter server IP (or press Enter for localhost): "\nif "%ip%"=="" set ip=localhost\nvenv\\Scripts\\python client.py %ip%\npause',
            "run_launcher.bat": "venv\\Scripts\\python launcher.py\npause",
            "run_test.bat": "venv\\Scripts\\python test_setup.py\npause",
        }
    else:
        # Unix shell scripts
        scripts = {
            "run_server.sh": "#!/bin/bash\nvenv/bin/python server.py",
            "run_client.sh": '#!/bin/bash\nread -p "Enter server IP (or press Enter for localhost): " ip\nvenv/bin/python client.py ${ip:-localhost}',
            "run_launcher.sh": "#!/bin/bash\nvenv/bin/python launcher.py",
            "run_test.sh": "#!/bin/bash\nvenv/bin/python test_setup.py",
        }

    print("📝 Creating convenience scripts...")
    for filename, content in scripts.items():
        try:
            with open(filename, "w") as f:
                f.write(content)

            # Make executable on Unix systems
            if not platform.system() == "Windows":
                os.chmod(filename, 0o755)

            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"⚠️  Failed to create {filename}: {e}")


def main():
    print("🚀 Python Remote Control Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        return False

    # Create virtual environment
    if not create_virtual_environment():
        print("\n💡 Alternative installation methods:")
        print("• Use --break-system-packages flag (not recommended)")
        print("• Install with brew (macOS): brew install python-tk")
        print("• Use pipx for isolated installation")
        return False

    # Install dependencies
    if not install_dependencies():
        return False

    # Test installation
    print("\n🧪 Testing installation...")
    if not test_installation():
        print("⚠️  Installation test failed, but basic setup is complete")

    # Create convenience scripts
    create_run_scripts()

    # Show usage instructions
    show_usage_instructions()

    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during setup: {e}")
        sys.exit(1)
