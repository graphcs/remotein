#!/usr/bin/env python3
"""
Remote Control Server
Runs on the machine to be controlled.
Captures screen and executes received mouse/keyboard commands.
"""

import socket
import threading
import json
import time
import pyautogui
from PIL import Image
import io
import struct
import logging
import sys

# Import configuration
try:
    from config import *
except ImportError:
    print("⚠️ Configuration file not found, using default settings")
    # Default settings if config.py is not available
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 9999
    SCREEN_QUALITY = 50
    SCREEN_SCALE = 0.5
    FRAME_RATE = 30
    MAX_CLIENTS = 5
    PYAUTOGUI_FAILSAFE = False
    PYAUTOGUI_PAUSE = 0.01
    ENABLE_LOGGING = True
    LOG_LEVEL = "INFO"


class RemoteControlServer:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.running = False
        self.clients = []
        self.screen_quality = SCREEN_QUALITY
        self.screen_scale = SCREEN_SCALE
        self.frame_rate = FRAME_RATE
        self.max_clients = MAX_CLIENTS

        # Performance tracking
        self.frames_sent = 0
        self.start_time = time.time()
        self.last_fps_update = time.time()

        # Configure logging
        if ENABLE_LOGGING:
            logging.basicConfig(
                level=getattr(logging, LOG_LEVEL),
                format="%(asctime)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.StreamHandler(sys.stdout),
                    logging.FileHandler("remote_server.log"),
                ],
            )
            self.logger = logging.getLogger(__name__)
        else:
            # Create dummy logger if logging is disabled
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        # Configure pyautogui
        pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = PYAUTOGUI_PAUSE

        self.logger.info("🚀 Remote Control Server initialized")

    def start_server(self):
        """Start the remote control server"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_clients)
            print(f"🚀 Remote Control Server started on {self.host}:{self.port}")
            print(
                f"📊 Settings: Quality={self.screen_quality}%, Scale={self.screen_scale}, FPS={self.frame_rate}"
            )
            print("💡 Waiting for client connections...")
            self.logger.info(f"Server listening on {self.host}:{self.port}")

            # Start performance monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_performance)
            monitor_thread.daemon = True
            monitor_thread.start()

            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()

                    if len(self.clients) >= self.max_clients:
                        print(
                            f"❌ Maximum clients ({self.max_clients}) reached. Rejecting {address}"
                        )
                        client_socket.close()
                        continue

                    print(f"✅ Client connected from {address}")
                    self.logger.info(f"Client connected: {address}")

                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except socket.error as e:
                    if self.running:
                        print(f"❌ Error accepting connection: {e}")
                        self.logger.error(f"Connection error: {e}")

        except Exception as e:
            print(f"❌ Server error: {e}")
            self.logger.error(f"Server error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        self.clients.append(client_socket)

        # Start screen streaming thread for this client
        screen_thread = threading.Thread(
            target=self.stream_screen, args=(client_socket, address)
        )
        screen_thread.daemon = True
        screen_thread.start()

        try:
            while self.running and client_socket in self.clients:
                # Receive commands from client
                try:
                    client_socket.settimeout(5.0)  # 5 second timeout
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    try:
                        command = json.loads(data.decode("utf-8"))
                        self.execute_command(command)
                        self.logger.debug(
                            f"Executed command: {command.get('type', 'unknown')}"
                        )
                    except json.JSONDecodeError:
                        self.logger.warning("Received invalid JSON command")
                        continue
                except socket.timeout:
                    continue  # No data received, continue listening
                except socket.error:
                    break

        except Exception as e:
            self.logger.error(f"Client handler error for {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            try:
                client_socket.close()
            except:
                pass
            print(f"🔌 Client {address} disconnected")
            self.logger.info(f"Client disconnected: {address}")

    def capture_screen(self):
        """Capture and compress screen"""
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()

            # Convert RGBA to RGB if necessary (JPEG doesn't support transparency)
            if screenshot.mode == "RGBA":
                # Create a white background and paste the screenshot onto it
                rgb_screenshot = Image.new("RGB", screenshot.size, (255, 255, 255))
                rgb_screenshot.paste(
                    screenshot, mask=screenshot.split()[-1]
                )  # Use alpha channel as mask
                screenshot = rgb_screenshot
            elif screenshot.mode != "RGB":
                # Convert any other mode to RGB
                screenshot = screenshot.convert("RGB")

            # Scale down for better performance
            if self.screen_scale != 1.0:
                width = int(screenshot.width * self.screen_scale)
                height = int(screenshot.height * self.screen_scale)
                screenshot = screenshot.resize(
                    (width, height), Image.Resampling.LANCZOS
                )

            # Convert to JPEG bytes with optimization
            img_bytes = io.BytesIO()
            screenshot.save(
                img_bytes,
                format="JPEG",
                quality=self.screen_quality,
                optimize=True,
                progressive=True,  # Progressive JPEG for better streaming
            )
            img_bytes.seek(0)

            return img_bytes.getvalue()

        except Exception as e:
            self.logger.error(f"Screen capture error: {e}")
            return None

    def stream_screen(self, client_socket, address):
        """Stream screen to client"""
        try:
            frame_delay = 1.0 / self.frame_rate
            last_frame_time = 0

            while self.running and client_socket in self.clients:
                current_time = time.time()

                # Frame rate limiting
                if current_time - last_frame_time < frame_delay:
                    time.sleep(0.001)  # Small sleep to prevent CPU spinning
                    continue

                screen_data = self.capture_screen()
                if screen_data:
                    try:
                        # Send image size first
                        size = len(screen_data)
                        size_bytes = struct.pack("!I", size)
                        client_socket.send(size_bytes)

                        # Send image data in chunks
                        bytes_sent = 0
                        chunk_size = 8192  # 8KB chunks
                        while bytes_sent < size:
                            chunk = screen_data[bytes_sent : bytes_sent + chunk_size]
                            client_socket.send(chunk)
                            bytes_sent += len(chunk)

                        self.frames_sent += 1
                        last_frame_time = current_time

                    except socket.error as e:
                        self.logger.error(f"Screen streaming error for {address}: {e}")
                        break

        except Exception as e:
            self.logger.error(f"Screen streaming error for {address}: {e}")

    def execute_command(self, command):
        """Execute received mouse/keyboard commands"""
        try:
            cmd_type = command.get("type")

            if cmd_type == "mouse_move":
                x = int(command["x"] / self.screen_scale)
                y = int(command["y"] / self.screen_scale)
                pyautogui.moveTo(x, y)

            elif cmd_type == "mouse_click":
                x = int(command["x"] / self.screen_scale)
                y = int(command["y"] / self.screen_scale)
                button = command.get("button", "left")
                pyautogui.click(x, y, button=button)

            elif cmd_type == "mouse_drag":
                x1 = int(command["x1"] / self.screen_scale)
                y1 = int(command["y1"] / self.screen_scale)
                x2 = int(command["x2"] / self.screen_scale)
                y2 = int(command["y2"] / self.screen_scale)
                pyautogui.drag(x1, y1, x2, y2, duration=0.1)

            elif cmd_type == "mouse_scroll":
                x = int(command["x"] / self.screen_scale)
                y = int(command["y"] / self.screen_scale)
                clicks = command.get("clicks", 1)
                pyautogui.scroll(clicks, x=x, y=y)

            elif cmd_type == "key_press":
                key = command["key"]
                pyautogui.press(key)

            elif cmd_type == "key_combination":
                keys = command["keys"]
                pyautogui.hotkey(*keys)

            elif cmd_type == "type_text":
                text = command["text"]
                pyautogui.typewrite(text)

            elif cmd_type == "double_click":
                x = int(command["x"] / self.screen_scale)
                y = int(command["y"] / self.screen_scale)
                pyautogui.doubleClick(x, y)

        except Exception as e:
            self.logger.error(f"Command execution error: {e}")

    def monitor_performance(self):
        """Monitor and log performance metrics"""
        while self.running:
            time.sleep(10)  # Update every 10 seconds

            current_time = time.time()
            elapsed = current_time - self.start_time

            if elapsed > 0:
                avg_fps = self.frames_sent / elapsed

                # Calculate recent FPS
                if current_time - self.last_fps_update >= 10:
                    recent_frames = self.frames_sent
                    recent_fps = recent_frames / 10 if self.last_fps_update > 0 else 0

                    print(
                        f"📊 Performance: {recent_fps:.1f} FPS | {len(self.clients)} clients | {self.frames_sent} total frames"
                    )
                    self.logger.info(
                        f"Performance: FPS={recent_fps:.1f}, Clients={len(self.clients)}, TotalFrames={self.frames_sent}"
                    )

                    self.frames_sent = 0
                    self.last_fps_update = current_time
                    self.start_time = current_time

    def adjust_quality(self, change):
        """Dynamically adjust quality based on performance"""
        old_quality = self.screen_quality
        self.screen_quality = max(10, min(100, self.screen_quality + change))

        if self.screen_quality != old_quality:
            print(f"🔧 Quality adjusted: {old_quality}% → {self.screen_quality}%")
            self.logger.info(
                f"Quality adjusted from {old_quality}% to {self.screen_quality}%"
            )

    def stop_server(self):
        """Stop the server"""
        print("🛑 Stopping server...")
        self.running = False

        # Close all client connections
        for client in self.clients.copy():
            try:
                client.close()
            except:
                pass
        self.clients.clear()

        # Close server socket
        if hasattr(self, "server_socket"):
            try:
                self.server_socket.close()
            except:
                pass

        self.logger.info("Server stopped")
        print("🛑 Server stopped")


def main():
    server = RemoteControlServer()

    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        server.stop_server()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        server.logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
