from bottle_detection_pipeline import BottleDetectionPipeline
from edge_detection_pipeline import BottleEdgeDetectionPipeline

VIDEO_PATH = './data/bottle_production.mp4'

if __name__ == '__main__':
    print("\nSelect an option:")
    print("1. Bottle Scanning using Edge Detection")
    print("2. Bottle Detection on Conveyor Belt using Template Matching")
    print("3. Defect Detection")
    print("0. Exit")

    choice = input("Enter your choice (1-3 or 0 to exit): ")

    if choice == '1':
      print("\nSelect an option for Bottle Scanning:")
      print("1. Blur rest of the video apart from the focus area")
      print("2. Do not blur rest of the video apart from the focus area")
      print("0. Exit")
      blur_choice = input("Enter your choice (1, 2 or 0 to exit): ")
      blurRestOfFrame = True if blur_choice=='1' else False
      BottleEdgeDetectionPipeline().run_bottle_edge_detection_pipeline(VIDEO_PATH, blurRestOfFrame)
    elif choice == '2':
      BottleDetectionPipeline().run_bottle_detection_pipeline()
    elif choice == '3':
      ## To do: We need to implement some defect detection use case
      print("Feature currently being developed. Exiting!")
      exit(0)
    elif choice == '0':
      print("Thank you for using the Automated Industrial Inspection System!")
      exit(0)
    else:
      print("Invalid choice. Exiting!")
      exit(0)