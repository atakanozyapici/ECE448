
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    #variables that will be used overall
    start = arm.getArmAngle()
    limit = arm.getArmLimit()
    base = arm.getBase()

    if(len(limit) == 3):
        three_arm = 1
    else:
        three_arm = 0;
    if(len(limit) == 2 or len(limit) == 3):
        two_arm = 1
    else:
        two_arm = 0;

    alpha_limit = limit[0]
    if(two_arm):
        beta_limit = limit[1]
        height = int((beta_limit[1] - beta_limit[0]) / granularity + 1)
    else:
        height = 1
        beta_limit = 0
    if(three_arm):
        gamma_limit = limit[2]
        z = int((gamma_limit[1] - gamma_limit[0]) / granularity + 1)
    else:
        gamma_limit = 0
        z = 1

    width = int((alpha_limit[1] - alpha_limit[0]) / granularity + 1)


    maze = np.array([[[SPACE_CHAR for k in range(z)] for i in range(height)]for j in range(width)])
    for a in range(0, width):
        real_a = idxToAngle([a],[alpha_limit[0]], granularity)[0]
        if(two_arm):
            arm.setArmAngle((real_a, beta_limit[0]))
        elif(three_arm):
            arm.setArmAngle((real_a, beta_limit[0], gamma_limit[0]))
        else:
            arm.setArmAngle([real_a])
        first_arm = arm.getArmPosDist()[0]
        arm_list_a = arm.getArmPos()[0]

        if(not isArmWithinWindow([arm_list_a] , window)):
            maze[a][:][:] = WALL_CHAR
            continue
        elif(doesArmTouchObjects([first_arm], obstacles)):
            maze[a][:][:] = WALL_CHAR
            continue
        elif(doesArmTouchObjects([first_arm], goals, isGoal=True)):
            if(three_arm or two_arm):
                maze[a][:][:] = WALL_CHAR
            elif(doesArmTipTouchGoals(arm_list_a[1], goals)):
                maze[a][:][:] = OBJECTIVE_CHAR
            else:
                maze[a][:][:] = WALL_CHAR
            continue
        if(two_arm or three_arm):
            for b in range(0, height):
                real_b = idxToAngle([b], [beta_limit[0]], granularity)[0]
                if(two_arm):
                    arm.setArmAngle((real_a, real_b))
                elif(three_arm):
                    arm.setArmAngle((real_a, real_b, gamma_limit[0]))
                arm_list = arm.getArmPos()[0:2]
                whole_arm = arm.getArmPosDist()[0:2]
                if(not isArmWithinWindow(arm_list, window)):
                    maze[a][b][:] = WALL_CHAR
                elif(doesArmTouchObjects(whole_arm, obstacles)):
                    maze[a][b][:] = WALL_CHAR
                elif(doesArmTouchObjects(whole_arm, goals, isGoal=True)):
                    if(three_arm):
                        maze[a][b][:] = WALL_CHAR
                    elif(doesArmTipTouchGoals(arm_list[1][1], goals)):
                        maze[a][b][:] = OBJECTIVE_CHAR
                    else:
                        maze[a][b][:] = WALL_CHAR
                if(three_arm):
                    for g in range(0, z):
                        real_g = idxToAngle([g], [gamma_limit[0]], granularity)[0]
                        arm.setArmAngle((real_a, real_b, real_g))
                        arm_list = arm.getArmPos()
                        whole_arm = arm.getArmPosDist()
                        if(not isArmWithinWindow(arm_list, window)):
                            maze[a][b][g] = WALL_CHAR
                        elif(doesArmTouchObjects(whole_arm, obstacles)):
                            maze[a][b][g] = WALL_CHAR
                        elif(doesArmTouchObjects(whole_arm, goals, isGoal=True)):
                            if(doesArmTipTouchGoals(arm_list[2][1], goals)):
                                maze[a][b][g] = OBJECTIVE_CHAR
                            else:
                                maze[a][b][g] = WALL_CHAR



    start_a = angleToIdx([start[0]], [alpha_limit[0]], granularity)[0]


    if(two_arm):
        start_b = angleToIdx([start[1]], [beta_limit[0]], granularity)[0]
        maze[start_a][start_b][0] = START_CHAR
        offset = [alpha_limit[0], beta_limit[0], 0]
    elif(three_arm):
        start_b = angleToIdx([start[1]], [beta_limit[0]], granularity)[0]
        start_g = angleToIdx([start[2]], [gamma_limit[0]], granularity)[0]
        maze[start_a][start_b][start_g] = START_CHAR
        offset = [alpha_limit[0], beta_limit[0], gamma_limit[0]]
    else:
        maze[start_a][0][0] = START_CHAR
        offset = tuple((alpha_limit[0], 0, 0))
    ret = Maze(maze, offset, granularity)
    return ret
