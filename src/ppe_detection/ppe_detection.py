import torch
from PIL import Image
import cv2

class PPEDetector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='path_to_ppe_model.pt')

    def detect_ppe(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = self.model([img])
        return results.xyxy[0]

def is_ppe_present(results):
    ppe_classes = {1, 2}  # Example class IDs for helmet and vest
    detected_classes = set(int(det[-1]) for det in results)
    return ppe_classes.issubset(detected_classes)
