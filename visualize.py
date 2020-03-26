import sys

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import spr as spr

'''
Set up matplotlib to create a plot with an empty square
'''
def setupPlot():
    fig = plt.figure(num=None, dpi=120, facecolor='w', edgecolor='k')
    ax = plt.axes()
    ax.set_axisbelow(True)
    ax.grid(which='minor', linestyle=':', alpha=0.2)
    ax.grid(which='major', linestyle=':', alpha=0.5)
    return fig, ax

'''
Make a patch for a single pology
'''
def createPolygonPatch(polygon):
    verts = []
    codes= []
    for v in range(0, len(polygon)):
        xy = polygon[v]
        verts.append((xy[0], xy[1]))
        if v == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch

'''
Make a patch for the robot
'''
def createPolygonPatchForRobot(polygon):
    verts = []
    codes= []
    for v in range(0, len(polygon)):
        xy = polygon[v]
        verts.append((xy[0], xy[1]))
        if v == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch


'''
Render polygon obstacles
'''
def drawPolygons(polygons, fig, ax):
    for p in range(0, len(polygons)):
        patch = createPolygonPatch(polygons[p])
        ax.add_patch(patch)


def plot(roadmap, computed, vertexMap):
    print(roadmap)

    x =[]
    y =[]
    for i in roadmap:
        startX = vertexMap.get(i)[0]
        startY = vertexMap.get(i)[1]
        print(i, vertexMap.get(i)[0],vertexMap.get(i)[1])
        print()
        for j in roadmap.get(i):
            endX = vertexMap.get(j[0])[0]
            endY = vertexMap.get(j[0])[1]
            print(endX, endY)
            x.append((startX, endX))
            y.append((startY, endY))
            plt.plot(x,y, 'g-' , marker="o", ms=5, label="roadmap")
            #plt.plot(x[i:i+2], y[i:i+2], 'ro-')


    for y in computed:
        #computedX.append(y[0])
        #computedY.append(y[1])
        print()
    #plt.plot(computedX, computedY, color="red", marker="o", ms=5, label="computed")
    plt.show()
    return

if __name__ == "__main__":

    # Retrive file name for input data
    if(len(sys.argv) < 6):
        print("Please provide input tfile: python visualize.py [env-file] x1 y1 x2 y2")
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

    # Setup
    fig, ax = setupPlot()

    # Draw the polygons
    drawPolygons(polygons, fig, ax)

    # Extra visualization elements goes here
    # ===== delete the following line before you make some changes =====
    ax.plot()

    reflexVertices = spr.findReflexiveVertices(polygons)
    print("Reflexive vertices:")
    print(str(reflexVertices))
    print("")

    # Compute the roadmap
    vertexMap, adjListMap = spr.computeSPRoadmap(polygons, reflexVertices)
    print("Vertex map:")
    print(str(vertexMap))
    print("")
    print("Base roadmap:")
    print(dict(adjListMap))
    print("")

    start, goal, updatedALMap = updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2)
    print("Updated roadmap:")
    print(dict(updatedALMap))
    print("")

    # Search for a solution
    path, length = uniformCostSearch(updatedALMap, start, goal)
    print("Final path:")
    print(str(path))
    print("Final path length:" + str(length))

    plot(adjListMap, []], vertexMap)
    # ======= delete the above line before you make some changes =======

    plt.show()
