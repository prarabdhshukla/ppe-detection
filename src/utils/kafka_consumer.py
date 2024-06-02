from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frame_detection.frame_detection import FrameDetector
from person_detection.person_detection import PersonDetector, is_person_detected
from ppe_detection.ppe_detection import PPEDetector, is_ppe_present

class FrameConsumer:
    def __init__(self, input_topic, output_topic):
        self.consumer = KafkaConsumer(input_topic, bootstrap_servers='localhost:9092')
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.output_topic = output_topic
        self.frame_detector = FrameDetector()
        self.person_detector = PersonDetector()
        self.ppe_detector = PPEDetector()

    def consume_and_process(self):
        for message in self.consumer:
            np_arr = np.frombuffer(message.value, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            fg_mask = self.frame_detector.detect_change(frame)
            person_results = self.person_detector.detect_person(frame)
            if is_person_detected(person_results):
                ppe_results = self.ppe_detector.detect_ppe(frame)
                if not is_ppe_present(ppe_results):
                    _, buffer = cv2.imencode('.jpg', frame)
                    self.producer.send(self.output_topic, buffer.tobytes())
