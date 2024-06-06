from metaflow import FlowSpec, step
import sys
sys.path.append('..')
from frame_detection.frame_detection import FrameDetector
from person_detection.person_detection import PersonDetector, is_person_detected
from ppe_detection.ppe_detection import PPEDetector, is_ppe_present
from utils.db_utils import save_detection_to_db

class PPEFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.process_frames)
    
    @step
    def process_frames(self):
        frame_detector = FrameDetector()
        person_detector = PersonDetector()
        ppe_detector = PPEDetector()
        
        for frame, camera_id in self.input_frames:
            fg_mask = frame_detector.detect_change(frame)
            person_results = person_detector.detect_person(frame)
            if is_person_detected(person_results):
                ppe_results = ppe_detector.detect_ppe(frame)
                if not is_ppe_present(ppe_results):
                    save_detection_to_db(camera_id, frame, False, ppe_results)
                else:
                    save_detection_to_db(camera_id, frame, True, ppe_results)
        self.next(self.end)

    @step
    def end(self):
        print("Flow finished.")

if __name__ == '__main__':
    PPEFlow()