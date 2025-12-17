import cv2

class CameraManager:
    def __init__(self, camera_index=0, frame_width=640, frame_height=480, jpeg_quality=60):
        self.camera_index = camera_index
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.jpeg_quality = jpeg_quality
        self.camera = None

    def start(self):
        """Initialize Camera"""
        print(f"📷 Opening Camera (Index: {self.camera_index})...")
        self.camera = cv2.VideoCapture(self.camera_index)
        
        if not self.camera.isOpened():
            print("⚠️ Camera start failed. Retrying index 1...")
            self.camera = cv2.VideoCapture(1) # Fallback
            if not self.camera.isOpened():
                print("❌ Could not open any camera.")
                return False
        return True

    def get_frame_bytes(self):
        """Capture frame and return as JPEG bytes"""
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                # Resize
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                # Encode
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
                return buffer.tobytes()
        return None

    def stop(self):
        if self.camera:
            self.camera.release()
