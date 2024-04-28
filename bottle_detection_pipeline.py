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
    def run_bottle_detection_pipeline(self, template_file_path='./data/template.jpeg', bottle_production_video_file_path='./data/bottle_production.mp4'):
        template = cv2.imread(template_file_path, 0)
        bottle_production_video = cv2.VideoCapture(bottle_production_video_file_path)
        template_height, template_width = template.shape[:2]
        cv2.namedWindow('Bottle Detection', cv2.WINDOW_NORMAL)
        while True:
            ret, frame = bottle_production_video.read()
            if not ret:
                break

            #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            matches = []

            for scale in np.linspace(0.5, 1.5, 20)[::-1]:  
                resized_template = cv2.resize(template, None, fx=scale, fy=scale)
                resized_width, resized_height = resized_template.shape[::-1]

                if resized_width > frame.shape[1] or resized_height > frame.shape[0]:
                    continue
                
                blurred_frame = bottle_detector.perform_frame_blurring(frame)
                focus_segment = bottle_detector.get_focus_segment(frame, blurred_frame)
                focus_segment_gray = cv2.cvtColor(focus_segment, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(focus_segment_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(result >= threshold)
                for pt in zip(*loc[::-1]):
                    matches.append((pt, scale))
                    break

            filtered_coordinates = bottle_detector.remove_redundant_coordinates(matches)
            for pt, scale in filtered_coordinates[:1]:
                top_left = (pt[0] - padding, pt[1] - padding)
                bottom_right = (pt[0] + padding + int(resized_width * scale_factor_x), pt[1] + padding + int(resized_height * scale_factor_y))
                cv2.rectangle(focus_segment, top_left, bottom_right, (0, 255, 0), 2)
                text = "Bottle Detected"
                bottle_detector.draw_box_and_text(focus_segment, text, top_left, bottom_right)

            text = "Area of Focus"
            bottle_detector.draw_focus_area_and_text(focus_segment, text)
            cv2.imshow('Bottle Detection', focus_segment)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        bottle_production_video.release()   
        cv2.destroyAllWindows()

if __name__ == '__main__':
    BottleDetectionPipeline().run_bottle_detection_pipeline()