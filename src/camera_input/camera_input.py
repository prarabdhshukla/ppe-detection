import cv2
from src.frame_detection.frame_detection import FrameDetector
from src.person_detection.person_detection import PersonDetector, is_person_detected
from src.ppe_detection.ppe_detection import PPEDetector, is_ppe_present

def process_frames_from_directory(directory_path):
    frame_detector = FrameDetector()
    person_detector = PersonDetector()
    ppe_detector = PPEDetector()
    video_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.mp4')]
    
    for video_file in video_files:
        cap = cv2.VideoCapture(video_file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            fg_mask = frame_detector.detect_change(frame)
            person_results = person_detector.detect_person(frame)
            if is_person_detected(person_results):
                ppe_results = ppe_detector.detect_ppe(frame)
                if not is_ppe_present(ppe_results):
                    yield frame, fg_mask, person_results, ppe_results
        cap.release()
