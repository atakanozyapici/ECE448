import numpy as np
import utils
import random


class Agent:

    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        def transform(state):
            ret = [0] * 5
            ret[0] = state[0]/40
            ret[1] = state[1]/40

            temp = []
            for point in state[2]:
                temp.append((point[0]/40, point[1]/40))

            ret[2] = temp
            ret[3] = state[3]/40
            ret[4] = state[4]/40
            return ret

        def get_wall(x,y):
            retx = 0
            rety = 0

            if(x == 1):
                retx = 1
            elif(x == 12):
                retx = 2

            if(y == 1):
                rety = 1
            elif(y == 12):
                rety = 2

            return retx, rety

        def get_food_dir(head_x, head_y, food_x, food_y):
            if(head_x > food_x):
                retx = 1
            elif(head_x == food_x):
                retx = 0
            else:
                retx = 2

            if(head_y > food_y):
                rety = 1
            elif(head_y == food_y):
                rety = 0
            else:
                rety = 2

            return retx, rety

        def get_body_states(body_list, head_x, head_y):
            top = 0
            bottom = 0
            left = 0
            right = 0

            for body in body_list:
                if(body[0] == head_x and body[1] == head_y - 1):
                    top = 1
                elif(body[0] == head_x and body[1] == head_y + 1):
                    bottom = 1
                elif(body[0] == head_x - 1 and body[1] == head_y):
                    left = 1
                elif(body[0] == head_x + 1 and body[1] == head_y):
                    right = 1

            return top, bottom, left, right

        def explore_step(explore_dict, q_table, state, param):
            a = -1

            wall_x, wall_y = get_wall(state[0], state[1])
            food_dir_x, food_dir_y = get_food_dir(state[0], state[1], state[3], state[4])
            adj_top, adj_bot, adj_left, adj_right = get_body_states(state[2], state[0], state[1])

            for i in range(0,4):
                if(explore_dict[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, i] < param):
                    a = i

            if(a == -1):
                for i in range(0,4):
                    if(a == -1):
                        a = i
                        max = q_table[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, i]
                    else:
                        temp = q_table[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, i]
                        if(temp >= max):
                            max = temp
                            a = i

            return a


        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''

        # print(transform(state))
        state_T = transform(state)
        wall_x_bar, wall_y_bar = get_wall(state_T[0], state_T[1])
        food_dir_x_bar, food_dir_y_bar = get_food_dir(state_T[0], state_T[1], state_T[3], state_T[4])
        adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar = get_body_states(state_T[2], state_T[0], state_T[1])
        if(self._train):
            if(self.s != None and self.a != None):
                wall_x, wall_y = get_wall(self.s[0], self.s[1])
                food_dir_x, food_dir_y = get_food_dir(self.s[0], self.s[1], self.s[3], self.s[4])
                adj_top, adj_bot, adj_left, adj_right = get_body_states(self.s[2], self.s[0], self.s[1])
                #update q Table
                # print(points)
                if(dead):
                    reward = -1
                elif(self.points < points):
                    reward = 1
                    self.points = points
                else:
                    reward = -0.1


                alpha = self.C/(self.C + self.N[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, self.a])
                q = self.Q[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, self.a]

                a_bar = -1
                max = 0

                for i in range(0,4):
                    if(a_bar == -1):
                        a_bar = i
                        max = self.Q[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, i]
                    else:
                        temp = self.Q[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, i]
                        if(temp >= max):
                            max = temp
                            a = i

                q_bar = max


                val = q + alpha * (reward + self.gamma * q_bar - q)

                self.Q[wall_x, wall_y, food_dir_x, food_dir_y, adj_top, adj_bot, adj_left, adj_right, self.a] = val
                ret_action = explore_step(self.N,self.Q, state_T, self.Ne)
                if(not dead):
                    #update n table
                    self.N[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, ret_action] += 1
                elif dead:
                    self.reset()
            else:
                ret_action = explore_step(self.N,self.Q, state_T, self.Ne)
                self.N[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, ret_action] += 1



        else:
            a = -1
            for i in range(0,4):
                if(a == -1):
                    a = i
                    max = self.Q[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, i]
                else:
                    temp = self.Q[wall_x_bar, wall_y_bar, food_dir_x_bar, food_dir_y_bar, adj_top_bar, adj_bot_bar, adj_left_bar, adj_right_bar, i]
                    if(temp >= max):
                        max = temp
                        a = i
            ret_action = a

        self.s = state_T
        self.a = ret_action
        return ret_action
