import psycopg2
from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import json
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
        self.conn = psycopg2.connect(
            dbname="ppe_detection",
            user="user",
            password="password",
            host="db"
        )
        self.cur = self.conn.cursor()

    def consume_and_process(self):
        for message in self.consumer:
            np_arr = np.frombuffer(message.value, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            fg_mask = self.frame_detector.detect_change(frame)
            person_results = self.person_detector.detect_person(frame)
            if is_person_detected(person_results):
                ppe_results = self.ppe_detector.detect_ppe(frame)
                detected_ppe = is_ppe_present(ppe_results)
                self.save_results_to_db("camera1", frame, detected_ppe,ppe_results)
                if not detected_ppe:
                    _, buffer = cv2.imencode('.jpg', frame)
                    self.producer.send(self.output_topic, buffer.tobytes())
    
    def save_results_to_db(self, camera_id,frame,detected_ppe,details):
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        self.cur.execute(
            "INSERT INTO results (camera_id, timestamp, frame, detected_ppe, details) VALUES (%s, NOW(), %s, %s, %s)",
            (camera_id, frame_bytes, detected_ppe, json.dumps(details.tolist()))
        )
        self.conn.commit()
