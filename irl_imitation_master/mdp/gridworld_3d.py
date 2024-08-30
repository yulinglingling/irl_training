import numpy as np
up = 0;
down = 1;
left = 2;
right = 3;
front = 4;
right = 5;
stay = 6;
class GridWorld(object):
    """
    Grid world environment
    """

    def __init__(self, grid, terminals, trans_prob=1):
        print("init")
        """
        input:
          grid        2-d list of the grid including the reward
          terminals   a set of all the terminal states
          trans_prob  transition probability when given a certain action
        """
        self.z_distance = len(grid) ##z
        self.y_distance = len(grid[0]) ##y
        self.x_distance = len(grid[0][0]) ##x
        self.n_states = self.x_distance * self.y_distance * self.z_distance
        for i in range(self.z_distance):
            for j in range(self.y_distance):
                for k in range(self.x_distance):
                    grid[i][j][k] = str(grid[i][j][k])

        self.terminals = terminals
        self.grid = grid
        self.neighbors = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 0)]
        self.actions = [0, 1, 2, 3, 4, 5, 6]
        self.n_actions = len(self.actions)
        # self.dirs = {0: 's', 1: 'r', 2: 'l', 3: 'd', 4: 'u'}
        self.dirs = {0: 'up', 1: 'down', 2: 'left', 3: 'right', 4: 'front', 5: 'back', 6: 'stay'}
        # self.action_nei = {0-up: (1, 0, 0), 1-down: (-1, 0, 0), 2-left: (0, 0, -1), 3-right:(0, 0, 1), 4-front: (0, -1, 0), 5-back: (0, 1, 0)}

        # If the mdp is deterministic, the transition probability of taken a certain action should be 1
        # otherwise < 1, the rest of the probability are equally spreaded onto
        # other neighboring states.
        self.trans_prob = trans_prob

    def show_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                print(self.grid[i][j])

    def get_grid(self):
        return self.grid

    def get_states(self):
        """
        returns
          a list of all states
        """
        # print("get states")
        ans = [];
        for i in range(self.z_distance):
            for j in range(self.y_distance):
                for k in range(self.x_distance):
                    if 'x' != self.grid[i][j][k]:
                        ans.append((i, j, k));
        return ans;


    def get_actions(self, state):
        """
        get all the actions that can be taken on the current state
        returns
          a list of actions
        """
        if self.grid[state[0]][state[1]] == 'x':
            return [stay]

        actions = []
        for i in range(len(self.actions) - 1): ##except stay actions
            move = self.neighbors[i] ##(z, y, x)
            a = self.actions[i] ##(0~6)
            next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2]) 
            if next_state[0] >= 0 and next_state[0] < self.z_distance and next_state[1] >= 0 and next_state[1] < self.y_distance and next_state[2] >= 0 and next_state[2] <= self.x_distance and self.grid[next_state[0]][next_state[1]][next_state[2]] != 'x':
                actions.append(a)
        return actions

    def __get_action_states(self, state):
        """
        get all the actions that can be taken on the current state
        returns
          a list of (action, state) pairs
        """
        a_s = []
        for i in range(len(self.actions)):
            move = self.neighbors[i]
            a = self.actions[i]
            next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])
            if next_state[0] >= 0 and next_state[0] < self.z_distance and next_state[1] >= 0 and next_state[1] < self.y_distance and next_state[2] >= 0 and next_state[2] < self.x_distance and self.grid[next_state[0]][next_state[1]][next_state[2]] != 'x':
                a_s.append((a, next_state))
        return a_s

    def get_reward_sas(self, state, action, state1):
        """
        args
          state     current state
          action    action
          state1    next state
        returns
          the reward on current state
        """
        if not self.grid[state[0]][state[1]][state[2]] == 'x':
            return float(self.grid[state[0]][state[1]][state[2]])
        else:
            return 0

    def get_reward(self, state):
        """
        returns
          the reward on current state
        """
        if not self.grid[state[0]][state[1]][state[2]] == 'x':
            return float(self.grid[state[0]][state[1]][state[2]])
        else:
            return 0

    def get_transition_states_and_probs(self, state, action):
        """
        get all the possible transition states and their probabilities with [action] on [state]
        args
          state     (y, x)
          action    int
        returns
          a list of (next_state, probability of next_state) pair
        """
        if self.is_terminal(tuple(state)):
            return [(tuple(state), 1)]

        if self.trans_prob == 1:
            move = self.neighbors[action]
            next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])
            if next_state[0] >= 0 and next_state[0] < self.z_distance and next_state[1] >= 0 and next_state[1] < self.y_distance and next_state[2] >= 0 and next_state[2] < self.x_distance and self.grid[next_state[0]][next_state[1]][next_state[2]] != 'x':
                return [(next_state, 1)]
            else:
                # if the state is invalid, stay in the current state
                return [(state, 1)]
        else:
            # [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
            mov_probs = np.zeros([self.n_actions])
            mov_probs[action] = self.trans_prob
            mov_probs += (1 - self.trans_prob) / self.n_actions

            for a in range(self.n_actions):
                move = self.neighbors[a]
                next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])
                if next_state[0] < 0 or next_state[0] >= self.z_distance or next_state[1] < 0 or next_state[1] >= self.y_distance or next_state[2] < 0 or next_state[2] >= self.x_distance or self.grid[int(next_state[0])][int(next_state[1])][int(next_state[2])] == 'x':
                    # if the move is invalid, accumulates the prob to the stay_state
                    mov_probs[stay] += mov_probs[a]
                    mov_probs[a] = 0
            res = []
            for a in range(self.n_actions):
                if mov_probs[a] != 0:
                    move = self.neighbors[a]
                    next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])
                    res.append((next_state, mov_probs[a]))
            return res

    def is_terminal(self, state):
        """
        returns
          True if the [state] is terminal
        """
        return tuple(state) in self.terminals

    ##############################################
    # Stateful Functions For Model-Free Learning #
    ##############################################

    def reset(self, start_pos):
        """
        Reset the gridworld for model-free learning. It assumes only 1 agent in the gridworld.
        args
          start_pos     (i,j) pair of the start location
        """
        self._cur_state = start_pos

    def get_current_state(self):
        return self._cur_state

    def step(self, action):
        """
        Step function for the agent to interact with gridworld
        args
          action        action taken by the agent
        returns
          current_state current state
          action        input action
          next_state    next_state
          reward        reward on the next state
          is_done       True/False - if the agent is already on the terminal states
        """
        if self.is_terminal(self._cur_state):
            self._is_done = True
            return self._cur_state, action, self._cur_state, self.get_reward(self._cur_state), True

        st_prob = self.get_transition_states_and_probs(self._cur_state, action)

        sampled_idx = np.random.choice(np.arange(0, len(st_prob)), p=[prob for st, prob in st_prob]) ##according probability of next_state, randomly choose one action, return number 0~6
        last_state = self._cur_state
        next_state = st_prob[sampled_idx][0]
        reward = self.get_reward(last_state)
        self._cur_state = next_state
        return last_state, action, next_state, reward, False

    # ###########################################
    # # Policy Evaluation for Model-free Agents #
    # ###########################################

    # def get_optimal_policy(self, agent):
    #     states = self.get_states()
    #     policy = {}
    #     for s in states:
    #         policy[s] = [(agent.get_optimal_action(s), 1)]
    #     return policy

    # def get_values(self, agent):
    #     states = self.get_states()
    #     values = {}
    #     for s in states:
    #         values[s] = agent.get_value(s)
    #     return values

    # def get_qvalues(self, agent):
    #     states = self.get_states()
    #     q_values = {}
    #     for s in states:
    #         for a in self.get_actions(s):
    #             q_values[(s, a)] = agent.get_qvalue(s, a)
    #     return q_values

    # ###################################
    # # For Display in the command line #
    # ###################################

    # def display_qvalue_grid(self, qvalues):
    #     print("==Display q-value grid==")

    #     qvalues_grid = np.empty((len(self.grid), len(self.grid[0])), dtype=object)
    #     for s in self.get_states():
    #         if self.grid[s[0]][s[1]] == 'x':
    #             qvalues_grid[s[0]][s[1]] = '-'
    #         else:
    #             tmp_str = ""
    #             for a in self.get_actions(s):
    #                 tmp_str += self.dirs[a] + f' {qvalues[(s, a)]:.2f} '
    #             qvalues_grid[s[0]][s[1]] = tmp_str

    #     row_format = '{:>40}' * (len(self.grid[0]))
    #     for row in qvalues_grid:
    #         print(row_format.format(*row))

    # def display_value_grid(self, values):
    #     """
    #     Prints a nice table of the values in grid
    #     """
    #     print("==Display value grid==")

    #     value_grid = np.zeros((len(self.grid), len(self.grid[0])))
    #     for k in values:
    #         value_grid[k[0]][k[1]] = float(values[k])

    #     row_format = '{:>20.4}' * (len(self.grid[0]))
    #     for row in value_grid:
    #         print(row_format.format(*row))

    # def display_policy_grid(self, policy):
    #     """
    #     prints a nice table of the policy in grid
    #     input:
    #       policy    a dictionary of the optimal policy {<state, action_dist>}
    #     """
    #     print("==Display policy grid==")

    #     policy_grid = np.empty((len(self.grid), len(self.grid[0])), dtype=object)
    #     for k in self.get_states():
    #         if self.is_terminal((k[0], k[1])) or self.grid[k[0]][k[1]] == 'x':
    #             policy_grid[k[0]][k[1]] = '-'
    #         else:
    #             policy_grid[k[0]][k[1]] = self.dirs[policy[(k[0], k[1])][0][0]]

    #     row_format = '{:>20}' * (len(self.grid[0]))
    #     for row in policy_grid:
    #         print(row_format.format(*row))

    #######################
    # Some util functions #
    #######################

    def get_transition_mat(self):
        """
        get transition dynamics of the gridworld

        return:
          P_a         NxNxN_ACTIONS transition probabilities matrix - 
                        P_a[s0, s1, a] is the transition prob of 
                        landing at state s1 when taking action 
                        a at state s0
        """
        N_STATES = self.x_distance * self.y_distance * self.z_distance;
        N_ACTIONS = len(self.actions)
        P_a = np.zeros((N_STATES, N_STATES, N_ACTIONS))
        for si in range(N_STATES):
            posi = self.pos_1Dto3D(si)
            for a in range(N_ACTIONS):
                probs = self.get_transition_states_and_probs(posi, a)

                for posj, prob in probs:
                    sj = self.pos_3Dto1D(posj)
                    # Prob of si to sj given action a
                    P_a[si, sj, a] = prob
        return P_a

    # def get_values_mat(self, values):
    #     """
    #     inputs:
    #       values: a dictionary {<state, value>}
    #     """
    #     shape = np.shape(self.grid)
    #     v_mat = np.zeros(shape)
    #     for i in range(shape[0]):
    #         for j in range(shape[1]):
    #             v_mat[i, j] = values[(i, j)]
    #     return v_mat

    def get_reward_mat(self):
        """
        Get reward matrix from gridworld
        """
        shape = np.shape(self.grid) ##(z_distance, y_distance, x_distance)
        r_mat = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    r_mat[i, j, k] = float(self.grid[i][j][k])
        return r_mat

    def pos_3Dto1D(self, pos):
        """
        input:
          column-major 2d position
        returns:
          1d index
        """
        # print(f"change {pos} to {pos[0] * (self.x_distance * self.y_distance) + pos[1] * self.x_distance + pos[2]}")
        return pos[0] * (self.x_distance * self.y_distance) + pos[1] * self.x_distance + pos[2];

    def pos_1Dto3D(self, idx):
        """
        input:
          1d idx
        returns:
          2d column-major position
        """
        z = idx // (self.x_distance * self.y_distance);
        y = idx % (self.x_distance * self.y_distance) // self.x_distance;
        x = idx % (self.x_distance * self.y_distance) % self.x_distance;
        # print(f'change {idx} to {(z, y, x)}')
        return (z, y, x)
