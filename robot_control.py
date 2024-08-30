import json
import time
from STR400_SDK.str400 import STR400
import math
import os

Pi = math.pi

def calculate_distance(x1, y1, z1, x2, y2, z2):
    """Calculate the Euclidean distance between two points in 3D space."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def vector_to_angle(vector_x, vector_y):
    """Convert a 2D vector to an angle in degrees."""
    angle = math.degrees(math.atan2(vector_y, vector_x))
    return angle if angle >= 0 else angle + 360

def find_closest_point_and_angle(x, y, z, x_mid, y_mid, step_x, step_y, base_angle, init_yaw):
    """Find the closest point and yaw angle to (x, y, z) from the points defined by (x_mid + n * step_x, y_mid + n * step_y, 0) for n in [-2, -1, 0, 1, 2], and yaw angle closest to init_yaw."""
    points = [(x_mid + n * step_x, y_mid + n * step_y, 0) for n in range(-4, 5)]
    distances = [calculate_distance(x, y, z, point[0], point[1], point[2]) for point in points]
    closest_point_index = distances.index(min(distances))
    closest_point = points[closest_point_index]

    # Generate yaw angles from -180 to 175 degrees relative to base_angle
    yaw_angles = [(base_angle + (i - 36) * 10) % 360 for i in range(36)]
    yaw_angles = [(angle if angle <= 180 else angle - 360) for angle in yaw_angles]

    # Normalize init_yaw to be within [0, 360)
    init_yaw = init_yaw % 360
    if init_yaw > 180:
        init_yaw -= 360

    # Find the closest yaw angle to init_yaw
    closest_yaw = min(yaw_angles, key=lambda angle: abs(angle - init_yaw))
    closest_yaw_index = yaw_angles.index(closest_yaw)

    return closest_point, closest_point_index, closest_yaw, closest_yaw_index

def robot_control():
    # Load pose values from JSON file using absolute path
    # json_file_path = 'D:\\Users\\TianHaoChen\\Desktop\\trainmodel-touch_pen\\object_location.json'
    json_file_path = 'object_location.json'
    with open(json_file_path, 'r') as file:
        pose_values = json.load(file)

    # Extract values from JSON
    pen_x = pose_values['pen']['x']
    pen_y = pose_values['pen']['y']
    pen_z = pose_values['pen']['z']
    roll = 180
    pitch = 0
    
    vector_x = pose_values['vector']['x']
    vector_y = pose_values['vector']['y']

    # Calculate step_x and step_y
    step_x = (3.375 / 5.25) * vector_x / 2
    step_y = (3.375 / 5.25) * vector_y / 2

    # Calculate base angle from the vector
    base_angle = -vector_to_angle(vector_x, vector_y)
    print("Base angle: " + str(base_angle))

    # Your current location (x, y, z)
    current_x = 0  # Replace with your current x-coordinate
    current_y = 0  # Replace with your current y-coordinate
    current_z = 777  # Replace with your current z-coordinate
    init_yaw = 0  # Replace with your current yaw angle
    print("Initial yaw: " + str(init_yaw))

    # Find the closest point and yaw angle
    closest_point, closest_point_index, closest_yaw, closest_yaw_index = find_closest_point_and_angle(current_x, current_y, current_z, pen_x, pen_y, step_x, step_y, base_angle, init_yaw)
    closest_x, closest_y, closest_z = closest_point

    # Initialize the robot with specified host and port
    robot = STR400(host='localhost', port=8080)

    # Activating the robot
    robot.enable()
    print("Robot successfully activated.")

    # Commanding the robot to move its joints to specified angles using MoveJ
    print("Initiating MoveJ to target angles [0, 0, 0, 0, 0, 0] with a duration of 6 seconds...")
    angles = [0, 0, 0, 0, 0, 0, 6]
    robot.movej(angles)

    # Brief pause to ensure the MoveJ command is processed
    time.sleep(0.5)

    # Monitoring task status and waiting for the completion of the MoveJ operation
    print("Monitoring task status until MoveJ operation is completed...")
    while True:
        task_status = robot.get_task_status()
        if task_status.get('type') is None:  # Check if the task has concluded
            print("MoveJ operation completed.")
            break
        time.sleep(0.2)

    # Pause to ensure full completion of the operation
    time.sleep(0.5)

    # Commanding the robot to move to the closest Cartesian pose using MoveC
    CartesianPose = [closest_x, closest_y, pen_z, roll, pitch, closest_yaw, 10]

    CartesianPose = [closest_x + 27 + 27 * (math.cos(-init_yaw * Pi / 180) - math.cos((-init_yaw + closest_yaw) * Pi / 180)) , 
                     closest_y + 27 * (math.sin(-init_yaw * Pi / 180) - math.sin((-init_yaw + closest_yaw) * Pi / 180)), 
                     pen_z, roll, pitch, closest_yaw, 10]
    robot.movec(CartesianPose)
    time.sleep(0.5)

    print("Monitoring task status until the MoveC operation is completed...")
    print(f"Approaching ({CartesianPose[0]}, {CartesianPose[1]}, {CartesianPose[2]}) with Point ID: {closest_point_index}, Yaw ID: {closest_yaw_index}, and Absolute Yaw: {closest_yaw}")
    while True:
        task_status = robot.get_task_status()
        if task_status.get('type') is None:  # Check if the task has concluded
            print("MoveC operation completed.")
            break
        time.sleep(0.2)

    # Pause to ensure full completion of the operation
    # time.sleep(5)

    # # Repeating MoveJ command to return to the initial joint angles
    # print("Initiating MoveJ back to initial angles [0, 0, 0, 0, 0, 0] with a duration of 6 seconds...")
    # angles = [0, 0, 0, 0, 0, 0, 6]
    # robot.movej(angles)

    # # Brief pause to allow processing of the MoveJ command
    # time.sleep(0.5)

    # # Monitoring task status for the completion of the MoveJ operation
    # print("Monitoring task status until MoveJ operation is completed...")
    # while True:
    #     task_status = robot.get_task_status()
    #     if task_status.get('type') is None:  # Check if the task has concluded
    #         print("MoveJ operation completed.")
    #         break
    #     time.sleep(0.2)

    # # Disabling the robot after all operations are completed
    # robot.disable()
    # print("Robot is now disabled.")
    return closest_yaw_index, closest_point_index 
    

if __name__ == "__main__":
    yaw, x = robot_control()
