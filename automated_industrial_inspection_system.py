from bottle_detection_pipeline import BottleDetectionPipeline

if __name__ == '__main__':
    print("\nSelect an option:")
    print("1. Edge Detection")
    print("2. Bottle Detection on Conveyor Belt (Template Matching)")
    print("3. Defect Detection")
    print("0. Exit")

    choice = input("Enter your choice (1-3 or 0 to exit): ")

    if choice == '1':
      ## To do: We need to implement some edge detection use case
      print("Feature currently being developed. Exiting!")
      exit(0)
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