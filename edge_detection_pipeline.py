import cv2
import numpy as np
from bottle_detector import BottleDetector
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

redundancy_range = 10

bottle_detector = BottleDetector(redundancy_range)

class BottleEdgeDetectionPipeline:
    def run_bottle_edge_detection_pipeline(self, bottle_production_video_file_path='./data/bottle_production.mp4', blurRestOfFrame=False):
        bottle_production_video = cv2.VideoCapture(bottle_production_video_file_path)

        if not bottle_production_video.isOpened():
            print("Error opening video capture")
            return

        # cv2.namedWindow('Edge Detection', cv2.WINDOW_NORMAL)
        # plt.figure('Edge Detection')

        while True:
            ret, frame = bottle_production_video.read()
            if not ret:
                break

            focus_segment = bottle_detector.perform_edge_detection_on_focus_segment(frame, blurRestOfFrame)
            bottle_detector.draw_focus_area_and_text(focus_segment, "Scanning Bottles")

            ret, jpeg = cv2.imencode('.jpg', focus_segment)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        #     # cv2.imshow('Scanning Bottles', focus_segment)
        #     plt.imshow(cv2.cvtColor(focus_segment, cv2.COLOR_BGR2RGB))
        #     plt.title('Scanning Bottles')
        #     plt.draw()
        #     plt.pause(0.01)

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        # bottle_production_video.release()
        # cv2.destroyAllWindows()

if __name__ == "__main__":
  BottleEdgeDetectionPipeline().run_bottle_edge_detection_pipeline()
