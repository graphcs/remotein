#!/usr/bin/env python3
"""
Remote Control Configuration
Centralized configuration for server and client settings.
"""

# =============================================================================
# SERVER CONFIGURATION
# =============================================================================

# Network Settings
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces (0.0.0.0) or specific IP
SERVER_PORT = 9999  # Port to listen on

# Screen Capture Settings
SCREEN_QUALITY = 50  # JPEG quality (1-100, higher = better quality but slower)
SCREEN_SCALE = 0.5  # Scale factor (0.1-1.0, lower = faster but less detail)
FRAME_RATE = 30  # Target frames per second (10-60)

# Performance Settings
MAX_CLIENTS = 5  # Maximum simultaneous client connections
BUFFER_SIZE = 4096  # Network buffer size for commands

# =============================================================================
# CLIENT CONFIGURATION
# =============================================================================

# Window Settings
CLIENT_WINDOW_WIDTH = 1024  # Default client window width
CLIENT_WINDOW_HEIGHT = 768  # Default client window height
CLIENT_RESIZABLE = True  # Allow window resizing

# Display Settings
CLIENT_FPS = 60  # Client GUI refresh rate
WINDOW_TITLE = "🖥️ Remote Control Client"

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# Connection Settings
CONNECTION_TIMEOUT = 30  # Seconds to wait for connection
RECEIVE_TIMEOUT = 5  # Seconds to wait for data

# Authentication (Future implementation)
ENABLE_AUTH = False  # Enable authentication (not implemented yet)
AUTH_PASSWORD = ""  # Password for authentication

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# PyAutoGUI Settings
PYAUTOGUI_FAILSAFE = False  # Disable PyAutoGUI failsafe (moving mouse to corner)
PYAUTOGUI_PAUSE = 0.01  # Pause between PyAutoGUI commands

# Compression Settings
USE_COMPRESSION = True  # Enable image compression
COMPRESSION_LEVEL = 6  # Compression level (1-9, higher = better compression)

# Logging Settings
ENABLE_LOGGING = True  # Enable detailed logging
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# =============================================================================
# PLATFORM-SPECIFIC SETTINGS
# =============================================================================

import platform

# macOS specific settings
if platform.system() == "Darwin":
    # macOS might need special handling for accessibility
    MACOS_ACCESSIBILITY_CHECK = True

# Windows specific settings
elif platform.system() == "Windows":
    # Windows might need admin privileges for some operations
    WINDOWS_ADMIN_MODE = False

# Linux specific settings
elif platform.system() == "Linux":
    # Linux might need virtual display for headless operation
    LINUX_VIRTUAL_DISPLAY = False
    DISPLAY_NUMBER = ":99"

# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================

# Presets for different use cases
PRESETS = {
    "high_quality": {
        "SCREEN_QUALITY": 80,
        "SCREEN_SCALE": 0.8,
        "FRAME_RATE": 30,
        "description": "High quality for fast networks",
    },
    "balanced": {
        "SCREEN_QUALITY": 50,
        "SCREEN_SCALE": 0.5,
        "FRAME_RATE": 30,
        "description": "Balanced quality and performance",
    },
    "low_bandwidth": {
        "SCREEN_QUALITY": 30,
        "SCREEN_SCALE": 0.3,
        "FRAME_RATE": 15,
        "description": "Optimized for slow connections",
    },
    "mobile_network": {
        "SCREEN_QUALITY": 20,
        "SCREEN_SCALE": 0.25,
        "FRAME_RATE": 10,
        "description": "Minimal bandwidth usage",
    },
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def apply_preset(preset_name):
    """Apply a configuration preset"""
    if preset_name not in PRESETS:
        print(f"❌ Unknown preset: {preset_name}")
        print(f"Available presets: {', '.join(PRESETS.keys())}")
        return False

    preset = PRESETS[preset_name]
    globals().update({k: v for k, v in preset.items() if k != "description"})
    print(f"✅ Applied preset '{preset_name}': {preset['description']}")
    return True


def get_config_summary():
    """Get a summary of current configuration"""
    return f"""
🔧 Current Configuration:
   📡 Server: {SERVER_HOST}:{SERVER_PORT}
   🖼️  Quality: {SCREEN_QUALITY}% | Scale: {SCREEN_SCALE} | FPS: {FRAME_RATE}
   👥 Max Clients: {MAX_CLIENTS}
   🖥️  Window: {CLIENT_WINDOW_WIDTH}x{CLIENT_WINDOW_HEIGHT}
"""


def save_custom_config(filename="custom_config.py"):
    """Save current configuration to a file"""
    try:
        with open(filename, "w") as f:
            f.write("# Custom Remote Control Configuration\n")
            f.write("# Generated automatically\n\n")

            config_vars = [
                "SERVER_HOST",
                "SERVER_PORT",
                "SCREEN_QUALITY",
                "SCREEN_SCALE",
                "FRAME_RATE",
                "MAX_CLIENTS",
                "CLIENT_WINDOW_WIDTH",
                "CLIENT_WINDOW_HEIGHT",
                "PYAUTOGUI_FAILSAFE",
                "PYAUTOGUI_PAUSE",
            ]

            for var in config_vars:
                if var in globals():
                    value = globals()[var]
                    if isinstance(value, str):
                        f.write(f"{var} = '{value}'\n")
                    else:
                        f.write(f"{var} = {value}\n")

        print(f"✅ Configuration saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False


# =============================================================================
# VALIDATION
# =============================================================================


def validate_config():
    """Validate current configuration"""
    errors = []
    warnings = []

    # Validate ranges
    if not (1 <= SCREEN_QUALITY <= 100):
        errors.append("SCREEN_QUALITY must be between 1 and 100")

    if not (0.1 <= SCREEN_SCALE <= 1.0):
        errors.append("SCREEN_SCALE must be between 0.1 and 1.0")

    if not (1 <= FRAME_RATE <= 60):
        errors.append("FRAME_RATE must be between 1 and 60")

    if not (1 <= SERVER_PORT <= 65535):
        errors.append("SERVER_PORT must be between 1 and 65535")

    # Validate performance settings
    if SCREEN_QUALITY > 70 and SCREEN_SCALE > 0.7:
        warnings.append("High quality + large scale may impact performance")

    if FRAME_RATE > 30 and SCREEN_QUALITY > 60:
        warnings.append("High frame rate + quality may use excessive bandwidth")

    # Print results
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"   • {error}")

    if warnings:
        print("⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"   • {warning}")

    if not errors and not warnings:
        print("✅ Configuration is valid")

    return len(errors) == 0


if __name__ == "__main__":
    print("🔧 Remote Control Configuration")
    print(get_config_summary())
    validate_config()

    print("\n📋 Available presets:")
    for name, preset in PRESETS.items():
        print(f"   • {name}: {preset['description']}")
