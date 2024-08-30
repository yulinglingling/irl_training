# import json
import time
from STR400_SDK.str400 import STR400
import math
import serial
# import os

# vec_x, vec_y = -5, 45
def instruct(vec_x, vec_y):
    robot = STR400(host='localhost', port=8080)
        # Activating the robot
    robot.enable()

    print("Robot successfully activated.")
    plus_x, min_x, plus_ang, min_ang = 0, 1, 2, 3
    action = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    l_act = []
    robot_status = robot.get_robot_status();
    x, y, z, roll, pitch, yaw = robot_status['cartesianPosition']['x'] * 1000, robot_status['cartesianPosition']['y'] * 1000, robot_status['cartesianPosition']['z'] * 1000, robot_status['cartesianPosition']['roll'], robot_status['cartesianPosition']['pitch'], robot_status['cartesianPosition']['yaw']
    while True:
        # movx, movy, movang = 0, 0, 0
        # x, y, z, roll, pitch, yaw = 0, 0, 0, 0, 0, 0
        # robot_status = robot.get_robot_status();
        # x, y, z, roll, pitch, yaw = robot_status['cartesianPosition']['x'], robot_status['cartesianPosition']['y'], robot_status['cartesianPosition']['z'], robot_status['cartesianPosition']['roll'], robot_status['cartesianPosition']['pitch'], robot_status['cartesianPosition']['yaw']
        
        pre_x, pre_y, pre_yaw = x, y, yaw
        dir = input();
        if(dir == "exit"): break;
        elif(dir == "b"): 
            last = l_act.pop()
            tmpx, tmpy, tmpang = action[last][1] * vec_x, action[last][1] * vec_y, action[last][0] * 10
            x = x + 27 * math.cos((-yaw) * math.pi / 180) - 27 * math.cos((-yaw - movang) * math.pi / 180) + movx
            y = y + movy + 27 * math.sin((-yaw) * math.pi / 180) - 27 * math.sin((-yaw - movang) * math.pi / 180)
            z, roll, pitch, yaw = z * 1000, roll, pitch, yaw + movang
            
            CartesianPose = [x, y, z, roll, pitch, yaw, 5]
            time.sleep(5)
            print(f"move x, y, yaw: {tmpx}, {tmpy}, {tmpang}")
            continue;
            # robot.movec(CartesianPose)
        elif(dir == "g"):
            arduino = serial.Serial('COM6', 9600)
            time.sleep(2)
            arduino.write(b'OPEN\n') 
            while True:
                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').rstrip()
                    print("Arduino says:", data)
                    break
                else:
                    time.sleep(0.05)
            
            while True:
                task_status = robot.get_task_status()
                if task_status.get('type') is None:  # Check if the task has concluded
                    print("MoveC operation completed.")
                    break
                time.sleep(0.2)
            CartesianPose = [x, y, -30, roll, pitch, yaw, 10]
            robot.movec(CartesianPose)
            time.sleep(10)

            arduino.write(b'CLOSE\n')
            
            # time.sleep(0.5) # 等待 Arduino 执行
            while True:
                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').rstrip()
                    print("Arduino says:", data)
                    break
                else:
                    time.sleep(0.05)
                
            time.sleep(1)

            arduino.close()
            continue;
            
            # while True:
            #     task_status = robot.get_task_status()
            #     if task_status.get('type') is None:  # Check if the task has concluded
            #         print("MoveC operation completed.")
            #         break
            #     time.sleep(0.2)
            # angle = [0, 0, 0, 0, 0, 0, 10]
            # robot.movej(angle)

        elif(dir == "" or ord(dir) < ord('0') or ord(dir) > ord('3')): continue;
            
        while True:
            task_status = robot.get_task_status()
            if task_status.get('type') is None:  # Check if the task has concluded
                print("MoveC operation completed.")
                break
            time.sleep(0.2)
        
        dir = int(dir)
        movx, movy, movang = action[dir][1] * vec_x, action[dir][1] * vec_y, action[dir][0] * 10
        # errx, erry = 27 * math.cos((-yaw) * math.pi / 180) - 27 * math.cos((-yaw - movang) * math.pi / 180), 27 * math.sin((-yaw) * math.pi / 180) - 27 * math.sin((-yaw - movang) * math.pi / 180)
        pi = math.pi
        x = x - 27 * (math.cos((0-pre_yaw) * pi / 180) - math.cos((0-pre_yaw - movang) * pi / 180)) + movx
        y = y + movy - 27 * (math.sin((0-pre_yaw) * pi / 180) - math.sin((0-pre_yaw - movang) * pi / 180))
        z, roll, pitch, yaw = z, roll, pitch, yaw + movang
        print("x, y", x, y)
        # print("errx, erry", errx, erry)
        print(f"move x, y, yaw: {movx}, {movy}, {movang}")
        # CartesianPose = [x * 1000 + errx + movx, y * 1000 + movy + erry, z * 1000, roll, pitch, yaw + movang, 2]
        CartesianPose = [x, y, z, roll, pitch, yaw, 3]
        robot.movec(CartesianPose)
        time.sleep(3)
        
        end_status = robot.get_robot_status();
        end_x, end_y, end_z, end_roll, end_pitch, end_yaw = end_status['cartesianPosition']['x'], end_status['cartesianPosition']['y'], end_status['cartesianPosition']['z'], end_status['cartesianPosition']['roll'], end_status['cartesianPosition']['pitch'], end_status['cartesianPosition']['yaw'] 
        if(math.fabs(end_x - pre_x) < 5 / 1000 and math.fabs(end_y - pre_y) < 5 / 1000 and math.fabs(end_yaw - pre_yaw) < 3):
            print("error: can not reach")
            continue;
        else:
            l_act.append(dir)
        
        # nx, ny, nz, nr, np, nya = x * 1000 + errx + movx, y * 1000 + movy + erry, z * 1000, roll, pitch, yaw + movang
        # while True:
        #     end_status = robot.get_robot_status();
        #     # nx, ny, nz, nr, np, ny = x * 1000 + errx + movx, y * 1000 + movy + erry, z * 1000, roll, pitch, yaw + movang
        #     end_x, end_y, end_z, end_roll, end_pitch, end_yaw = end_status['cartesianPosition']['x'], end_status['cartesianPosition']['y'], end_status['cartesianPosition']['z'], end_status['cartesianPosition']['roll'], end_status['cartesianPosition']['pitch'], end_status['cartesianPosition']['yaw'] 
        #     # pre_x, pre_y, pre_z, pre_r, pre_p, pre_y = end_x, end_y, end_z, end_roll, end_pitch, end_yaw
        #     moverr_x, moverr_y, moverr_z, moverr_r, moverr_p, moverr_ya = nx - end_x * 1000, ny - end_y * 1000, nz - end_z * 1000, nr - end_roll, np - end_pitch, nya - end_yaw
        #     if(math.fabs(end_x * 1000 - nx) < 5 and math.fabs(end_y * 1000 - ny) < 5 and math.fabs(end_z * 1000 - nz) < 5 and math.fabs(end_roll - nr) < 3 and math.fabs(end_pitch - np) < 3 and math.fabs(end_yaw - nya) < 3):
        #         print("break!!!!!!")
        #         break
        #     else:
        #         print("error:", math.fabs(end_x * 1000 - nx), math.fabs(end_y * 1000 - ny), math.fabs(end_z * 1000 - nz), math.fabs(end_roll - nr), math.fabs(end_pitch - np), math.fabs(end_yaw - nya))
        #         print("nowy, goaly", end_y, ny)
        #     while True:
        #         task_status = robot.get_task_status()
        #         if task_status.get('type') is None:  # Check if the task has concluded
        #             print("MoveC operation completed.")
        #             break
        #         time.sleep(0.2)
        #     CartesianPose = [end_x * 1000 + moverr_x, end_y * 1000 + moverr_y, end_z * 1000 + moverr_z, end_roll + moverr_r, end_pitch + moverr_p, end_yaw + moverr_ya, 2]
        #     robot.movec(CartesianPose)
        #     time.sleep(2)

        
        # CartesianPose = [x * 1000 + errx + movx, y * 1000 + movy + erry, z * 1000, roll, pitch, yaw + movang, 5]
        # print("x, y", x * 1000, y * 1000)
        # print("errx, erry", errx, erry)
        # print(f"move x, y, yaw: {movx}, {movy}, {movang}")
        # robot.movec(CartesianPose)
        # time.sleep(5)

        # end_status = robot.get_robot_status();
        # end_x, end_y, end_yaw = end_status['cartesianPosition']['x'], end_status['cartesianPosition']['y'], end_status['cartesianPosition']['yaw'] 
        # if(math.fabs(end_x - pre_x) < 5 / 1000 and math.fabs(end_y - pre_y) < 5 / 1000 and math.fabs(end_yaw - pre_yaw) < 3):
        #     print("error: can not reach")
        # else:
        #     l_act.append(dir)

        # l_act.append(dir)
    print("l_act: ", l_act)
    angle = [0, 0, 0, 0, 0, 0, 10]
    robot.movej(angle)
    # robot.disable()
    print("Robot is now disabled.")

if(__name__ == "__main__"):
    instruct()
