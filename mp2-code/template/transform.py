
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

    alpha_limit = limit[0]
    beta_limit = limit[1]
    width = int(alpha_limit[1] - alpha_limit[0]) / granularity + 1
    height = int(beta_limit[1] - beta_limit[0]) / granularity + 1
    maze = [width][height]
    for a in range(0, width):
        real_a = idxToAngle(a,alpha_limit[0], granularity)
        arm.setArmAngle(real_a, 0)
        first_arm = arm.getArmPosDist()[0]
        if(isArmWithinWindow((first_arm[0],first_arm[1]))):
            maze[a][:] = WALL_CHAR
            continue
        elif(doesArmTouchObjects(first_arm, obstacles)):
            maze[a][:] = WALL_CHAR
            continue
        elif(doesArmTouchObjects(first_arm, goals, isGoal=True)):
            maze[a][:] = WALL_CHAR
            continue
        for b in range(0, height):
            

    pass
