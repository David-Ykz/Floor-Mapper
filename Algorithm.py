from Math import *

def removeDuplicatePoints(data):
    alreadyVisited = set()
    uniquePoints = []
    for eachPoint in data:
        if eachPoint.toString() not in alreadyVisited:
            uniquePoints.append(eachPoint)
            alreadyVisited.add(eachPoint.toString())
    return uniquePoints


def headingDistanceToPoints(p, data):
    previousHeading = 0
    obstaclePoint = Point(0, 0)
    allPoints = []
    positionData = []
    headingData = []
    for dataPoint in data:
        currentHeading, distanceToObstacle, currentlyMoving, averageVelocity = dataPoint[0], dataPoint[1], dataPoint[2], dataPoint[3]
        if currentlyMoving:
            if currentHeading != previousHeading:
                obstaclePoint = Point(p.x + (distanceToObstacle + averageVelocity) * math.cos(math.radians(currentHeading)), p.y + (distanceToObstacle + averageVelocity) * math.sin(math.radians(currentHeading)))
                previousHeading = currentHeading
                allPoints.append(obstaclePoint)
            deltaDistance = LineSegment(p, obstaclePoint).length() - distanceToObstacle
            p.x += deltaDistance * math.cos(math.radians(currentHeading))
            p.y += deltaDistance * math.sin(math.radians(currentHeading))
        elif currentHeading != previousHeading:
            obstaclePoint = Point(p.x + distanceToObstacle * math.cos(math.radians(currentHeading)), p.y + distanceToObstacle * math.sin(math.radians(currentHeading)))
            allPoints.append(obstaclePoint)
            previousHeading = currentHeading
        positionData.append(Point(p.x, p.y))
        headingData.append(currentHeading)
    allPoints = removeDuplicatePoints(allPoints)
    return allPoints, positionData, headingData

def triangulation(beaconCoordinates, data):
    EPSILON = 0.001
    positionData, headingData = [], []
    b1 = beaconCoordinates[0]
    b2 = beaconCoordinates[1]
    b3 = beaconCoordinates[2]
    for eachPoint in data:
        m = - LineSegment(b1, b2).verticalSlope()
        k = b1.x ** 2 + b1.y ** 2 - b2.x ** 2 - b2.y ** 2 + eachPoint[1] ** 2 - eachPoint[0] ** 2
        intercept = -k / (2 * (b2.y - b1.y))
        n = intercept - b1.y
        a = 1 + m ** 2
        b = -2 * b1.x + 2 * m * n
        c = b1.x ** 2 + n ** 2 - eachPoint[0] ** 2
        intercepts = quadraticFormula(a, b, c)
        for eachIntercept in intercepts:
            y = m * eachIntercept + intercept
            if (eachIntercept - b3.x) ** 2 + (y - b3.y) ** 2 - eachPoint[2] ** 2 < EPSILON:
                positionData.append(Point(eachIntercept, y))
    for i in range(len(positionData) - 1):
        deltaX, deltaY = positionData[i + 1].x - positionData[i].x, positionData[i + 1].y - positionData[i].y

        if deltaX == 0 and deltaY == 0:
            if len(headingData) == 0:
                angle = 0
            else:
                angle = math.radians(headingData[i - 1])
        elif deltaX == 0:
            if deltaY > 0:
                angle = math.pi / 2
            else:
                angle = 3 * math.pi / 2
        else:
            angle = math.atan(deltaY / deltaX)
            if deltaX < 0:
                angle += math.pi
#                angle = math.pi - angle
            elif deltaY < 0 < deltaX:
                pass
#                angle += math.pi
        headingData.append(math.degrees(angle))
    headingData.insert(0, headingData[0])

    return positionData, headingData

def computeCircleIntersectionsForPoints(points, r):
    intersectionsPerPoint = dict()
    for eachPoint in points:
        for otherPoint in points:
            if eachPoint != otherPoint and isCircleTouching(eachPoint, r, otherPoint, r):
                if eachPoint in intersectionsPerPoint:
                    intersectionsPerPoint[eachPoint].append(otherPoint)
                else:
                    intersectionsPerPoint.update({eachPoint:[otherPoint]})
    return intersectionsPerPoint

def filterPointsByNumIntersections(intersectionsPerPoint):
    RADIUS = 20
    VELOCITY = 5
    CUTOFF_THRESHOLD = 3
    filteredPoints = []
    for eachPoint in intersectionsPerPoint:
        if len(intersectionsPerPoint[eachPoint]) <= CUTOFF_THRESHOLD:
            filteredPoints.append(eachPoint)
    return filteredPoints

def filterPointsByForces(intersectionsPerPoint):
    filteredPoints = []
    threshold = 5
    for eachPoint in intersectionsPerPoint:
        deltaX, deltaY = 0, 0
        for otherPoints in intersectionsPerPoint[eachPoint]:
            deltaX += otherPoints.x - eachPoint.x
            deltaY += otherPoints.y - eachPoint.y
        if math.sqrt(deltaX ** 2 + deltaY ** 2) > threshold:
            filteredPoints.append(eachPoint)
    return filteredPoints

def partition(p, arr, low, high):
    pivot = arr[high]
    index = low - 1
    for eachPoint in range(low, high):
        if LineSegment(arr[eachPoint], p).length() <= LineSegment(pivot, p).length():
            index += 1
            (arr[index], arr[eachPoint]) = (arr[eachPoint], arr[index])
    (arr[index + 1], arr[high]) = (arr[high], arr[index + 1])
    return index + 1

def sortClosestPoints(p, arr, low, high): # Quicksort
    if low < high:
        partitionIndex = partition(p, arr, low, high)
        sortClosestPoints(p, arr, low, partitionIndex - 1)
        sortClosestPoints(p, arr, partitionIndex + 1, high)

def fitLineToData(points):
    if len(points) < 2:
        return dict()
    closestPoint = closestPointToP(Point(0, 0), points)
    copiedPoints = points.copy()
    copiedPoints.remove(closestPoint)
    nextClosestPoint = closestPointToP(closestPoint, copiedPoints)
    copiedPoints.remove(nextClosestPoint)
    pointsInLines = dict()
    pointsInLines.update({closestPoint:[closestPoint, nextClosestPoint]})
    findClosestPoint(nextClosestPoint, copiedPoints, pointsInLines, closestPoint)
    if len(pointsInLines[closestPoint]) < 3:
        pointsInLines.pop(closestPoint)
    return pointsInLines

def absoluteDifference(a, b):
    if a > b:
        return a - b
    else:
        return b - a

def averageSlope(p, arr):
    slopes = 0
    for q in arr:
        if p != q:
            slopes += LineSegment(p, q).slope()
    return slopes/(len(arr) - 1)

def findClosestPoint(p, points, collection, index):
    EPSILON = 0.1
    VERTICAL_LINE_THRESHOLD = 10
    closestPoint = closestPointToP(p, points)
    points.remove(closestPoint)
    lineToPoint = LineSegment(p, closestPoint)
    if abs(lineToPoint.slope()) > VERTICAL_LINE_THRESHOLD:
        if abs(lineToPoint.verticalSlope()) < VERTICAL_LINE_THRESHOLD < abs(averageSlope(p, collection[index])):
            collection[index].append(closestPoint)
            if len(points) > 1:
                findClosestPoint(closestPoint, points, collection, index)
        elif len(points) > 2:
            nextClosestPoint = closestPointToP(closestPoint, points)
            collection.update({closestPoint: [closestPoint, nextClosestPoint]})
            points.remove(nextClosestPoint)
            findClosestPoint(nextClosestPoint, points, collection, closestPoint)
    elif absoluteDifference(lineToPoint.slope(), averageSlope(p, collection[index])) < EPSILON:
        collection[index].append(closestPoint)
        if len(points) > 1:
            findClosestPoint(closestPoint, points, collection, index)
    elif len(points) > 2:
        nextClosestPoint = closestPointToP(closestPoint, points)
        collection.update({closestPoint: [closestPoint, nextClosestPoint]})
        points.remove(nextClosestPoint)
        findClosestPoint(nextClosestPoint, points, collection, closestPoint)

def closestPointToP(p, points):
    closestPoint = points[0]
    for eachPoint in points:
        if LineSegment(p, eachPoint).length() < LineSegment(p, closestPoint).length():
            closestPoint = eachPoint
    return closestPoint

def furthestPointToP(p, points):
    furthestPoint = points[0]
    for eachPoint in points:
        if LineSegment(p, eachPoint).length() > LineSegment(p, furthestPoint).length():
            furthestPoint = eachPoint
    return furthestPoint

def pointsToLines(groupedPoints):
    lines = []
    for eachGroup in groupedPoints:
        firstPoint = furthestPointToP(groupedPoints[eachGroup][0], groupedPoints[eachGroup])
        secondPoint = furthestPointToP(firstPoint, groupedPoints[eachGroup])
        lines.append(LineSegment(firstPoint, secondPoint))
    return lines
