import json
import time
from STR400_SDK.str400 import STR400
import math
import os
import sys
import numpy as np
import serial
# 将子目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'irl_imitation_master')))
print("sys.path:", sys.path)

# 然后可以导入模块
# import mdp.gridworld3d as 
import maxent_irl
import mdp
import demo
import img_utils
from utils import *

right, left, down, up, stay = 0, 1, 2, 3, 4
action = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
y_distance = 36


def pos2idx(pos):
        """
        input:
          column-major 2d position
        returns:
          1d index
        """
        return pos[0] + pos[1] * y_distance

def idx2pos(idx):
        """
        input:
          1d idx
        returns:
          2d column-major position
        """
        return (idx % y_distance, idx // y_distance)

def rotation_matrix(roll, pitch, yaw):
    cos_roll = np.cos(roll)
    sin_roll = np.sin(roll)
    cos_pitch = np.cos(pitch)
    sin_pitch = np.sin(pitch)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)
    
    R_x = np.array([
        [1, 0, 0],
        [0, cos_roll, -sin_roll],
        [0, sin_roll, cos_roll]
    ])
    
    R_y = np.array([
        [cos_pitch, 0, sin_pitch],
        [0, 1, 0],
        [-sin_pitch, 0, cos_pitch]
    ])
    
    R_z = np.array([
        [cos_yaw, -sin_yaw, 0],
        [sin_yaw, cos_yaw, 0],
        [0, 0, 1]
    ])
    
    R = R_x @ R_y @ R_z
    return R

def grasp(x, y, z, roll, pitch, yaw, vec_to_top):

    robot = STR400(host='localhost', port=8080)
    # Activating the robot
    # robot.enable()
    print("Robot successfully activated.")

    # robot_status = robot.get_robot_status()
    # cur_x, cur_y, cur_z, cur_roll, cur_pitch, cur_yaw = robot_status['cartesianPosition']['x'], robot_status['cartesianPosition']['y'], robot_status['cartesianPosition']['z'], robot_status['cartesianPosition']['roll'], robot_status['cartesianPosition']['pitch'], robot_status['cartesianPosition']['yaw']
    R = rotation_matrix(roll, pitch, yaw)
    err = np.array([-27, 0, 0])
    rotated_err = R * err
    errx, erry, errz = rotated_err[0], rotated_err[1], rotated_err[2]

    need_stop = False;
    # robot_status = robot.get_robot_status()
    # check_roll, check_pitch, check_yaw = robot_status['cartesianPosition']['roll'], robot_status['cartesianPosition']['pitch'],robot_status['cartesianPosition']['yaw']
    # if(math.fabs(check_roll - roll) < 3 or math.fabs(check_pitch - pitch) < 3 or math.fabs(check_yaw - yaw) < 3): need_stop = True;
    # time.sleep(0.1)
    
    if(need_stop == False):
        arduino = serial.Serial('COM6', 9600)
        time.sleep(1)
        arduino.write(b'OPEN\n') 
        while True:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode('utf-8').rstrip()
                print("Arduino says:", data)
                break
            else:
                time.sleep(0.05)
        time.sleep(2)

        while True:
            task_status = robot.get_task_status()
            if task_status.get('type') is None:  # Check if the task has concluded
                print("MoveJ operation completed.")
                break
            time.sleep(0.2)    

        Cartesian = [x + errx, y + erry, z + errz, roll, pitch, yaw, 5]
        # robot.movec(Cartesian)
        time.sleep(5)

        arduino.write(b'CLOSE\n')
                
                # time.sleep(0.5) # 等待 Arduino 执行
        while True:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode('utf-8').rstrip()
                print("Arduino says:", data)
                break
            else:
                time.sleep(0.05)
                    
        time.sleep(2)

        arduino.close()

    vector = np.array(vec_to_top)
    norm = np.linalg.norm(vector)
    finish_vec = 8 / norm * 10 * vector
    
    while True:
            task_status = robot.get_task_status()
            if task_status.get('type') is None:  # Check if the task has concluded
                print("MoveJ operation completed.")
                break
            time.sleep(0.2)  
    Cartesian = [x + finish_vec[0] + errz, y + finish_vec[1] + erry, z + finish_vec[2] + errz, roll, pitch, yaw, 3]
    # robot.movec(Cartesian)

    # while True:
    #     task_status = robot.get_task_status()
    #     if task_status.get('type') is None:  # Check if the task has concluded
    #         print("MoveJ operation completed.")
    #         break
    #     time.sleep(0.2)
    # angle = [0, 0, 0, 0, 0, 0, 20]
    # robot.movej(angle)

    #         # Brief pause to allow processing of the MoveJ command
    # time.sleep(0.5)

            # Monitoring task status for the completion of the MoveJ operation
    print("Monitoring task status until MoveJ operation is completed...")

    # robot.disable()
    print("Robot is now disabled.")

if(__name__ == '__main__'):
    # y_distance, x_distance, ACT_RAND = 5, 5, 0.3
    # init_grid = np.zeros([y_distance, x_distance])
    # gw = mdp.gridworld.GridWorld(init_grid, {}, 1 - ACT_RAND)
    grasp(0, 0, 0, 0, 0, 0, (0, 0, 0))




