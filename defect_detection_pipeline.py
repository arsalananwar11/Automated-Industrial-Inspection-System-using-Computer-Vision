import base64
import cv2
import numpy as np
from bottle_detector import BottleDetector

scale_factor_x = 2.2
scale_factor_y = 2.5
padding = 5
redundancy_range = 10
threshold = 0.6

bottle_detector = BottleDetector(redundancy_range)

class DefectDetectionPipeline:
    def template_matching(self, template_path, image_path, image_name, defect_template_path = './data/defect_bottle_template.png'):
        try:
            template = cv2.imread(template_path)
            image = cv2.imread(image_path)

            if template is None or image is None:
                return {'match': False, 'message': 'Error loading images'}

            gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            best_match = None
            best_max_val = -float('inf')

            for scale in np.linspace(0.5, 1.5, 20)[::-1]:
                resized_template = cv2.resize(gray_template, None, fx=scale, fy=scale)
                resized_width, resized_height = resized_template.shape[::-1]

                if resized_width > image.shape[1] or resized_height > image.shape[0]:
                    continue

                result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                if max_val >= threshold and max_val > best_max_val:
                    best_max_val = max_val
                    best_match = (max_loc, scale)

            if best_match:
                pt, scale = best_match
                top_left = (pt[0] - padding, pt[1] - padding)
                bottom_right = (pt[0] + padding + int(resized_width * scale_factor_x), pt[1] + padding + int(resized_height * scale_factor_y))
                cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

                _, buffer = cv2.imencode('.jpg', image)
                image_as_string = base64.b64encode(buffer).decode('utf-8')

                top_left = list(top_left)
                bottom_right = list(bottom_right)

                return {
                    'match': True,
                    'image_name': image_name,
                    'image': image_as_string,
                    'top_left': top_left,
                    'bottom_right': bottom_right
                }
            else:
                template = cv2.imread(defect_template_path)
                gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                best_match = None
                best_max_val = -float('inf')

                for scale in np.linspace(0.5, 1.5, 20)[::-1]:
                    resized_template = cv2.resize(gray_template, None, fx=scale, fy=scale)
                    resized_width, resized_height = resized_template.shape[::-1]

                    if resized_width > image.shape[1] or resized_height > image.shape[0]:
                        continue

                    result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    if max_val > best_max_val:
                        best_max_val = max_val
                        best_match = (max_loc, scale)
                pt, scale = best_match
                top_left = (pt[0] - padding, pt[1] - padding)
                bottom_right = (pt[0] + padding + int(resized_width * scale_factor_x), pt[1] + padding + int(resized_height * scale_factor_y))
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

                _, buffer = cv2.imencode('.jpg', image)
                image_as_string = base64.b64encode(buffer).decode('utf-8')

                top_left = list(top_left)
                bottom_right = list(bottom_right)

                return {
                    'match': False,
                    'image_name': image_name,
                    'image': image_as_string,
                    'top_left': top_left,
                    'bottom_right': bottom_right
                }

        except Exception as e:
            print(f"Error during processing: {e}")
            return {'match': False, 'message': 'Internal error'}