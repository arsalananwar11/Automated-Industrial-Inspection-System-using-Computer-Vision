from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from bottle_detection_pipeline import BottleDetectionPipeline
from edge_detection_pipeline import BottleEdgeDetectionPipeline
from defect_detection_pipeline import DefectDetectionPipeline
import os

app = Flask(__name__)

VIDEO_PATH = './data/bottle_production.mp4'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/bottle_scanning', methods=['GET', 'POST'])
def bottle_scanning():
    if request.method == 'POST':
        blur_choice = request.form.get('blur_choice')
        blurRestOfFrame = True if blur_choice=='1' else False
        return Response(BottleEdgeDetectionPipeline().run_bottle_edge_detection_pipeline(VIDEO_PATH, blurRestOfFrame),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('bottle_scanning.html')

@app.route('/bottle_detection')
def bottle_detection():
    return Response(BottleDetectionPipeline().run_bottle_detection_pipeline(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/defect_detection')
def defect_detection():
    # Implement defect detection here
    return render_template('defect_detection.html')

@app.route('/play_video')
def play_video():
    # Implement video playing here
    return render_template('play_video.html')

@app.route('/batch_process_folder', methods=['POST'])
def batch_process_folder():
  if 'folder_path' not in request.form:
     return jsonify({'message': 'Missing required fields: template_image or folder_path'}), 400

  folder_path = request.form['folder_path']
  template_path = './data/template.jpeg'

  output_directory = "output_directory"
  if not os.path.exists('output_directory'):
    os.makedirs(output_directory)
    print(f"Creating directory for output called {output_directory}")

  results = []
  for filename in os.listdir(folder_path):
    if not os.path.isdir(filename) and filename.split('.')[-1] == 'png':
        print(filename)
        image_path = os.path.join(folder_path, filename)
        result = DefectDetectionPipeline().template_matching(template_path, image_path, filename)
        results.append(result)

  return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)