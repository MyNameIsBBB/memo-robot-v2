import serial
import time

class SerialManager:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_conn = None

    def connect(self):
        """Initialize Serial Connection to Arduino"""
        ports = self.port if isinstance(self.port, list) else [self.port]
        
        for p in ports:
            try:
                print(f"🔌 Connecting to Arduino at {p}...")
                self.serial_conn = serial.Serial(p, self.baud_rate, timeout=1)
                self.serial_conn.flush()
                
                # Wait for Arduino reboot
                print("⏳ Waiting 2 seconds for Arduino to reboot...")
                time.sleep(2)
                print(f"✅ Arduino Connected on {p}!")
                return True
            except serial.SerialException as e:
                print(f"⚠️ Connection failed on {p}: {e}")
                
        print("❌ Could not connect to any serial port.")
        print("   (Use standard keys or simulator mode if no Arduino)")
        return False

    def send_command(self, command):
        """Send string command to Arduino"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                full_msg = command + "\n"
                self.serial_conn.write(full_msg.encode('utf-8'))
                print(f"🤖 Sent to Arduino: {command}")
            except Exception as e:
                print(f"❌ Serial Write Error: {e}")
        else:
            print(f"🚫 [No Serial] Command Received: {command}")

    def close(self):
        if self.serial_conn:
            self.serial_conn.close()
