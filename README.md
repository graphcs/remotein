# 🖥️ Python Remote Control Software

A simple yet powerful remote control software written in Python that allows you to control one computer from another, similar to AnyDesk.

## ✨ Features

- **Real-time screen sharing** with adjustable quality and frame rate
- **Full mouse control** (click, drag, scroll, right-click)
- **Keyboard input** including special keys and combinations (Ctrl+C, Ctrl+V, etc.)
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Low latency** optimized for smooth control experience
- **Secure TCP connection** between client and server
- **Easy setup** with minimal dependencies

## 🚀 Quick Start

### 1. Installation

First, clone or download this repository and install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running the Server (Machine to be controlled)

On the computer you want to control remotely, run:

```bash
python server.py
```

The server will start and display:
```
🚀 Remote Control Server started on 0.0.0.0:9999
💡 Waiting for client connections...
```

### 3. Running the Client (Controlling machine)

On the computer you want to control from, run:

```bash
python client.py
```

Or specify a remote server IP:

```bash
python client.py 192.168.1.100
```

## 📋 System Requirements

- **Python 3.7+**
- **Operating Systems**: Windows, macOS, Linux
- **Network**: Both machines must be able to communicate over TCP (same network or port forwarding)

## 🔧 Dependencies

- `pillow` - Image processing for screen capture
- `pyautogui` - Screen capture and input automation
- `pygame` - GUI framework for the client
- `numpy` - Image processing optimization

## 🎮 Controls

### Mouse Controls
- **Left Click**: Click on the remote screen
- **Right Click**: Right-click on the remote screen
- **Mouse Drag**: Click and drag to select or move items
- **Scroll Wheel**: Scroll up/down on the remote screen

### Keyboard Controls
- **Regular Keys**: Type normally - all characters are sent to remote
- **Special Keys**: Arrow keys, Enter, Backspace, Tab, Escape, etc.
- **Combinations**: 
  - `Ctrl+C` - Copy
  - `Ctrl+V` - Paste
  - `Ctrl+A` - Select All

## ⚙️ Configuration

You can modify the following settings in `server.py`:

```python
# Image quality (1-100, higher = better quality but slower)
self.screen_quality = 50

# Screen scaling (0.1-1.0, lower = faster but less detail)
self.screen_scale = 0.5

# Server settings
host = '0.0.0.0'  # Listen on all interfaces
port = 9999       # Default port
```

## 🔒 Security Considerations

⚠️ **Important Security Notes:**

1. **No Authentication**: This software currently has no built-in authentication. Only use on trusted networks.
2. **No Encryption**: Data is sent unencrypted. Avoid using over public networks.
3. **Full Control**: The server gives complete control of the machine to any connected client.

### Recommended Security Measures:

- Use only on private, trusted networks
- Consider running through a VPN
- Use firewall rules to restrict access
- Add authentication if deploying in production

## 🌐 Network Setup

### Local Network
If both computers are on the same network, just use the local IP address:
```bash
python client.py 192.168.1.100
```

### Remote Access (Internet)
1. Configure port forwarding on your router for port 9999
2. Use your public IP address to connect
3. Consider using a VPN for security

### Finding IP Address

**Windows:**
```cmd
ipconfig
```

**macOS/Linux:**
```bash
ifconfig
# or
ip addr show
```

## 🐛 Troubleshooting

### Common Issues

**1. Connection Refused**
- Ensure the server is running first
- Check if the IP address and port are correct
- Verify firewall settings allow connections on port 9999

**2. Poor Performance**
- Reduce `screen_quality` in server.py (try 30-40)
- Increase `screen_scale` value (try 0.3)
- Check network bandwidth

**3. Keyboard Not Working**
- Ensure the client window has focus
- Some special keys might not work depending on the OS

**4. Permission Errors (macOS)**
```bash
# Grant accessibility permissions to Terminal/Python in:
# System Preferences > Security & Privacy > Accessibility
```

### Performance Optimization

For better performance on slower networks:

```python
# In server.py, adjust these values:
self.screen_quality = 30    # Lower quality
self.screen_scale = 0.3     # Smaller resolution
time.sleep(1/15)           # Lower frame rate (15 FPS)
```

## 🔧 Advanced Usage

### Custom Port
```bash
# Modify server.py and client.py to use different port
python server.py  # Change port in RemoteControlServer.__init__
python client.py <ip>  # Update port in main()
```

### Multiple Clients
The server supports multiple simultaneous client connections.

### Headless Server
For running on servers without GUI, you might need to set up a virtual display:

```bash
# Linux with xvfb
sudo apt-get install xvfb
xvfb-run -a python server.py
```

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source. Use responsibly and in accordance with local laws and regulations.

## ⚠️ Disclaimer

This software is for educational and legitimate remote access purposes only. Users are responsible for complying with applicable laws and obtaining proper authorization before accessing remote systems. 
