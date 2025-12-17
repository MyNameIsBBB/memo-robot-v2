# --- CONFIGURATION ---
SERVER_IP = "192.168.215.108" # Change to Server IP if running on Pi (e.g., "192.168.1.100")
SERVER_PORT = 8765
SERVER_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/ws?role=pi"

# Serial Config
SERIAL_PORT_NAME = '/dev/ttyACM0' # Check your port!
BAUD_RATE = 9600

# Camera Config
CAMERA_INDEX = 0      # 0 for default, 1 for external USB
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 60
FPS_LIMIT = 0.06      # ~15 FPS
