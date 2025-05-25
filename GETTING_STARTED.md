# 🚀 Getting Started with Python Remote Control

This guide will walk you through setting up and using the Python Remote Control software step by step.

## 📋 Prerequisites

- **Python 3.7+** installed on both machines
- **Network connection** between the machines (same network or internet)
- **Administrator/sudo access** may be required for some features

## 🔧 Step 1: Installation

### Download and Setup

1. **Download or clone this repository** to both machines
2. **Navigate to the project directory**:
   ```bash
   cd remotein
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Verify Installation

Run the test script to ensure everything is working:
```bash
python test_setup.py
```

This will check all dependencies and provide platform-specific setup instructions.

## 🖥️ Step 2: Platform-Specific Setup

### 🍎 macOS Setup

1. **Grant Accessibility Permissions**:
   - Go to `System Preferences` → `Security & Privacy` → `Accessibility`
   - Click the lock icon and enter your password
   - Add `Terminal` or `Python` to the allowed applications
   - ✅ This allows the software to control mouse and keyboard

2. **Firewall Settings**:
   - Go to `System Preferences` → `Security & Privacy` → `Firewall`
   - Allow incoming connections for Python (if prompted)

### 🪟 Windows Setup

1. **Run as Administrator** (if needed):
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to the project directory and run the software

2. **Windows Defender**:
   - Allow Python through Windows Defender Firewall when prompted
   - Or manually add exception for port 9999

3. **Antivirus Software**:
   - Some antivirus programs may flag pyautogui as suspicious
   - Add the project folder to your antivirus whitelist if needed

### 🐧 Linux Setup

1. **Install system packages**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-tk python3-dev
   ```

2. **For headless servers** (no GUI):
   ```bash
   sudo apt-get install xvfb
   # Run server with virtual display:
   xvfb-run -a python server.py
   ```

3. **Firewall** (if enabled):
   ```bash
   sudo ufw allow 9999
   ```

## 🎯 Step 3: Basic Usage

### Method 1: Using the Launcher (Recommended)

The easiest way to get started:

1. **Run the launcher**:
   ```bash
   python launcher.py
   ```

2. **Follow the menu**:
   - Choose option 1 to run server (on machine to control)
   - Choose option 2 to run client (on controlling machine)
   - The launcher will guide you through everything!

### Method 2: Manual Setup

#### On the Computer to be Controlled (Server)

1. **Start the server**:
   ```bash
   python server.py
   ```

2. **Note the IP address** displayed in the output:
   ```
   🚀 Remote Control Server started on 0.0.0.0:9999
   📍 Your IP address: 192.168.1.100
   ```

#### On the Controlling Computer (Client)

1. **Start the client**:
   ```bash
   python client.py 192.168.1.100
   ```
   (Replace with the server's IP address)

2. **Start controlling!** 
   - Move your mouse to control the remote screen
   - Click, type, and scroll normally
   - The remote screen will appear in the window

## 🎮 Controls Reference

### Mouse Controls
- **Left Click**: Click on remote screen
- **Right Click**: Right-click on remote screen  
- **Drag**: Click and drag to select or move items
- **Scroll**: Use mouse wheel to scroll

### Keyboard Controls
- **Regular typing**: All characters are sent to remote
- **Special keys**: Arrow keys, Enter, Backspace, Tab, etc.
- **Shortcuts**:
  - `Ctrl+C` → Copy
  - `Ctrl+V` → Paste  
  - `Ctrl+A` → Select All
  - `Ctrl+Z` → Undo
  - `Ctrl+Y` → Redo

## 🔧 Configuration & Optimization

### Adjust Performance Settings

Edit `config.py` to optimize for your network:

```python
# For fast networks (high quality)
SCREEN_QUALITY = 80
SCREEN_SCALE = 0.8
FRAME_RATE = 30

# For slow networks (optimized)
SCREEN_QUALITY = 30
SCREEN_SCALE = 0.3
FRAME_RATE = 15
```

### Apply Presets

Use built-in presets for common scenarios:

```python
from config import apply_preset

# For high-speed local networks
apply_preset('high_quality')

# For mobile/slow connections  
apply_preset('mobile_network')
```

## 🌐 Network Setup Scenarios

### Same WiFi Network (Easiest)

Both computers on same network:
1. Server shows IP like `192.168.1.100`
2. Client connects to that IP
3. ✅ Should work immediately!

### Different Networks (Internet)

To connect over the internet:

1. **Port Forwarding**:
   - Configure router to forward port 9999 to server computer
   - Use router's public IP address to connect

2. **Security Warning**: Only use over trusted networks or VPN

### Corporate/Restricted Networks

If blocked by firewall:
1. Try different port in `config.py`
2. Contact IT to allow the port
3. Consider using VPN

## ❗ Troubleshooting

### Connection Issues

**"Connection Refused"**:
- ✅ Ensure server is running first
- ✅ Check IP address is correct
- ✅ Verify firewall allows port 9999
- ✅ Try `localhost` if same computer

**"Permission Denied"**:
- ✅ Grant accessibility permissions (macOS)
- ✅ Run as administrator (Windows)
- ✅ Install system packages (Linux)

### Performance Issues

**Slow/Laggy**:
- ⚙️ Reduce `SCREEN_QUALITY` in config.py
- ⚙️ Reduce `SCREEN_SCALE` (try 0.3)
- ⚙️ Lower `FRAME_RATE` (try 15)
- 📶 Check network bandwidth

**High CPU Usage**:
- ⚙️ Reduce frame rate and quality
- 🔧 Close other applications
- 💻 Use more powerful hardware

### Keyboard/Mouse Not Working

- ✅ Ensure client window has focus
- ✅ Check accessibility permissions
- ✅ Try clicking on remote screen first
- ✅ Restart both client and server

### Common Error Messages

**"PIL not found"**:
```bash
pip install Pillow
```

**"pyautogui not found"**:
```bash
pip install pyautogui
```

**"pygame not found"**:
```bash
pip install pygame
```

## 🛡️ Security Best Practices

### Important Security Notes

⚠️ **No Built-in Security**: This software has no authentication or encryption

### Recommended Usage

✅ **Safe**:
- Same trusted network (home/office WiFi)
- Behind corporate VPN
- Between your own devices

❌ **Avoid**:
- Public networks
- Untrusted internet connections
- Production servers without additional security

### Additional Security

Consider these options for better security:
- Use through VPN connection
- Set up firewall rules
- Use SSH tunneling
- Add authentication (requires code modification)

## 🎯 Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test passed (`python test_setup.py`)
- [ ] Accessibility permissions granted (macOS)
- [ ] Firewall configured for port 9999
- [ ] Server started on target machine
- [ ] Client connected with correct IP
- [ ] Controls working properly

## 🆘 Getting Help

If you encounter issues:

1. **Run the test script**: `python test_setup.py`
2. **Check the logs**: Look for `remote_server.log`
3. **Verify network**: Can you ping between machines?
4. **Check documentation**: Review README.md
5. **Platform-specific**: Check OS-specific sections above

## 🎉 Success!

Once everything is working:
- You can control the remote computer as if sitting in front of it
- All mouse and keyboard actions are transmitted in real-time
- Use responsibly and only on systems you own or have permission to access

**Enjoy your new remote control capabilities!** 🖥️✨ 