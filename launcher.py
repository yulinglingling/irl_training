from capture_and_detection import capture_and_detection
from object_location import box_to_real_location
from robot_control import robot_control
import gather
# import best_traj
import grasp
import cv2
import segmentation
import time
import reflect
import quaternions
import numpy as np
import simulate
# from best_traj import generate_trajs

def launcher():
    # Executing the functions
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
        data = input("ready to continue? [y/exit] ");
        if(data == "exit"): break;
        ready = capture_and_detection(orbbec, brio)
        time.sleep(1)
        if(ready == False): 
            print("error: Failed to read image.")
            return 
        
        # print("Launching \"object_location.py\"")
        # vec_x, vec_y = box_to_real_location()
        orbbec_left, brio_mid, orbbec_mid, brio_right = segmentation.segmentation()

        origin, vec_to_top = reflect.point_and_vec(orbbec_left, brio_mid, orbbec_mid, brio_right)
        vec_to_top /= np.linalg.norm(np.array(vec_to_top))
        print("origin, vector", origin, vec_to_top);
        
        claw_target_vec = -1 * np.array(vec_to_top)
        quat = quaternions.vector_to_quaternion(claw_target_vec)
        roll, pitch, yaw = quaternions.quaternion_to_euler_angles(quat)
        print("rpy", roll, pitch, yaw)
        print("Launching \"simulate grasp pen\"")
        simulate.simulate(origin, (roll, pitch, yaw), vec_to_top)
        # grasp.grasp(origin[0] * 10, origin[1] * 10, origin[2] * 10, roll, pitch, yaw)

        # # generate_trajs()
        # print("Launching \"robot_control.py\"")
        # start_yaw, start_x = robot_control()

        # print("Launching \" generate best traj\"")
        # end_yaw, end_x = best_traj.best_traj(start_yaw, start_x)

    
    orbbec.release()
    brio.release()

    # gather.instruct(vec_x, vec_y)

if __name__ == "__main__":
    launcher()