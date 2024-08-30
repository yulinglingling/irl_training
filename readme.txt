Procedure
1. Prepare the dataset for training. Save the original images in /images and the labels in /labels.

2. Run split_images.py and it is going to split the dataset into three folders: train, val, test, with ratio 0.7:0.2:0.1.

3. If the model has not been trained, run model_training.py to train the model,
   and the trained model and the training information will be save in /runs. 
   Make sure the paths in this python file and config.yaml are correct.

4. When the task is to detect objects from images, run image_detection.py, and the results will be saved in /results.

5. When the task is to detect objects from a live stream, run real-time_detection.py.

6. When the task is to detect objects from a photo taken immediately from a camera connected to this computer, run capture_and_detection.py. 
   The photo will be saved in /captured_images. Run object_location.py to obtain the location of the object detected.