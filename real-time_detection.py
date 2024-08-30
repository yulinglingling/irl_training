import cv2
from ultralytics import YOLO

def realtime_detection():
    model_path = 'D:\\Users\\TianHaoChen\\Desktop\\python_code\\runs\\detect\\train13\\weights\\best.pt'  # Path to the best model weights
    # Load the trained model
    model = YOLO(model_path)

    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)  # 0 is the default camera

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Perform inference on the frame
        results = model(frame)

        # Process each result in the results list
        for result in results:
            # Display the result with bounding boxes
            plotted_frame = result.plot()

        # Show the frame with bounding boxes
        cv2.imshow('Real-Time Detection', plotted_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    realtime_detection()
