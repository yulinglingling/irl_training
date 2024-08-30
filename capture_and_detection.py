import os
import cv2
import shutil
from ultralytics import YOLO
import json
import time
import numpy as np
import threading

def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
def record(*args):
    # 打开文件以进行写入（'w' 模式表示写入模式）
    with open('output.txt', 'w') as file:
        # 写入文本数据
        for arg in args:
            
            if(type(arg) == list):
                arg = map(str, arg)
                tmp = ','.join(arg)
            else: tmp = arg
            file.write(f'[{tmp}]\n')

def capture_from_camera(camera, frame_list, index, lock):
    with lock:   
        ret, frame = camera.read()
        if ret:
            frame_list[index] = frame
            print("Number of channels:", frame.shape[2])

def capture_photo(orbbec, brio, save_dir, photo_name="captured_photo.jpg"):
    # Clear the save directory
    clear_directory(save_dir)
    
    # Create the directory if it does not exist
    os.makedirs(save_dir, exist_ok=True)
    
    print("Connecting the camera...")
    # Access the camera and take a photo
    # cap = cv2.VideoCapture(0)  # 0 is the default camera
    if not (orbbec.isOpened()):
        print("Error: Could not open camera Orbbec.")
        return None
    if not brio.isOpened():
        print("Error: Could not open mx brio")
        return None
    
    # Set camera properties (adjust these values as needed)
    brio.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    brio.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    orbbec.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    orbbec.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    orbbec.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Value range: 0 to 1
    orbbec.set(cv2.CAP_PROP_CONTRAST, 0.5)    # Value range: 0 to 1
    orbbec.set(cv2.CAP_PROP_SATURATION, 0.5)  # Value range: 0 to 1
    orbbec.set(cv2.CAP_PROP_GAIN, 0.5)        # Value range: 0 to 1
    orbbec.set(cv2.CAP_PROP_EXPOSURE, -4)     # Value range: -13 to -1 (manual exposure)

    print("Taking a photo...")
    # ret, frame = orbbec.read()
    # ret_brio, frame_brio = brio.read()
    # if not ret:
    #     print("Orbbec Failed to capture image")
    #     orbbec.release()
    #     return None
    # if not ret_brio:
    #     print("Brio Failed to capture image")
    #     brio.release()
    #     return None

    # Save the captured image
    photo_path = os.path.join(save_dir, photo_name)
    photo_brio = os.path.join(save_dir, "brio.jpg")
    print(f"Saving the photo to {photo_path}")
    print(f"saving th photo to {photo_brio}")
    frames = [None, None]
    lock = threading.Lock()
    thread_o = threading.Thread(target=capture_from_camera, args=(orbbec, frames, 0, lock))
    thread_b = threading.Thread(target=capture_from_camera, args=(brio, frames, 1, lock))
    
    thread_o.start()
    thread_b.start()
    
    thread_o.join()
    thread_b.join()
    
    if frames[0] is None:
        print("Orbbec Failed to capture image")
        orbbec.release()
        return None
    if frames[1] is None:
        print("Brio Failed to capture image")
        brio.release()
        return None
    
    cv2.imwrite(photo_path, frames[0])

    cv2.imwrite(photo_brio, frames[1])
    # cap.release()
    return photo_path, photo_brio

def predict_image(model_path, image_path, confidence_threshold=0.3):
    print("Loading the trained model...")
    # Load the trained model
    model = YOLO(model_path)

    # Read the image using OpenCV
    print("Reading the image...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image {image_path}")
        return False

    print("Performing object detection...")
    # Perform inference on the image
    results = model(image)

    # Get image dimensions
    img_height, img_width, _ = image.shape
    print(f"Image resolution: {img_width}x{img_height}")

    # Process each result in the results list
    highest_confidence_boxes = {"pen": None, "cap": None}
    highest_confidence_scores = {"pen": -1, "cap": -1}
    
    for result in results:
        # Filter boxes by confidence threshold
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            if class_name in highest_confidence_boxes:
                if box.conf[0] >= confidence_threshold and box.conf[0] > highest_confidence_scores[class_name]:
                    highest_confidence_scores[class_name] = box.conf[0]
                    highest_confidence_boxes[class_name] = box

    bounding_box_info = {}
    plotted_image = image.copy()

    for class_name, box in highest_confidence_boxes.items():
        if box:
            # Get bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # Draw the bounding box
            cv2.rectangle(plotted_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # Put label and confidence
            label = f"{class_name}: {box.conf[0]:.2f}"
            cv2.putText(plotted_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # Calculate the center of the bounding box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            center_x_ratio = center_x / img_width
            center_y_ratio = center_y / img_height

            # Save bounding box information
            bounding_box_info[class_name] = {
                "center_x_ratio": center_x_ratio,
                "center_y_ratio": center_y_ratio
            }

    if "pen" not in bounding_box_info or "cap" not in bounding_box_info:
        print("Pen or cap not found")
        return False

    # Save bounding box information to JSON file
    with open('bounding_box_info.json', 'w') as f:
        json.dump(bounding_box_info, f)

    # Show the image with bounding boxes
    cv2.imshow('Prediction', plotted_image)
    cv2.waitKey(0)  # Wait for a key press to display the next image
    cv2.destroyAllWindows()  # Close the window
    return True

def capture_and_detection(orbbec, brio):
    model_path = os.path.abspath(os.path.join('model', 'best.pt'))
    # model_path = "D:\\Users\\YulingChen\\Downloads\\trainmodel-model_v3.1_2\\trainmodel-model_v3.1\\model\\best.pt"
    save_dir = os.path.abspath(os.path.join('captured_images'))
    
    photo_path, photo_brio = capture_photo(orbbec, brio, save_dir)
    

    if photo_path and photo_brio:
        # correct = predict_image(model_path, photo_path)
        correct = True
        if not correct:
            return False
        return True
    else: 
        return False

if __name__ == '__main__':
    cap0 = cv2.VideoCapture(0)
    orbbec = []
    brio = []
    if(cap0.get(cv2.CAP_PROP_FRAME_WIDTH) == 1280 and cap0.get(cv2.CAP_PROP_FRAME_HEIGHT) == 720):
        orbbec = cap0;
        brio = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        print("brio wrong")
    else:
        #  = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        orbbec = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # 使用 MSMF 后端
        print("orbbec wrong")
        brio = cap0
    while True:
        data = input("ready to continue? ");
        if(data == "exit"): break;
        tmp = capture_and_detection(orbbec, brio)
        time.sleep(3)
    orbbec.release()
    brio.release()

