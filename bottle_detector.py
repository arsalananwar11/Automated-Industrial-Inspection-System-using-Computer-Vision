import cv2
import numpy as np

class BottleDetector:
  def __init__(self, redundancy_range = 10):
      self.redundancy_range = redundancy_range

  def get_focus_segment(self, frame, top_left = (125, 500), bottom_right = (375, 1100)):
          blurred_img = cv2.GaussianBlur(frame, (35, 35), 0)
          mask = np.zeros_like(frame, dtype=np.uint8)
          mask = cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)
          focus_segment = np.where(mask==(255, 255, 255), frame, blurred_img)
          return focus_segment

  def draw_rectangle_and_text(self, frame, type="bottle", top_left = (125, 500), bottom_right = (375, 1100)):
    if type!="bottle":
      text="Area of Focus"
      rectangle_color = (0, 0, 255)
      rectangle_border_thickness = 8
      text_weight = 3

    else:
      text = "Bottle Detected"
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

