# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    visited = {} #dictionary
    q = queue.Queue()
    start = maze.getStart()
    q.put(start)
    visited[start] = start

    while(q.empty() == False):
        current = q.get()
        neighbors = maze.getNeighbors(current[0], current[1])
        for i in neighbors:
            b_flag = 0
            if(maze.isObjective(i[0], i[1]) == True):
                visited[i] = current
                current = i
                b_flag = 1
                break
            if(i not in visited):
                q.put(i)
                visited[i] = current
        if(b_flag):
            break

    ret = []
    while (current != start):
        ret.insert(0,current)
        current = visited[current]
    ret.insert(0,start)
    return ret


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    done = {}
    frontier_q = queue.PriorityQueue()

    start = maze.getStart()
    frontier_q.put((0, start))
    done[start] = (0,start)
    prev = start

    while(frontier_q.empty() == False):
        current = frontier_q.get()
        neighbors = maze.getNeighbors(current[1][0], current[1][1])
        for i in neighbors:
            b_flag = 0
            if(maze.isObjective(i[0], i[1]) == True):
                done[i] = current
                ret_cur = i
                b_flag = 1
                break
            if(i not in done):
                prev = done[current[1]]
                if(prev != start):
                    prev_distance = prev[0] - abs((maze.getObjectives())[0][0]-prev[1][0]) - abs((maze.getObjectives())[0][1]-prev[1][1]) + 1
                else:
                    prev_distance = 1
                f_distance = abs((maze.getObjectives())[0][0]-current[1][0]) + abs((maze.getObjectives())[0][1]-current[1][1]) + prev_distance
                frontier_q.put((f_distance, i))
                done[i] = current
        if(b_flag):
            break
    if(not b_flag):
        ret_cur = start
    ret = []
    while (ret_cur != start):
        ret.insert(0,ret_cur)
        ret_cur = done[ret_cur][1]
    ret.insert(0,start)
    return ret

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
