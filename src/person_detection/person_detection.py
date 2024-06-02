import torch 
from torchvision import transforms
from PIL import Image
import cv2

class PersonDetector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def detect_person(self,frame):
        img=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        results = self.model([img])

        return results.xyxy[0]
    
def is_person_detected(results):
    for det in results:
        if int(det[-1]) == 0:
            return True
    return False