from kafka import KafkaProducer
import cv2
import numpy as np 

class FrameProducer:
    def __init__(self,topic):
        self.producer=KafkaProducer(bootstrap_servers='localhost:9092')
        self.topic=topic
    
    def send_frame(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        self.producer.send(self.topic, buffer.tobytes())