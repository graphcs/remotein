#!/usr/bin/env python3
"""
Remote Control Client
Connects to the server and provides a GUI for remote control.
Displays remote screen and sends mouse/keyboard commands.
"""

import socket
import threading
import json
import struct
import pygame
import sys
from PIL import Image
import io
import time

# Import configuration
try:
    from config import *
except ImportError:
    print("⚠️ Configuration file not found, using default settings")
    # Default settings if config.py is not available
    SERVER_PORT = 9999
    CLIENT_WINDOW_WIDTH = 1024
    CLIENT_WINDOW_HEIGHT = 768
    CLIENT_FPS = 60
    WINDOW_TITLE = "🖥️ Remote Control Client"
    CONNECTION_TIMEOUT = 30


class RemoteControlClient:
    def __init__(self):
        self.socket = None
        self.running = False
        self.screen = None
        self.clock = None
        self.remote_image = None
        self.window_size = (CLIENT_WINDOW_WIDTH, CLIENT_WINDOW_HEIGHT)
        self.connected = False
        self.dragging = False
        self.drag_start = None
        self.last_mouse_pos = None
        self.connection_time = None
        self.frames_received = 0
        self.last_frame_time = time.time()

        # Store display positioning for accurate mouse mapping
        self.display_x = 0
        self.display_y = 0
        self.display_width = 0
        self.display_height = 0
        self.scale_factor = 1.0

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def connect_to_server(self, host, port=SERVER_PORT):
        """Connect to the remote control server"""
        try:
            print(f"🔗 Connecting to {host}:{port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(CONNECTION_TIMEOUT)
            self.socket.connect((host, port))
            self.socket.settimeout(None)  # Remove timeout after connection

            self.connected = True
            self.connection_time = time.time()
            print(f"✅ Connected to {host}:{port}")

            # Start receiving screen updates
            receive_thread = threading.Thread(target=self.receive_screen_updates)
            receive_thread.daemon = True
            receive_thread.start()

            return True

        except socket.timeout:
            print(f"❌ Connection timeout after {CONNECTION_TIMEOUT} seconds")
            return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def receive_screen_updates(self):
        """Receive screen updates from server"""
        try:
            while self.running and self.connected:
                try:
                    # Receive image size
                    size_data = b""
                    while len(size_data) < 4:
                        chunk = self.socket.recv(4 - len(size_data))
                        if not chunk:
                            raise ConnectionError("Server disconnected")
                        size_data += chunk

                    size = struct.unpack("!I", size_data)[0]

                    # Receive image data
                    image_data = b""
                    while len(image_data) < size:
                        chunk_size = min(8192, size - len(image_data))
                        chunk = self.socket.recv(chunk_size)
                        if not chunk:
                            raise ConnectionError("Server disconnected")
                        image_data += chunk

                    if len(image_data) == size:
                        # Convert to pygame surface
                        pil_image = Image.open(io.BytesIO(image_data))

                        # Convert PIL image to pygame surface
                        mode = pil_image.mode
                        img_size = pil_image.size
                        raw = pil_image.tobytes()

                        if mode == "RGB":
                            self.remote_image = pygame.image.fromstring(
                                raw, img_size, mode
                            )
                        elif mode == "RGBA":
                            self.remote_image = pygame.image.fromstring(
                                raw, img_size, mode
                            )
                        else:
                            # Convert to RGB if needed
                            pil_image = pil_image.convert("RGB")
                            raw = pil_image.tobytes()
                            self.remote_image = pygame.image.fromstring(
                                raw, img_size, "RGB"
                            )

                        self.frames_received += 1
                        self.last_frame_time = time.time()

                except socket.timeout:
                    continue
                except ConnectionError as e:
                    print(f"❌ {e}")
                    break

        except Exception as e:
            print(f"❌ Screen update error: {e}")
        finally:
            self.connected = False

    def send_command(self, command):
        """Send command to server"""
        try:
            if self.connected and self.socket:
                data = json.dumps(command).encode("utf-8")
                self.socket.send(data)
        except Exception as e:
            print(f"❌ Send command error: {e}")
            self.connected = False

    def get_scaled_mouse_pos(self, mouse_pos):
        """Convert window mouse position to remote screen coordinates"""
        if not self.remote_image or self.display_width == 0 or self.display_height == 0:
            return None

        mouse_x, mouse_y = mouse_pos

        # Check if mouse is within the remote screen area
        if (
            self.display_x <= mouse_x <= self.display_x + self.display_width
            and self.display_y <= mouse_y <= self.display_y + self.display_height
        ):

            # Convert to remote coordinates using stored display info
            relative_x = mouse_x - self.display_x
            relative_y = mouse_y - self.display_y

            # Calculate remote coordinates based on original image size
            img_rect = self.remote_image.get_rect()
            remote_x = (relative_x / self.display_width) * img_rect.width
            remote_y = (relative_y / self.display_height) * img_rect.height

            return (remote_x, remote_y)

        return None

    def handle_events(self):
        """Handle pygame events and convert to remote commands"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.window_size = event.size
                self.screen = pygame.display.set_mode(
                    self.window_size, pygame.RESIZABLE
                )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                remote_pos = self.get_scaled_mouse_pos(event.pos)
                if remote_pos:
                    remote_x, remote_y = remote_pos

                    if event.button == 1:  # Left click
                        self.send_command(
                            {
                                "type": "mouse_click",
                                "x": remote_x,
                                "y": remote_y,
                                "button": "left",
                            }
                        )
                        self.dragging = True
                        self.drag_start = (remote_x, remote_y)

                    elif event.button == 3:  # Right click
                        self.send_command(
                            {
                                "type": "mouse_click",
                                "x": remote_x,
                                "y": remote_y,
                                "button": "right",
                            }
                        )

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.dragging = False
                    self.drag_start = None

            elif event.type == pygame.MOUSEMOTION:
                remote_pos = self.get_scaled_mouse_pos(event.pos)
                if remote_pos:
                    remote_x, remote_y = remote_pos

                    if self.dragging and self.drag_start:
                        # Send drag command
                        self.send_command(
                            {
                                "type": "mouse_drag",
                                "x1": self.drag_start[0],
                                "y1": self.drag_start[1],
                                "x2": remote_x,
                                "y2": remote_y,
                            }
                        )
                        self.drag_start = (remote_x, remote_y)
                    else:
                        # Send move command (throttled)
                        current_time = time.time()
                        if (
                            not self.last_mouse_pos
                            or current_time - self.last_mouse_pos > 0.05
                        ):  # 20 FPS max
                            self.send_command(
                                {"type": "mouse_move", "x": remote_x, "y": remote_y}
                            )
                            self.last_mouse_pos = current_time

            elif event.type == pygame.MOUSEWHEEL:
                remote_pos = self.get_scaled_mouse_pos(pygame.mouse.get_pos())
                if remote_pos:
                    remote_x, remote_y = remote_pos

                    self.send_command(
                        {
                            "type": "mouse_scroll",
                            "x": remote_x,
                            "y": remote_y,
                            "clicks": event.y,
                        }
                    )

            elif event.type == pygame.KEYDOWN:
                # Handle keyboard input
                key_name = pygame.key.name(event.key)

                # Handle special key combinations
                mods = pygame.key.get_pressed()
                if mods[pygame.K_LCTRL] or mods[pygame.K_RCTRL]:
                    if key_name == "c":
                        self.send_command(
                            {"type": "key_combination", "keys": ["ctrl", "c"]}
                        )
                    elif key_name == "v":
                        self.send_command(
                            {"type": "key_combination", "keys": ["ctrl", "v"]}
                        )
                    elif key_name == "a":
                        self.send_command(
                            {"type": "key_combination", "keys": ["ctrl", "a"]}
                        )
                    elif key_name == "z":
                        self.send_command(
                            {"type": "key_combination", "keys": ["ctrl", "z"]}
                        )
                    elif key_name == "y":
                        self.send_command(
                            {"type": "key_combination", "keys": ["ctrl", "y"]}
                        )
                else:
                    # Convert pygame key names to pyautogui key names
                    key_mapping = {
                        "return": "enter",
                        "backspace": "backspace",
                        "tab": "tab",
                        "escape": "esc",
                        "space": "space",
                        "up": "up",
                        "down": "down",
                        "left": "left",
                        "right": "right",
                        "delete": "delete",
                        "home": "home",
                        "end": "end",
                        "page up": "pageup",
                        "page down": "pagedown",
                    }

                    if key_name in key_mapping:
                        self.send_command(
                            {"type": "key_press", "key": key_mapping[key_name]}
                        )
                    elif len(key_name) == 1:
                        self.send_command({"type": "type_text", "text": key_name})

    def draw_connection_status(self):
        """Draw connection status and instructions"""
        if not self.connected:
            text = self.font.render("❌ Not Connected", True, (255, 0, 0))
            self.screen.blit(text, (10, 10))

            instructions = [
                "Instructions:",
                "1. Run server.py on the remote machine",
                "2. Connect using: python client.py <server_ip>",
                "3. Control the remote screen with mouse and keyboard",
            ]

            for i, instruction in enumerate(instructions):
                text = self.small_font.render(instruction, True, (255, 255, 255))
                self.screen.blit(text, (10, 60 + i * 30))

        else:
            # Connected status
            text = self.font.render("✅ Connected", True, (0, 255, 0))
            self.screen.blit(text, (10, 10))

            # Connection info
            if self.connection_time:
                uptime = time.time() - self.connection_time
                uptime_text = f"⏱️ Uptime: {int(uptime//60)}m {int(uptime%60)}s"
                uptime_surface = self.small_font.render(
                    uptime_text, True, (200, 200, 200)
                )
                self.screen.blit(uptime_surface, (10, 45))

            # Frame info
            fps_text = f"📊 Frames: {self.frames_received}"
            fps_surface = self.small_font.render(fps_text, True, (200, 200, 200))
            self.screen.blit(fps_surface, (10, 65))

            if not self.remote_image:
                waiting_text = self.font.render(
                    "⏳ Waiting for screen data...", True, (255, 255, 0)
                )
                self.screen.blit(waiting_text, (10, 90))

    def run(self, host="localhost", port=SERVER_PORT):
        """Run the client application"""
        self.running = True
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Connect to server
        if not self.connect_to_server(host, port):
            print("❌ Failed to connect to server")

        try:
            while self.running:
                self.handle_events()

                # Clear screen
                self.screen.fill((30, 30, 30))

                # Draw remote screen if available
                if self.remote_image and self.connected:
                    # Scale image to fit window while maintaining aspect ratio
                    img_rect = self.remote_image.get_rect()
                    screen_rect = self.screen.get_rect()

                    # Calculate scaling to fit screen
                    scale_x = screen_rect.width / img_rect.width
                    scale_y = screen_rect.height / img_rect.height
                    scale = min(scale_x, scale_y)

                    new_width = int(img_rect.width * scale)
                    new_height = int(img_rect.height * scale)

                    scaled_image = pygame.transform.scale(
                        self.remote_image, (new_width, new_height)
                    )

                    # Center the image and store display info for mouse mapping
                    self.display_x = (screen_rect.width - new_width) // 2
                    self.display_y = (screen_rect.height - new_height) // 2
                    self.display_width = new_width
                    self.display_height = new_height
                    self.scale_factor = scale

                    self.screen.blit(scaled_image, (self.display_x, self.display_y))
                else:
                    self.draw_connection_status()

                pygame.display.flip()
                self.clock.tick(CLIENT_FPS)

        except KeyboardInterrupt:
            print("\n🛑 Client shutting down...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.running = False
        self.connected = False
        if self.socket:
            self.socket.close()
        pygame.quit()


def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
        # Check if port is included in host (for ngrok URLs)
        if ":" in host:
            host, port_str = host.rsplit(":", 1)
            try:
                port = int(port_str)
            except ValueError:
                port = 9999
        else:
            port = 9999
    else:
        host = input("Enter server IP address (default: localhost): ").strip()
        if not host:
            host = "localhost"
        port = 9999

    client = RemoteControlClient()
    client.run(host, port)


if __name__ == "__main__":
    main()
