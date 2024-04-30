import cv2
import numpy as np
from bottle_detector import BottleDetector


scale_factor_x = 2.25
scale_factor_y = 2.5
padding = 5
redundancy_range = 10
threshold = 0.58

bottle_detector = BottleDetector(redundancy_range)

class BottleDetectionPipeline:
    def __init__(self):
        self.tracks = {}  # Tracks of detected bottles
        self.next_track_id = 0  # ID for the next new track
        self.distance_threshold = 25  # Maximum distance to consider a detection part of an existing track
        self.no_detection_threshold = 10  # Frames allowed with no detections before removing a track
        self.total_bottle_count = 0

    def run_bottle_detection_pipeline(self, template_file_path='./data/template.jpeg', bottle_production_video_file_path='./data/bottle_production.mp4'):
        template = cv2.imread(template_file_path, 0)
        bottle_production_video = cv2.VideoCapture(bottle_production_video_file_path)
        template_height, template_width = template.shape[:2]
        cv2.namedWindow('Bottle Detection', cv2.WINDOW_NORMAL)

        while True:
            ret, frame = bottle_production_video.read()
            if not ret:
                break

            matches = []
            for scale in np.linspace(0.5, 1.5, 20)[::-1]:
                resized_template = cv2.resize(template, (int(template_width * scale), int(template_height * scale)), interpolation=cv2.INTER_AREA)
                resized_width, resized_height = resized_template.shape[::-1]
                if resized_template.shape[1] > frame.shape[1] or resized_template.shape[0] > frame.shape[0]:
                    continue

                blurred_frame = bottle_detector.perform_frame_blurring(frame)
                focus_segment = bottle_detector.get_focus_segment(frame, blurred_frame)
                focus_segment_gray = cv2.cvtColor(focus_segment, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(focus_segment_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(result >= threshold)
                for pt in zip(*loc[::-1]):
                    matches.append((pt, scale))
                    break  # Assumes you want the first match only for simplicity
            
            filtered_coordinates = bottle_detector.remove_redundant_coordinates(matches)
            self.update_bottle_tracks(filtered_coordinates, focus_segment.shape, resized_template.shape)

            for pt, scale in filtered_coordinates[:1]:
                top_left = (pt[0] - padding, pt[1] - padding)
                bottom_right = (pt[0] + padding + int(resized_width * scale_factor_x), pt[1] + padding + int(resized_height * scale_factor_y))
                cv2.rectangle(focus_segment, top_left, bottom_right, (0, 255, 0), 2)
                #text = "Bottle Detected"
                bottle_detector.draw_box_and_text(focus_segment, 'Bottle Detected', top_left, bottom_right)

            cv2.putText(focus_segment, f'Total Count: {self.total_bottle_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            bottle_detector.draw_focus_area_and_text(focus_segment, '')
            cv2.imshow('Bottle Detection',focus_segment)  # Display the main frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        bottle_production_video.release()
        cv2.destroyAllWindows()

    def update_bottle_tracks(self, detections, frame_shape, template_shape):
        # Update existing tracks with detected bottles or start new tracks
        new_tracks = {}
        for pt, scale in detections:
            x,y = pt
            matched = False
            for track_id, track in self.tracks.items():
                if np.sqrt((track['position'][0] - x) ** 2 + (track['position'][1] - y) ** 2) < self.distance_threshold:
                    new_tracks[track_id] = {'position': (x, y), 'scale': scale, 'frames_since_seen': 0}
                    matched = True
                    break
            if not matched:
                new_tracks[self.next_track_id] = {'position': (x, y), 'scale': scale, 'frames_since_seen': 0}
                self.next_track_id += 1
                self.total_bottle_count += 1 # Increment total bottle count

        # Increment frames since seen and remove old tracks
        for track_id, track in self.tracks.items():
            if track_id not in new_tracks:
                if track['frames_since_seen'] < self.no_detection_threshold:
                    track['frames_since_seen'] += 1
                    new_tracks[track_id] = track
                else:
                    continue  # Remove track by not adding it to new_tracks

        self.tracks = new_tracks

if __name__ == '__main__':
    bottle_detector = BottleDetector(redundancy_range=10)
    pipeline = BottleDetectionPipeline()
    pipeline.run_bottle_detection_pipeline()