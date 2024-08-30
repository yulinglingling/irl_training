import numpy as np
import matplotlib.pyplot as plt
import argparse
from collections import namedtuple

import img_utils_3d
import img_utils
from mdp import gridworld_3d
from mdp import value_iteration
from maxent_irl import *
from utils import *
# from lp_irl import *

Step = namedtuple('Step', 'cur_state action next_state reward done')

PARSER = argparse.ArgumentParser(description=None)
PARSER.add_argument('-hei', '--height', default=5, type=int, help='height of the gridworld')
PARSER.add_argument('-wid', '--width', default=5, type=int, help='width of the gridworld')
PARSER.add_argument('-dep', '--depth', default=5, type=int, help='depth of the gridworld')  # Added depth argument
PARSER.add_argument('-g', '--gamma', default=0.95, type=float, help='discount factor')
PARSER.add_argument('-a', '--act_random', default=0.7, type=float, help='probability of acting randomly')
PARSER.add_argument('-t', '--n_trajs', default=200, type=int, help='number of expert trajectories')
PARSER.add_argument('-l', '--l_traj', default=20, type=int, help='length of expert trajectory')
PARSER.add_argument('--rand_start', dest='rand_start', action='store_true', help='when sampling trajectories, randomly pick start positions')
PARSER.add_argument('--no-rand_start', dest='rand_start', action='store_false', help='when sampling trajectories, fix start positions')
PARSER.set_defaults(rand_start=True)
PARSER.add_argument('-lr', '--learning_rate', default=0.02, type=float, help='learning rate')
PARSER.add_argument('-ni', '--n_iters', default=20, type=int, help='number of iterations')
ARGS = PARSER.parse_args()
print(ARGS)

GAMMA = ARGS.gamma
ACT_RAND = ARGS.act_random
R_MAX = 1  # the constant r_max does not affect much the recoverred reward distribution
y_dis = ARGS.height
x_dis = ARGS.width
z_dis = ARGS.depth  # Added depth variable
N_TRAJS = ARGS.n_trajs
L_TRAJ = ARGS.l_traj
RAND_START = ARGS.rand_start
LEARNING_RATE = ARGS.learning_rate
N_ITERS = ARGS.n_iters

def generate_demonstrations(gw, policy, n_trajs=100, len_traj=20, rand_start=False, start_pos=[0,0,0]):
    """gatheres expert demonstrations

    inputs:
    gw          Gridworld - the environment
    policy      Nx1 matrix
    n_trajs     int - number of trajectories to generate
    rand_start  bool - randomly picking start position or not
    start_pos   3x1 list - set start position, default [0,0,0]
    returns:
    trajs       a list of trajectories - each element in the list is a list of Steps representing an episode
    """

    trajs = []
    for i in range(n_trajs):
        if rand_start:
            # override start_pos
            start_pos = [np.random.randint(0, gw.z_distance), np.random.randint(0, gw.y_distance), np.random.randint(0, gw.x_distance)]

        episode = []
        gw.reset(start_pos)
        cur_state = start_pos
        cur_state, action, next_state, reward, is_done = gw.step(int(policy[gw.pos_3Dto1D(cur_state)]))
        episode.append(Step(cur_state=gw.pos_3Dto1D(cur_state), action=action, next_state=gw.pos_3Dto1D(next_state), reward=reward, done=is_done))
        # while not is_done:
        for _ in range(len_traj):
            cur_state, action, next_state, reward, is_done = gw.step(int(policy[gw.pos_3Dto1D(cur_state)]))
            episode.append(Step(cur_state=gw.pos_3Dto1D(cur_state), action=action, next_state=gw.pos_3Dto1D(next_state), reward=reward, done=is_done))
            if is_done:
                break
        trajs.append(episode)
    return trajs

def main():
    N_STATES = x_dis * y_dis * z_dis  # Updated for 3D

    rmap_gt = np.zeros([z_dis, y_dis, x_dis])
    # rmap_gt[H-2, W-2, D-2] = R_MAX
    # rmap_gt[1, 1, 1] = R_MAX
    rmap_gt[4, :, :] = [
        [1000, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    # rmap_gt = np.array([
    #     [[1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0]],
    #     # Add similar layers for depth
    #     [[0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0]]
    # ], dtype=float)[:H, :W, :D]  # Truncate to H, W, D dimensions

    gw = gridworld_3d.GridWorld(rmap_gt, {}, 1 - ACT_RAND)
    # print("initial grid", gw.grid)

    rewards_gt = np.reshape(rmap_gt, (z_dis* y_dis* x_dis), order='F')
    rewards_init = rewards_gt
    P_a = gw.get_transition_mat()

    values_gt, policy_gt = value_iteration.value_iteration(P_a, rewards_gt, GAMMA, error=0.01, deterministic=True)

    rewards_gt = normalize(values_gt)
    gw = gridworld_3d.GridWorld(np.reshape(rewards_gt, (z_dis, y_dis, x_dis), order='F'), {}, 1 - ACT_RAND)

    P_a = gw.get_transition_mat()
    values_gt, policy_gt = value_iteration.value_iteration(P_a, rewards_gt, GAMMA, error=0.01, deterministic=True)
    # print("qvalues", values_gt)

    feat_map = np.eye(N_STATES)

    trajs = generate_demonstrations(gw, policy_gt, n_trajs=N_TRAJS, len_traj=L_TRAJ, rand_start=RAND_START)
    # print("number of expert", len(trajs))
    # print("export step 1", trajs[0][0])
    # print("number export step", len(trajs[0]))
    # print('LP IRL training ..')
    # rewards_lpirl = lp_irl(P_a, policy_gt, gamma=0.3, l1=10, R_max=R_MAX)
    print('Max Ent IRL training ..')
    rewards_maxent = maxent_irl(feat_map, P_a, GAMMA, trajs, LEARNING_RATE*2, N_ITERS*2)
    print("reward: ", rewards_maxent[:25])
    # plots
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    # plt.subplot(1, 2, 1)
    img_utils_3d.heatmap3d(ax1, np.reshape(rewards_gt, (z_dis, y_dis, x_dis), order='F'), 'Rewards Map - Ground Truth')  # Update to 3D heatmap
    # plt.subplot(1, 4, 2)
    # img_utils.heatmap3d(np.reshape(rewards_lpirl, (z_dis, y_dis, x_dis), order='F'), 'Reward Map - LP', block=False)  # Update to 3D heatmap
    ax3 = fig.add_subplot(1, 2, 2, projection='3d')
    # plt.subplot(1, 2, 1)
    img_utils_3d.heatmap3d(ax3, np.reshape(rewards_maxent, (z_dis, y_dis, x_dis), order='F'), 'Reward Map - Maxent')  # Update to 3D heatmap
    # plt.subplot(1, 4, 4)
    # img_utils.heatmap3d(np.reshape(rewards, (H, W, D), order='F'), 'Reward Map - Deep Maxent', block=False)  # Update to 3D heatmap
    plt.show()

if __name__ == "__main__":
    main()
