import cv2
import numpy as np

class BottleDetector:
  def __init__(self, redundancy_range = 10):
      self.redundancy_range = redundancy_range

  def perform_frame_blurring(self, frame, ksize=(35,35)):
    blurred_frame = cv2.GaussianBlur(frame, (35, 35), 0)
    return blurred_frame

  def get_focus_segment(self, original_frame, blurred_frame, top_left = (125, 500), bottom_right = (375, 1100)):
    mask = np.zeros_like(original_frame, dtype=np.uint8)
    mask = cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)
    focus_segment = np.where(mask==(255, 255, 255), original_frame, blurred_frame)
    return focus_segment
  
  def edge_detection(self, frame):
    edges = cv2.Canny(frame, 100, 200)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)   
    return edges

  def perform_edge_detection_on_focus_segment(self, frame, blurRestOfFrame, top_left=(125, 500), bottom_right=(375, 1100)):
    mask = np.zeros_like(frame, dtype=np.uint8)
    mask = cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)
    edges = self.edge_detection(frame)
    if blurRestOfFrame:
      frame = cv2.GaussianBlur(frame, (35, 35), 0)
    
    focus_segment = np.where(mask == (255, 255, 255), edges, frame) 
    return focus_segment

  def draw_focus_area_and_text(self, frame, text, top_left = (125, 500), bottom_right = (375, 1100)):
    rectangle_color = (0, 0, 255)
    rectangle_border_thickness = 8
    text_weight = 3
    cv2.rectangle(frame, top_left, bottom_right, rectangle_color, rectangle_border_thickness)  
    font = cv2.FONT_HERSHEY_SIMPLEX 
    text_size, _ = cv2.getTextSize(text, font, 1, 2)  
    text_x = top_left[0] + 12
    text_y = top_left[1] - 12
    cv2.putText(frame, text, (text_x, text_y), font, 1, (240, 255, 235), text_weight)

  def draw_box_and_text(self, frame, text="Bottle Detected", top_left = (125, 500), bottom_right = (375, 1100)):
    rectangle_color = (0, 255, 0)
    rectangle_border_thickness = 3
    text_weight = 2
    cv2.rectangle(frame, top_left, bottom_right, rectangle_color, rectangle_border_thickness)  
    font = cv2.FONT_HERSHEY_SIMPLEX 
    text_size, _ = cv2.getTextSize(text, font, 1, 2)  
    text_x = top_left[0] + 12
    text_y = top_left[1] - 12
    cv2.putText(frame, text, (text_x, text_y), font, 1, (240, 255, 235), text_weight) 

  def remove_redundant_coordinates(self, coordinates):
    filtered_coordinates = []
    seen_x_values = set() 

    for point, scale in coordinates:
      x, y = point
      if round(x) not in seen_x_values:
        filtered_coordinates.append((point, scale))
        min_x = round(x-(self.redundancy_range/2))
        max_x = round(x+(self.redundancy_range/2))
        for point_x in range(min_x, max_x):
          seen_x_values.add(point_x)

    return filtered_coordinates

