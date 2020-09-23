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
import heapq

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
    frontier_q.put((0,0, start))
    done[start] = (0,0,start)

    while(frontier_q.empty() == False):
        current = frontier_q.get()
        neighbors = maze.getNeighbors(current[2][0], current[2][1])
        for i in neighbors:
            b_flag = 0
            if(maze.isObjective(i[0], i[1]) == True):
                done[i] = current
                ret_cur = i
                b_flag = 1
                break
            if(i not in done):
                f_distance = abs((maze.getObjectives())[0][0]-i[0]) + abs((maze.getObjectives())[0][1]-i[1]) + current[1] + 1
                frontier_q.put((f_distance, current[1]+1, i))
                done[i] = current
        if(b_flag):
            break
    if(not b_flag):
        ret_cur = start
    ret = []
    while (ret_cur != start):
        ret.insert(0,ret_cur)
        ret_cur = done[ret_cur][2]
    ret.insert(0,start)
    return ret

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    def f_heuristic(coord, remaining, edge_list):
        heuristic = 0
        temp =[]
        for ind in range(0,4):
            if remaining[ind] == 1:
                temp.append(edge_list[ind])

        position = coord

        while(temp):
            dist = 0
            flag = 1

            for e in temp:
                d = abs(e[0] - position[0]) + abs(e[1] - position[1])
                if(d < dist or flag == 1):
                    flag = 0
                    dist = d
                    rem = e
            position = rem
            heuristic += dist
            temp.remove(rem)

        return heuristic



    done = {}
    frontier_q = queue.PriorityQueue()

    edges = maze.getObjectives()
    start = maze.getStart()
    #initialize prev state of start as start
    h = f_heuristic(start, (1,1,1,1), edges)
    frontier_q.put((0,0, (start, (1,1,1,1))))
    done[(start,(1,1,1,1))] = (0,0, (start, (1,1,1,1)))

    while(frontier_q.empty() == False):
        current = frontier_q.get()
        b_flag = 0
        tuples = list(current[2][1])
        if(tuples[0] == 0 and tuples[1] == 0 and tuples[2] == 0 and tuples[3] == 0):
            ret_cur = current[2]
            b_flag = 1
            break

        neighbors = maze.getNeighbors(current[2][0][0], current[2][0][1])
        for i in neighbors:
            #if the neighbor is a target mark that target as visited before pushing the flags to the queue
            cur_tuples = tuples.copy()
            if(i in edges):
                # print(i)
                cur_tuples[edges.index(i)] = 0

            #check if i(neighbor) was already visited with the current flags
            if((i,tuple(cur_tuples)) not in done):
                h = f_heuristic(i, cur_tuples, edges)
                #set the f and g values and push the reamining states as well as the locations of the point
                f_distance = h + current[1] + 1
                frontier_q.put((f_distance, current[1] + 1, (i, tuple(cur_tuples))))
                #push the prev node into the done table
                done[(i, tuple(cur_tuples))] = current


    if(not b_flag):
        ret_cur = (start,(1,1,1,1))

    ret = []
    while(ret_cur != (start,(1,1,1,1))):
        ret.insert(0,ret_cur[0])
        ret_cur = done[ret_cur][2]

    ret.insert(0,start)
    return ret

def astar_multi(maze):

    def astar_helper(maze, start, goal):
        done = {}
        frontier_q = queue.PriorityQueue()

        frontier_q.put((0,0, start))
        done[start] = (0,0,start)

        while(frontier_q.empty() == False):
            current = frontier_q.get()
            neighbors = maze.getNeighbors(current[2][0], current[2][1])
            for i in neighbors:
                b_flag = 0
                if(i == goal):
                    done[i] = current
                    ret_cur = current[1] +1
                    b_flag = 1
                    break
                if(i not in done):
                    f_distance = abs(goal[0]-i[0]) + abs(goal[1]-i[1]) + current[1] + 1
                    frontier_q.put((f_distance, current[1]+1, i))
                    done[i] = current
            if(b_flag):
                break
        if(not b_flag):
            ret_cur = 0

        return ret_cur

    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    class nodeMST:
        def __init__(self):

            self.neighbors = list()
            heapq.heapify(self.neighbors)
            self.coord = (-1,-1)

        def __init__(self, coord_i):
            self.neighbors = list()
            heapq.heapify(self.neighbors)
            self.coord = coord_i
            return

    class MSTree:

        def __init__(self):
            self.nodes = []
            self.calculated_dist = {}
            return
        def createNodes(self, objectives):
            for i in objectives:
                self.nodes.append(nodeMST(i))
            return

        def setDistances(self, maze):
            for node in self.nodes:
                for i in self.nodes:
                    if(node != i):
                        heapq.heappush(node.neighbors, tuple(((astar_helper(maze, node.coord, i.coord)), i.coord, i)))
            return

        def getNode(self, coord):
            for i in self.nodes:
                if(node.coor == coord):
                    return node
            return nodeMST()

        def calculateMST(self, objectivesLeft):
            if(objectivesLeft in self.calculated_dist):
                return self.calculated_dist[objectivesLeft]

            current_obj = []
            for i in self.nodes:
                if(i.coord in objectivesLeft):
                    print(i.coord)
                    current_obj.append(i)

            if(len(current_obj) == 1):
                return 0

            visited = []
            visited.append(current_obj[0])
            path_length = 0

            # print(visited)
            # print(current_obj)

            while(1):
                flag = 1
                prev_dist = 0
                for i in visited:
                    for ind in range(0,len(i.neighbors)):
                        if(i.neighbors[ind][2] in current_obj and (flag or (i.neighbors[ind][0] < prev_dist)) and i.neighbors[ind][2] not in visited):
                            flag = 0
                            prev_dist = i.neighbors[ind][0]
                            next_add = i.neighbors[ind][2]
                            break
                visited.append(next_add)
                path_length += prev_dist
                if(len(visited) == len(current_obj)):
                    break

            self.calculated_dist[objectivesLeft] = path_length
            return path_length

    def f_heuristic(coord, obj_tuple, MSTree):
        heuristic = 0
        temp =[]
        for ind in range(0,len(obj_tuple)):
            if obj_tuple[ind] != (-1,-1):
                temp.append(obj_tuple[ind])

        flag = 1
        dist = 0
        for i in temp:
            d = abs(coord[0]-i[0]) + abs(coord[1]-i[1])
            if(flag or d < dist):
                flag = 0
                dist = d

        return MSTree.calculateMST(obj_tuple) + dist

    def done_check(obj_tuple):
        ret = True
        for i in obj_tuple:
            if(i != (-1,-1)):
                ret = False
        return ret

    done = {}
    frontier_q = queue.PriorityQueue()

    edges = maze.getObjectives()
    start = maze.getStart()
    obj_tuple = tuple(edges)
    #init the MST
    mstTree = MSTree()
    mstTree.createNodes(obj_tuple)
    mstTree.setDistances(maze)


    #initialize prev state of start as start
    frontier_q.put((0,0, (start, obj_tuple)))
    done[(start, obj_tuple)] = (0,0, (start, obj_tuple))

    while(frontier_q.empty() == False):
        current = frontier_q.get()
        b_flag = 0
        tuples = list(current[2][1])
        if(done_check(tuples)):
            ret_cur = current[2]
            b_flag = 1
            break

        neighbors = maze.getNeighbors(current[2][0][0], current[2][0][1])
        for i in neighbors:
            #if the neighbor is a target mark that target as visited before pushing the flags to the queue
            cur_tuples = tuples.copy()
            if(i in edges):
                # print(i)
                cur_tuples[cur_tuples.index(i)] = (-1,-1)

            #check if i(neighbor) was already visited with the current flags
            if((i,tuple(cur_tuples)) not in done):
                h = f_heuristic(i, cur_tuples, mstTree)
                #set the f and g values and push the reamining states as well as the locations of the point
                f_distance = h + current[1] + 1
                frontier_q.put((f_distance, current[1] + 1, (i, tuple(cur_tuples))))
                #push the prev node into the done table
                done[(i, tuple(cur_tuples))] = current


    if(not b_flag):
        ret_cur = (start,obj_tuple)

    ret = []
    while(ret_cur != (start, obj_tuple)):
        ret.insert(0,ret_cur[0])
        ret_cur = done[ret_cur][2]

    ret.insert(0,start)
    return ret


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
