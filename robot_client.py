import asyncio
import aiohttp
import time
from config import (
    SERVER_URL, FPS_LIMIT, 
    SERIAL_PORTS, BAUD_RATE,
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, JPEG_QUALITY
)
from services.serial_manager import SerialManager
from services.camera_manager import CameraManager

class RobotClient:
    def __init__(self):
        self.ws = None
        self.session = None
        self.running = True
        
        # Initialize Managers with Config
        self.serial_manager = SerialManager(port=SERIAL_PORTS, baud_rate=BAUD_RATE)
        
        self.camera_manager = CameraManager(
            camera_index=CAMERA_INDEX,
            frame_width=FRAME_WIDTH,
            frame_height=FRAME_HEIGHT,
            jpeg_quality=JPEG_QUALITY
        )

    async def run(self):
        """Main client loop"""
        
        # 1. Setup Serial
        self.serial_manager.connect()

        # 2. Setup Camera
        self.camera_manager.start()
        
        # 3. Connect to WebSocket
        async with aiohttp.ClientSession() as session:
            self.session = session
            while self.running:
                try:
                    print(f"🔗 Connecting to Server at {SERVER_URL}...")
                    async with session.ws_connect(SERVER_URL) as ws:
                        self.ws = ws
                        print("✅ Connected to Server!")
                        
                        # Run Tasks
                        await asyncio.gather(
                            self.send_camera_fame(),
                            self.receive_messages()
                        )
                except aiohttp.ClientError as e:
                    print(f"❌ Connection Error: {e}")
                    print("   Retrying in 5 seconds...")
                    await asyncio.sleep(5)
                except Exception as e:
                    print(f"❌ Unexpected Error: {e}")
                    break
        
        # Cleanup
        self.camera_manager.stop()
        self.serial_manager.close()
        print("🛑 Client Shutdown")

    async def send_camera_fame(self):
        """Capture and send camera frames"""
        while self.running and self.ws and not self.ws.closed:
            
            frame_bytes = self.camera_manager.get_frame_bytes()
            if frame_bytes:
                try:
                    await self.ws.send_bytes(frame_bytes)
                except Exception as e:
                    print(f"Camera Send Error: {e}")
                    break
            
            # Limit FPS
            await asyncio.sleep(FPS_LIMIT)

    async def receive_messages(self):
        """Listen for messages from Server"""
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                data = msg.data
                if len(data) > 0:
                    header = data[0]
                    payload = data[1:]
                    
                    # 11 = MSG_ACTION (Command)
                    if header == 11:
                        try:
                            command = payload.decode('utf-8')
                            print(f"📩 Command: {command}")
                            self.serial_manager.send_command(command)
                        except Exception as e:
                            print(f"Command Decode Error: {e}")
                    
                    # 12 = MSG_AUDIO (TTS/Audio)
                    elif header == 12:
                        print(f"🔊 Received Audio ({len(payload)} bytes)")
                        # TODO: Play audio if needed. 
                        # On Pi: use 'aplay' or pygame
                        # self.play_audio(payload)
                        pass
                    
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print("Server Closed Connection")
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("WebSocket Error")
                break

if __name__ == "__main__":
    client = RobotClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n🛑 Stopped by User")
