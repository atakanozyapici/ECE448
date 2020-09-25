# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.
    """
    visited = {} #dictionary
    q = queue.Queue()
    start = maze.getStart()
    q.put(start)
    visited[start] = start

    while(q.empty() == False):
        current = q.get()
        neighbors = maze.getNeighbors(current[0], current[1], current[2])
        for i in neighbors:
            b_flag = 0
            if(maze.isObjective(i[0], i[1], i[2]) == True):
                visited[i] = current
                current = i
                b_flag = 1
                break
            if(i not in visited):
                q.put(i)
                visited[i] = current
        if(b_flag):
            break
    if(not b_flag):
        return None
    ret = []
    while (current != start):
        ret.insert(0,current)
        current = visited[current]
    ret.insert(0,start)
    return ret
