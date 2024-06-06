import psycopg2
from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ppe_detection_flow import PPEFlow

class FrameConsumer:
    def __init__(self, input_topic):
        self.consumer = KafkaConsumer(input_topic, bootstrap_servers='localhost:9092')

    def consume_and_process(self):
        frames = []
        for message in self.consumer:
            np_arr = np.frombuffer(message.value, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            camera_id = message.key.decode('utf-8')
            frames.append((frame, camera_id))

        PPEFlow(input_frames=frames).run()
    

if __name__ == "__main__":
    consumer = FrameConsumer(input_topic='camera-frames')
    consumer.consume_and_process()
