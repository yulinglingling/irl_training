# from irl_imitation_master import maxent_irl
# from irl_imitation_master import mdp
# from irl_imitation_master import demo_gridwrold3d
import numpy as np
from collections import namedtuple
import sys
import os
import matplotlib.pyplot as plt
import random
import math

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


dir = ['plus x', 'minus x', 'plus ang', 'minus ang', 'stay']
plusx, minusx, plusang, minusang, stay = 0, 1, 2, 3, 4
dir2 = ['stay', '']
y_distance, x_distance = 36, 9
terminals, START_POS = {}, [4, 4]
ACT_RAND, GAMMA, LEARN_RATE, N_ITERS, iter_err, RAND_START, step_len = 0.3, 0.97, 0.005, 30, 0.01, False, 20
Step = namedtuple('Step', 'cur_state action next_state reward done')
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

def random_act():
    l_act = []
    st_pos = []
    vmax = -1
    end_yaw, end_x = 18, 4

    for i in range(y_distance):
        for j in range(x_distance):
            start_yaw, start_x = i, j
            if(math.fabs(start_yaw - end_yaw) + math.fabs(start_x - end_x) > vmax): vmax = math.fabs(start_yaw - end_yaw) + math.fabs(start_x - end_x)
            
            for k in range(5):
                tmp = []
                st_pos.append((start_yaw, start_x))
                while(start_yaw != end_yaw or start_x != end_x): 
                    rand = 0
                    if(start_yaw == end_yaw): rand = 1;
                    elif(start_x == end_x): rand = 0
                    else: rand = random.randint(0, 1)
                    if(rand == 0):
                        if(start_yaw > end_yaw): 
                            tmp.append(minusang)
                            start_yaw -= 1;
                        else:
                            tmp.append(plusang);
                            start_yaw += 1;
                    else:
                        if(start_x > end_x): 
                            tmp.append(minusx)
                            start_x -= 1;
                        else:
                            tmp.append(plusx)
                            start_x += 1;
                l_act.append(tmp)
                             


    return st_pos, l_act, vmax
    
    


def generate_steps(gw, data, p_start):
    action = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    # data_split = data.split();
    temp_traj = [];
    cur_state = p_start
    for d in data:
        d = int(d)
        next_y, next_x = cur_state[0] + action[d][0], cur_state[1] + action[d][1]
        is_done = False
        terminal = list(terminals)
        # if(next_z == terminal[0][0] and next_y == terminal[0][1] and next_x == terminal[0][2]): is_done = True
        temp_traj.append(Step(cur_state = gw.pos2idx(cur_state), action = d, next_state = gw.pos2idx([next_y, next_x]), reward = 0, done = is_done))
        cur_state = [next_y, next_x]
    last_step = Step(temp_traj[-1].cur_state, temp_traj[-1].action, temp_traj[-1].next_state, temp_traj[-1].reward, True)
    temp_traj[-1] = last_step
    return temp_traj

def generate_trajs():
    N_STATES = y_distance * x_distance
    init_grid = np.zeros([y_distance, x_distance])
    gw = mdp.gridworld.GridWorld(init_grid, terminals, 1 - ACT_RAND)
    feat_map = np.eye(N_STATES)
    P_a = gw.get_transition_mat()
    trajs = []
    # act_inputs = [[0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
    # start_inputs = [[28, 0]]
    start_inputs, act_inputs, maxlen = random_act()
    for idx, act_input in enumerate(act_inputs):
        # data_list = input("input numbers: ").split()
        while(maxlen - len(act_input)):
            act_input.append(4)
        trajs.append(generate_steps(gw, act_input, start_inputs[idx]))
    # for traj in trajs:
    #     for step in traj:
    #         print(f"from {gw.idx2pos(step.cur_state)} move {dir[step.action]} to {gw.idx2pos(step.next_state)}")
  
    reward = maxent_irl.maxent_irl(feat_map, P_a, GAMMA, trajs, LEARN_RATE, N_ITERS)
    # print("final reward, check", list(reward), reward[111])

    _2, policy2 = mdp.value_iteration.value_iteration(P_a, reward, GAMMA, iter_err, False)
    _, policy = mdp.value_iteration.value_iteration(P_a, reward, GAMMA, iter_err, True)
    l_p = [];
    for p in policy2:
        l_p.append(list(p))
    print(l_p)
    print("value", _)
    print(list(policy))
    record(l_p, list(_), list(policy))


    irl_traj = demo.generate_demonstrations(gw, policy, 1, 25, RAND_START, START_POS)
    
    l_action = []

    fig = plt.figure(figsize=(20, 10))
    plt.subplot(2, 1, 1)
    img_utils.heatmap2d(np.reshape(_, (x_distance, y_distance), order='C'), 'Reward Map - Maxent', block=False)  # Update to 3D heatmap
    plt.subplot(2, 1, 2)
    img_utils.heatmap2d(np.reshape(policy, (x_distance, y_distance), order='C'), 'Reward Map - Maxent', block=False)  # Update to 3D heatmap
    plt.show()

    return l_action
    
    # print("traj", irl_traj)

if(__name__ == "__main__"):
    l = generate_trajs()