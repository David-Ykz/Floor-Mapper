from Math import *

def headingDistanceToPoints(p, data):
    previousHeading = 0
    obstaclePoint = Point(0, 0)
    allPoints = set()
    positionData = []
    headingData = []
    for dataPoint in data:
        currentHeading, distanceToObstacle, currentlyMoving, averageVelocity = dataPoint[0], dataPoint[1], dataPoint[2], dataPoint[3]
        if currentlyMoving:
            if currentHeading != previousHeading:
                obstaclePoint = Point(p.x + (distanceToObstacle + averageVelocity) * math.cos(math.radians(currentHeading)), p.y + (distanceToObstacle + averageVelocity) * math.sin(math.radians(currentHeading)))
                previousHeading = currentHeading
                allPoints.add(obstaclePoint)
            deltaDistance = LineSegment(p, obstaclePoint).length() - distanceToObstacle
            p.x += deltaDistance * math.cos(math.radians(currentHeading))
            p.y += deltaDistance * math.sin(math.radians(currentHeading))
        elif currentHeading != previousHeading:
            obstaclePoint = Point(p.x + distanceToObstacle * math.cos(math.radians(currentHeading)), p.y + distanceToObstacle * math.sin(math.radians(currentHeading)))
            allPoints.add(obstaclePoint)
            previousHeading = currentHeading
        positionData.append(Point(p.x, p.y))
        headingData.append(currentHeading)
    return allPoints, positionData, headingData

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

