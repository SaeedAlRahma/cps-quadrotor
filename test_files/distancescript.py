# take in triangle vertices
# find centroid
# calculate distance from each edge to centroid
# return as array [Triangle, (d of e0,1), (d of e1,2), (d of e2,0)]
#
# update UPPAAL model by hand?
import numpy
from numpy import ones,vstack
from numpy.linalg import lstsq
import math
import string

SPEED = 1
DROID_SIZE = 0.7
BC = "bc"
AC = "ac"
AB = "ab"
AB_INDEX = 0
BC_INDEX = 1
AC_INDEX = 2

NOISE1  = 0.218755358604
NOISE2  = 0.416135222849
NOISE3  = 0.575114018097
NOISE4  = 0.0565917003624
NOISE5  = 0.124517371433
NOISE6  = 0.910000809258
NOISE7  = 1.67250197011
NOISE8  = 0.515976111076
NOISE10 =  0.31362093354

STABLIZE_TIME = 2.86

# Creates line vals given two points
def getLine(x_i, y_i, x_f, y_f):
    points = [(x_i,y_i),(x_f,y_f)]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]
    #print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
    return m, c

# Returns distance of a point from a line
def lineDistance(a, c, x, y, b=-1):
    return abs(a*x + b*y + c)/math.sqrt(math.pow(a,2) +math.pow(b,2))

# Returns centroid of a triangle given each vertex
def centroid(ax, ay, bx, by, cx, cy):
    return ((ax + bx + cx)/3), ((ay + by + cy)/3)

def calcEdgeDistance(cenx, ceny, ax, ay, bx, by):
    m, c = getLine(ax, ay, bx, by)
    return lineDistance(m, c, cenx, ceny)

def triDistanceCalc(name, ax, ay, bx, by, cx, cy):
    cenx, ceny = centroid(ax, ay, bx, by, cx, cy)
    ab = calcEdgeDistance(cenx, ceny, ax, ay, bx, by)
    bc = calcEdgeDistance(cenx, ceny, bx, by, cx, cy)
    ca = calcEdgeDistance(cenx, ceny, cx, cy, ax, ay)
    return [name, (cenx, ceny), ab, bc, ca]

def getTimes(name, centroid, ab, bc, ca):
    return [name, ab/SPEED, bc/SPEED, ca/SPEED]

def safetyRadius(name, centroid, ab, bc, cb):
    return [name, centroid, min(ab, bc, cb)-DROID_SIZE]

def gazeboEnv(centroidDistArr, filename):
    gazeboArr = []
    for i in centroidDistArr:
        gazeboArr.append(safetyRadius(i[0],i[1],i[2],i[3],i[4]))
    dataFile = open(filename + "_gazebo_env", "w")
    for line in gazeboArr:
        dataFile.write("%s\n" % line)


def readTransitions(filename):
    transitions=[]
    datafile = open(filename, "r")
    for line in datafile:
        line2 = line.split()
        transitions.append([line2[0], line2[1],line2[2], line2[3]])

    return transitions

def calcTransitionLengthsTimes(transitions, dict):
    transitionLengths = []
    for line in transitions:
        newArr = []
        newArr.append(line[0])
        newArr.append(line[1])
        sum = 0
        for i in range(0, 2):
            if line[i+2] == (AB):
               sum +=dict[line[i]][AB_INDEX]
            else:
                if line[i+2] == (BC):
                    sum +=dict[line[i]][BC_INDEX]
                else:
                    if line[i + 2] ==(AC):
                        sum +=dict[line[i]][AC_INDEX]
        newArr.append(sum)
        transitionLengths.append(newArr)
    return transitionLengths

def printTimes(times, filename):
    dataFile = open(filename, "w")
    for i in times:
        for j in i:
            dataFile.write(str(j) +" ")
        dataFile.write("\n")
    dataFile.close()

def addnoise(dists):
    noisyDists = []
    for item in dists:
        if item <= 1.5: noisyDists.append(item + NOISE1)
        elif item <= 2.5: noisyDists.append(item + NOISE2)
        elif item <= 3.5: noisyDists.append(item + NOISE3)
        elif item <= 4.5: noisyDists.append(item + NOISE4)
        elif item <= 5.5: noisyDists.append(item + NOISE5)
        elif item <= 6.5: noisyDists.append(item + NOISE6)
        elif item <= 7.5: noisyDists.append(item + NOISE7)
        elif item <= 8.5: noisyDists.append(item + NOISE8)
        else: noisyDists.append(item + NOISE10)

def maxTimes(centroidArr):
    maxTimeArr = []
    for item in centroidArr:
        dists = addnoise(item[2:4])
        times = (dists/SPEED) + STABLIZE_TIME
        maxTimeArr.append(item[0], max[times])
    return maxTimeArr

def calcEnterTime(centroidArr):
    #[zone] [dist leaving ab    dist leaving bc     dist leaving ac]
    distanceArr = dict()
    for entry in centroidArr:
        #0 = zone, 2= ab, 3 = bc, 4 = ac
        ab = (entry[3] + entry[4]) / 2.0 + entry[2]
        bc = (entry[2] + entry[4]) / 2.0 + entry[3]
        ac = (entry[2] + entry[3]) / 2.0 + entry[4]
        distanceArr[entry[0]] = [ab, bc, ac]
        # print (distanceArr[entry[0]])
        #distance to edge in question + average of other two edges
    return distanceArr


# def main(filename):
    # Read in triangles formatted as [name, ax, ay, bx, by, cx, cy], store as array
filename = "enviro.txt"
dataFile = open(filename, "r")
inputArr = []
count = 0
for line in dataFile:
    if count>=15:
        break
    line = line.replace("[", "")
    line = line.replace(",", "")
    line = line.replace("]", "")
    inputArr.append(line)
    count += 1

centroidDistArr = []
for line in inputArr:
    i = line.split()
    centroidDistArr.append(triDistanceCalc(str(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6])))
print(centroidDistArr)
gazeboEnv(centroidDistArr, filename)
minTimes = []
for i in centroidDistArr:
    minTimes.append(getTimes(i[0], i[1], i[2], i[3], i[4]))

minFile = open(filename + "_minTimes", "w")
for mline in minTimes:
    minFile.write("%s\n" % mline)

distFile = open(filename + "_dists", "w")
for dline in centroidDistArr:
    distFile.write("%s\n" % dline)
#maxTimes = list(map (getTimes, list(map (maxTimes, distanceArr))))

#put in map
zoneDict = dict()
timeDict = dict()
for i in range(0, len(centroidDistArr)):
    zoneDict[centroidDistArr[i][0]] = [centroidDistArr[i][2], centroidDistArr[i][3], centroidDistArr[i][4]]
    timeDict[minTimes[i][0]] = [minTimes[i][1], minTimes[i][2], minTimes[i][3]]
transitions = readTransitions("Transitions.txt")
pathDistances = calcTransitionLengthsTimes(transitions, zoneDict)
pathTimes = calcTransitionLengthsTimes(transitions, timeDict)
printTimes(pathTimes, "TransitionTimes.txt")

zoneTimes = calcEnterTime(centroidDistArr)

datafile = open("TransitionThroughZone.txt", "w")
for i in zoneTimes:
    #myString = string.Formatter.format(" %.2f %.2f %.2f \n ", zoneTimes[i][0], zoneTimes[i][1], zoneTimes[i][2])
    yString = "%.2f %.2f %.2f" %(zoneTimes[i][0], zoneTimes[i][1], zoneTimes[i][2])
    datafile.write(str(i) +" "+ yString + "\n")
datafile.close()
