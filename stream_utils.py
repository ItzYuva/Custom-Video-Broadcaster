import cv2


class Streaming():
    def __init__(self):
        pass

    def list_availavle_devices(self):
        devices = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                devices.append({})
                
        return devices
    
    