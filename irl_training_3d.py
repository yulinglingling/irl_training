# from irl_imitation_master import maxent_irl
# from irl_imitation_master import mdp
# from irl_imitation_master import demo_gridwrold3d
import numpy as np
from collections import namedtuple
import sys
import os
import matplotlib.pyplot as plt

# 将子目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'irl_imitation_master')))
print("sys.path:", sys.path)

# 然后可以导入模块
# import mdp.gridworld3d as 
import maxent_irl
import mdp
import demo_gridworld3d
import img_utils_3d
from utils import *


dir = ['up', 'down', 'left', 'right', 'front', 'back', 'stay']
z_distance, y_distance, x_distance = 5, 5, 5
terminals, START_POS = {}, [0, 4, 4]
ACT_RAND, GAMMA, LEARN_RATE, N_ITERS, iter_err, RAND_START = 0.1, 0.95, 0.02, 6, 0.01, False
Step = namedtuple('Step', 'cur_state action next_state reward done')

def generate_steps(gw, data):
    action = [(1, 0, 0), (-1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0)]
    # data_split = data.split();
    temp_traj = [];
    cur_state = START_POS
    for d in data:
        d = int(d)
        next_z, next_y, next_x = cur_state[0] + action[d][0], cur_state[1] + action[d][1], cur_state[2] + action[d][2]
        is_done = False
        terminal = list(terminals)
        # if(next_z == terminal[0][0] and next_y == terminal[0][1] and next_x == terminal[0][2]): is_done = True
        temp_traj.append(Step(cur_state = gw.pos_3Dto1D(cur_state), action = d, next_state = gw.pos_3Dto1D([next_z, next_y, next_x]), reward = 0, done = is_done))
        cur_state = [next_z, next_y, next_x]
    last_step = Step(temp_traj[-1].cur_state, temp_traj[-1].action, temp_traj[-1].next_state, temp_traj[-1].reward, True)
    temp_traj[-1] = last_step
    return temp_traj

def generate_trajs():
    N_STATES = z_distance * y_distance * x_distance
    init_grid = np.zeros([z_distance, y_distance, x_distance])
    gw = mdp.gridworld_3d.GridWorld(init_grid, terminals, 1 - ACT_RAND)
    feat_map = np.eye(N_STATES)
    P_a = gw.get_transition_mat()
    data_list = input("input numbers: ").split()
    trajs = [generate_steps(gw, data_list)]
    print("traj = ", trajs)
    # trajs = [[Step(cur_state = gw.pos_3Dto1D([0, 0, 0]), action = 1, next_state=gw.pos_3Dto1D([1, 0, 0]), reward = 0, done = True)]]
    reward = maxent_irl.maxent_irl(feat_map, P_a, GAMMA, trajs, LEARN_RATE, N_ITERS)

    _, policy = mdp.value_iteration.value_iteration(P_a, reward, GAMMA, iter_err)
    irl_traj = demo_gridworld3d.generate_demonstrations(gw, policy, 1, 20, RAND_START, START_POS)
    for route in irl_traj:
        for step in route:
            print(f"move {dir[step.action]} to {gw.pos_1Dto3D(step.next_state)}")

    fig = plt.figure(figsize=(20, 10))
    ax3 = fig.add_subplot(1, 1, 1, projection='3d')
    # plt.subplot(1, 2, 1)
    img_utils_3d.heatmap3d(ax3, np.reshape(reward, (z_distance, y_distance, x_distance), order='F'), 'Reward Map - Maxent')  # Update to 3D heatmap
    plt.show()
    
    # print("traj", irl_traj)

if(__name__ == "__main__"):
    generate_trajs()