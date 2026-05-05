# IRL Training System (Image Detection + Robotics + Inverse Reinforcement Learning)

## 📌 Overview
This project integrates computer vision, robotics control, and inverse reinforcement learning (IRL) to build a system that can detect objects, estimate their states, and learn policies from demonstrations.

The system combines:
- Image segmentation and object detection (YOLO)
- Robot control via STR400 SDK
- Inverse Reinforcement Learning for policy learning

---
## 🚀 How to Run
Step1: Initialization
- Load YOLO model (weights initialization)
- Initialize STR400 SDK connection
- Load IRL model (if training/inference mode enabled)
- Initialize camera / input source

Step2: Simply start the system with:  
- python launcher.py

---
## 🧠 System Pipeline

1. **Object Detection & Segmentation**
   - YOLO-based detection for target objects
   - Segmentation to extract precise object regions

2. **State Estimation**
   - Convert visual outputs into 3D object positions
   - Coordinate transformation for robotic control

3. **Robot Control (STR400 SDK)**
   - Send motion commands to robotic arm
   - Control gripper actions for object manipulation

4. **Inverse Reinforcement Learning**
   - Learn reward function from demonstration data
   - Train policy to mimic expert behavior

---

## ⚙️ Technologies Used
- Python
- YOLO (Object Detection)
- Computer Vision (Segmentation)
- STR400 Robot SDK
- Inverse Reinforcement Learning
- NumPy / OpenCV

---

## 🚀 Project Goal
To build a system that bridges computer vision and robotics, enabling a robot to learn actions from visual input and human demonstrations.

---

## 📌 Notes
This project focuses on integrating machine learning, computer vision, and robotic control into a unified system for intelligent manipulation tasks.
