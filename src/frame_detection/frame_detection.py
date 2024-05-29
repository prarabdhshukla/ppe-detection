import cv2

class FrameDetector:
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    
    def detect_change(self,frame):
        fg_mask = self.bg_subtractor.apply(frame)
        return fg_mask