import sys
import numpy as np
from collections import defaultdict
import math
import queue

'''
Report reflexive vertices
'''
def findReflexiveVertices(polygons):
    vertices=[]

    # Your code goes here
    # You should return a list of (x,y) values as lists, i.e.
    # vertices = [[x1,y1],[x2,y2],...]

    # take 3 vertices at a time
    # (b.x - a.x) * (c.y - b.y)  -  (c.x - b.x) * (b.y - a.y) < 0
    # > 0 means it's less than 180 degrees
    # = 0 means it's a straight line

    for x in range(0,len(polygons)):
        for y in range(0,len(polygons[x])):
            if y == 0:
                if ((polygons[x][y][0] - polygons[x][len(polygons[x])-1][0]) * (polygons[x][y+1][1] - polygons[x][y][1]) - (polygons[x][y+1][0] - polygons[x][y][0]) * (polygons[x][y][1] - polygons[x][len(polygons[x])-1][1])) < 0:
                    vertices.append(polygons[x][y])
            elif y == len(polygons[x])-1:
                if ((polygons[x][y][0] - polygons[x][y-1][0]) * (polygons[x][0][1] - polygons[x][y][1]) - (polygons[x][0][0] - polygons[x][y][0]) * (polygons[x][y][1] - polygons[x][y-1][1])) < 0:
                    vertices.append(polygons[x][y])
            else:
                if ((polygons[x][y][0] - polygons[x][y-1][0]) * (polygons[x][y+1][1] - polygons[x][y][1]) - (polygons[x][y+1][0] - polygons[x][y][0]) * (polygons[x][y][1] - polygons[x][y-1][1])) < 0:
                    vertices.append(polygons[x][y])


    return vertices

'''
Compute the roadmap graph
'''
def computeSPRoadmap(polygons, reflexVertices):
    vertexMap = dict()
    adjacencyListMap = defaultdict(list)



    # Your code goes here
    # You should check for each pair of vertices whether the
    # edge between them should belong to the shortest path
    # roadmap.
    #
    # Your vertexMap should look like
    # {1: [5.2,6.7], 2: [9.2,2.3], ... }

    for x in range(0,len(reflexVertices)):
        vertexMap[x+1] = reflexVertices[x]

    # and your adjacencyListMap should look like
    # {1: [[2, 5.95], [3, 4.72]], 2: [[1, 5.95], [5,3.52]], ... }
    #
    # The vertex labels used here should start from 1

    point = []
    num = 0
    for i in range(0,len(reflexVertices)):
        for j in range(0,len(polygons)):
            if len(point) == 0:
                point = reflexVertices[i]
                num = i+1
            if i != len(reflexVertices)-1:
                if reflexVertices[i] in polygons[j] and reflexVertices[i+1] in polygons[j]:
                    if adjacencyListMap.get(i+1) == None:
                        adjacencyListMap[i+1].append([i+2,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)])
                    elif not [i+2,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(i+1):
                        adjacencyListMap[i+1].append([i+2,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)])
                    if adjacencyListMap.get(i+2) != None:
                        if not [i+1,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(i+2):
                            adjacencyListMap[i+2].append([i+1,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)])
                    else:
                        adjacencyListMap[i+2].append([i+1,math.sqrt((reflexVertices[i+1][0]-reflexVertices[i][0])**2 + (reflexVertices[i+1][1]-reflexVertices[i][1])**2)])
                elif reflexVertices[i] in polygons[j]:
                    if not [num,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(i+1):
                        adjacencyListMap[i+1].append([num,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])
                    if adjacencyListMap.get(num) != None:
                        if not [i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(num):
                            adjacencyListMap[num].append([i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])
                    else:
                        adjacencyListMap[num].append([i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])
                    num = i+2
                    point = reflexVertices[i+1]
            elif reflexVertices[i] in polygons[j]:
                if not [num,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(i+1):
                    adjacencyListMap[i+1].append([num,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])
                if adjacencyListMap.get(num) != None:
                    if not [i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(num):
                        adjacencyListMap[num].append([i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])
                else:
                    adjacencyListMap[num].append([i+1,math.sqrt((reflexVertices[num-1][0]-reflexVertices[i][0])**2 + (reflexVertices[num-1][1]-reflexVertices[i][1])**2)])


        #test for valid edges between reflex vertices from different polygons
        if i != len(reflexVertices)-1:
            for j in range(i+1,len(reflexVertices)):
                bool = False
                for k in range(0,len(polygons)):
                    bool2 = False
                    for a in range(0,len(polygons)):
                        if reflexVertices[i] in polygons[a] and reflexVertices[j] in polygons[a]:
                            bool2 = True
                            break
                    if bool2:
                        bool = True
                        break
                    for l in range(0,len(polygons[k])):
                        if l != len(polygons[k])-1 and (polygons[k][l] == reflexVertices[i] or polygons[k][l] == reflexVertices[j] or polygons[k][l+1] == reflexVertices[i] or polygons[k][l+1] == reflexVertices[j]):
                            continue
                        elif l == len(polygons[k])-1 and (polygons[k][l] == reflexVertices[i] or polygons[k][l] == reflexVertices[j] or polygons[k][0] == reflexVertices[i] or polygons[k][0] == reflexVertices[j]):
                            continue
                        x = 0
                        y = 0
                        if l != len(polygons[k])-1:
                            x, y = findIntersectingLines(reflexVertices[i][0],reflexVertices[i][1],reflexVertices[j][0],reflexVertices[j][1],polygons[k][l][0],polygons[k][l][1],polygons[k][l+1][0],polygons[k][l+1][1])
                        else:
                            x, y = findIntersectingLines(reflexVertices[i][0],reflexVertices[i][1],reflexVertices[j][0],reflexVertices[j][1],polygons[k][l][0],polygons[k][l][1],polygons[k][0][0],polygons[k][0][1])
                        if math.isclose(x,reflexVertices[i][0],abs_tol=0.01) or math.isclose(x,reflexVertices[j][0],abs_tol=0.01) or math.isclose(y,reflexVertices[i][1],abs_tol=0.01) or math.isclose(y,reflexVertices[j][1],abs_tol=0.01):
                            if (x == reflexVertices[i][0] and y == reflexVertices[i][1]) or (x == reflexVertices[j][0] and y == reflexVertices[j][1]):
                                bool = True
                                break
                        if x == sys.maxsize:
                            continue
                        if l != len(polygons[k])-1 and (((reflexVertices[i][0] <= x <= reflexVertices[j][0]) or (reflexVertices[i][0] >= x >= reflexVertices[j][0])) and ((reflexVertices[i][1] <= y <= reflexVertices[j][1]) or (reflexVertices[i][1] >= y >= reflexVertices[j][1])) and ((polygons[k][l][0] <= x <= polygons[k][l+1][0]) or (polygons[k][l][0] >= x >= polygons[k][l+1][0])) and ((polygons[k][l][1] <= y <= polygons[k][l+1][1]) or (polygons[k][l][1] >= y >= polygons[k][l+1][1]))):
                            bool = True
                            break
                        elif l == len(polygons[k])-1 and (((reflexVertices[i][0] <= x <= reflexVertices[j][0]) or (reflexVertices[i][0] >= x >= reflexVertices[j][0])) and ((reflexVertices[i][1] <= y <= reflexVertices[j][1]) or (reflexVertices[i][1] >= y >= reflexVertices[j][1])) and ((polygons[k][l][0] <= x <= polygons[k][0][0]) or (polygons[k][l][0] >= x >= polygons[k][0][0])) and ((polygons[k][l][1] <= y <= polygons[k][0][1]) or (polygons[k][l][1] >= y >= polygons[k][0][1]))):
                            bool = True
                            break
                    if bool:
                        break
                if not bool:
                    if not [j+1,math.sqrt((reflexVertices[j][0]-reflexVertices[i][0])**2 + (reflexVertices[j][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(i+1):
                        adjacencyListMap[i+1].append([j+1,math.sqrt((reflexVertices[j][0]-reflexVertices[i][0])**2 + (reflexVertices[j][1]-reflexVertices[i][1])**2)])
                        if adjacencyListMap.get(j+1) != None:
                            if not [i+1,math.sqrt((reflexVertices[j][0]-reflexVertices[i][0])**2 + (reflexVertices[j][1]-reflexVertices[i][1])**2)] in adjacencyListMap.get(j+1):
                                adjacencyListMap[j+1].append([i+1,math.sqrt((reflexVertices[j][0]-reflexVertices[i][0])**2 + (reflexVertices[j][1]-reflexVertices[i][1])**2)])
                        else:
                            adjacencyListMap[j+1].append([i+1,math.sqrt((reflexVertices[j][0]-reflexVertices[i][0])**2 + (reflexVertices[j][1]-reflexVertices[i][1])**2)])
    return vertexMap, adjacencyListMap

r=queue.PriorityQueue()

def add_to_queue_UC(node_id, parent_node_id, cost, path, initialize=False):
    if (initialize==True):
        while (not r.empty):
            r.get()
    r.put((cost,node_id,parent_node_id, path))
    return


def is_queue_empty_UC():
    if (r.empty()):
        return True
    else:
        return False

'''
UC pop from queue
'''
def pop_front_UC():
    (cost, node_id, parent_node_id, path) = (0, 0, 0, [])
    # Your code here
    node = r.get()
    (cost, node_id, parent_node_id, path) = (node[0],node[1], node[2], node[3])
    return (cost, node_id, parent_node_id, path)

'''
Perform uniform cost search
'''
def uniformCostSearch(adjListMap, start, goal):
    visited = set()
    q = queue.PriorityQueue()
    q.put((0, start, [start]))

    while not q.empty():
        f, current_node, path = q.get()
        visited.add(current_node)

        if current_node==goal:
            return path, f
        else:
            neighbors = []
            for x in adjListMap:
                for y in range(0, len(adjListMap.get(x))):
                    if(current_node == x):
                        neighbors.append([adjListMap.get(x)[y][0],adjListMap.get(x)[y][1]])

            for neighbor in neighbors:
                child = neighbor[0]
                if child not in visited:
                    q.put((f + neighbor[1], child, path + [child]))


    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.
    print(path)
    return path, pathLength

'''
Agument roadmap to include start and goal
'''
def updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2):
    updatedALMap = dict()
    startLabel = 0
    goalLabel = -1

    # Your code goes here. Note that for convenience, we
    # let start and goal have vertex labels 0 and -1,
    # respectively. Make sure you use these as your labels
    # for the start and goal vertices in the shortest path
    # roadmap. Note that what you do here is similar to
    # when you construct the roadmap.

    for i in range(-1,1):
        for j in range(0,len(vertexMap)):
            bool = False
            for k in range(0,len(polygons)):
                for l in range(0,len(polygons[k])):
                    if l != len(polygons[k])-1:
                        if vertexMap.get(j+1) == polygons[k][l] or vertexMap.get(j+1) == polygons[k][l+1]:
                            continue
                    else:
                        if vertexMap.get(j+1) == polygons[k][l] or vertexMap.get(j+1) == polygons[k][0]:
                            continue

                    x = 0
                    y = 0
                    if l != len(polygons[k])-1:
                        if i == 0:
                            x, y = findIntersectingLines(x1,y1,vertexMap.get(j+1)[0],vertexMap.get(j+1)[1],polygons[k][l][0],polygons[k][l][1],polygons[k][l+1][0],polygons[k][l+1][1])
                        else:
                            x, y = findIntersectingLines(x2,y2,vertexMap.get(j+1)[0],vertexMap.get(j+1)[1],polygons[k][l][0],polygons[k][l][1],polygons[k][l+1][0],polygons[k][l+1][1])
                    else:
                        if i == 0:
                            x, y = findIntersectingLines(x1,y1,vertexMap.get(j+1)[0],vertexMap.get(j+1)[1],polygons[k][l][0],polygons[k][l][1],polygons[k][0][0],polygons[k][0][1])
                        else:
                            x, y = findIntersectingLines(x2,y2,vertexMap.get(j+1)[0],vertexMap.get(j+1)[1],polygons[k][l][0],polygons[k][l][1],polygons[k][0][0],polygons[k][0][1])
                    #if j == 2:
                    #    print(k,l,",",k,l+1,",",x,y)
                    if i == 0:
                        if math.isclose(x,vertexMap.get(j+1)[0],abs_tol=0.01) or math.isclose(x,x1,abs_tol=0.01) or math.isclose(y,vertexMap.get(j+1)[1],abs_tol=0.01) or math.isclose(y,y1,abs_tol=0.01):
                            if (x == vertexMap.get(j+1)[0] and y == vertexMap.get(j+1)[1]) or (x == x1 and y == y1):
                                bool = True
                                break
                    else:
                        if math.isclose(x,vertexMap.get(j+1)[0],abs_tol=0.01) or math.isclose(x,x2,abs_tol=0.01) or math.isclose(y,vertexMap.get(j+1)[1],abs_tol=0.01) or math.isclose(y,y2,abs_tol=0.01):
                            if (x == vertexMap.get(j+1)[0] and y == vertexMap.get(j+1)[1]) or (x == x2 and y == y2):
                                bool = True
                                break
                    if x == sys.maxsize:
                        continue
                    if i == 0:
                        if l != len(polygons[k])-1 and (((vertexMap.get(j+1)[0] <= x <= x1) or (vertexMap.get(j+1)[0] >= x >= x1)) and ((vertexMap.get(j+1)[1] <= y <= y1) or (vertexMap.get(j+1)[1] >= y >=y1)) and ((polygons[k][l][0] <= x <= polygons[k][l+1][0]) or (polygons[k][l][0] >= x >= polygons[k][l+1][0])) and ((polygons[k][l][1] <= y <= polygons[k][l+1][1]) or (polygons[k][l][1] >= y >= polygons[k][l+1][1]))):
                            bool = True
                            break
                        elif l == len(polygons[k])-1 and (((vertexMap.get(j+1)[0] <= x <= x1) or (vertexMap.get(j+1)[0] >= x >= x1)) and ((vertexMap.get(j+1)[1] <= y <= y1) or (vertexMap.get(j+1)[1] >= y >= y1)) and ((polygons[k][l][0] <= x <= polygons[k][0][0]) or (polygons[k][l][0] >= x >= polygons[k][0][0])) and ((polygons[k][l][1] <= y <= polygons[k][0][1]) or (polygons[k][l][1] >= y >= polygons[k][0][1]))):
                            bool = True
                            break
                    else:
                        if l != len(polygons[k])-1 and (((vertexMap.get(j+1)[0] <= x <= x2) or (vertexMap.get(j+1)[0] >= x >= x2)) and ((vertexMap.get(j+1)[1] <= y <= y2) or (vertexMap.get(j+1)[1] >= y >=y2)) and ((polygons[k][l][0] <= x <= polygons[k][l+1][0]) or (polygons[k][l][0] >= x >= polygons[k][l+1][0])) and ((polygons[k][l][1] <= y <= polygons[k][l+1][1]) or (polygons[k][l][1] >= y >= polygons[k][l+1][1]))):
                            bool = True
                            break
                        elif l == len(polygons[k])-1 and (((vertexMap.get(j+1)[0] <= x <= x2) or (vertexMap.get(j+1)[0] >= x >= x2)) and ((vertexMap.get(j+1)[1] <= y <= y2) or (vertexMap.get(j+1)[1] >= y >= y2)) and ((polygons[k][l][0] <= x <= polygons[k][0][0]) or (polygons[k][l][0] >= x >= polygons[k][0][0])) and ((polygons[k][l][1] <= y <= polygons[k][0][1]) or (polygons[k][l][1] >= y >= polygons[k][0][1]))):
                            bool = True
                            break
                if bool:
                    break
            if not bool:
                if i == 0:
                    if not [0,math.sqrt((x1-vertexMap.get(j+1)[0])**2 + (y1-vertexMap.get(j+1)[1])**2)] in adjListMap.get(j+1):
                        adjListMap[j+1].append([0,math.sqrt((x1-vertexMap.get(j+1)[0])**2 + (y1-vertexMap.get(j+1)[1])**2)])
                        if adjListMap.get(0) != None:
                            if not [j+1,math.sqrt((x1-vertexMap.get(j+1)[0])**2 + (y1-vertexMap.get(j+1)[1])**2)] in adjListMap.get(0):
                                adjListMap[0].append([j+1,math.sqrt((x1-vertexMap.get(j+1)[0])**2 + (y1-vertexMap.get(j+1)[1])**2)])
                        else:
                            adjListMap[0].append([j+1,math.sqrt((x1-vertexMap.get(j+1)[0])**2 + (y1-vertexMap.get(j+1)[1])**2)])
                else:
                    if not [-1,math.sqrt((x2-vertexMap.get(j+1)[0])**2 + (y2-vertexMap.get(j+1)[1])**2)] in adjListMap.get(j+1):
                        adjListMap[j+1].append([-1,math.sqrt((x2-vertexMap.get(j+1)[0])**2 + (y2-vertexMap.get(j+1)[1])**2)])
                        if adjListMap.get(-1) != None:
                            if not [j+1,math.sqrt((x2-vertexMap.get(j+1)[0])**2 + (y2-vertexMap.get(j+1)[1])**2)] in adjListMap.get(-1):
                                adjListMap[-1].append([j+1,math.sqrt((x2-vertexMap.get(j+1)[0])**2 + (y2-vertexMap.get(j+1)[1])**2)])
                        else:
                            adjListMap[-1].append([j+1,math.sqrt((x2-vertexMap.get(j+1)[0])**2 + (y2-vertexMap.get(j+1)[1])**2)])

    updatedALMap = adjListMap

    return startLabel, goalLabel, updatedALMap

def findIntersectingLines(x1,y1,x2,y2, x3,y3,x4,y4):
    #line AB represeting as a1x + b1y = c1
    a1 = y2-y1
    b1 = x1-x2
    c1 = a1*x1 + b1*y1

    #line CD represeting as a1x + b1y = c1
    a2 = y4-y3
    b2 = x3-x4
    c2 = a2*x3 + b2*y3

    determinant = a1*b2 - a2*b1
    if(determinant==0):
        return (sys.maxsize, sys.maxsize)
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return (x,y)

    #If determinant = 0, lines are parralel, Otherwise will return the point of intersection

if __name__ == "__main__":
    # Retrive file name for input data
    if(len(sys.argv) < 6):
        print("Five arguments required: python spr.py [env-file] [x1] [y1] [x2] [y2]")
        exit()

    filename = sys.argv[1]
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])

    # Read data and parse polygons
    lines = [line.rstrip('\n') for line in open(filename)]
    polygons = []
    for line in range(0, len(lines)):
        xys = lines[line].split(';')
        polygon = []
        for p in range(0, len(xys)):
            polygon.append([float(i) for i in xys[p].split(',')])
        polygons.append(polygon)

    # Print out the data
    print("Pologonal obstacles:")
    for p in range(0, len(polygons)):
        print(str(polygons[p]))
    print("")

    # Compute reflex vertices
    reflexVertices = findReflexiveVertices(polygons)
    print("Reflexive vertices:")
    print(str(reflexVertices))
    print("")

    # Compute the roadmap
    vertexMap, adjListMap = computeSPRoadmap(polygons, reflexVertices)
    print("Vertex map:")
    print(str(vertexMap))
    print("")
    print("Base roadmap:")
    print(dict(adjListMap))
    print("")


    # Update roadmap
    start, goal, updatedALMap = updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2)
    print("Updated roadmap:")
    print(dict(updatedALMap))
    print("")

    # Search for a solution
    path, length = uniformCostSearch(updatedALMap, start, goal)
    print("Final path:")
    print(str(path))
    print("Final path length:" + str(length))
