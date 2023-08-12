from Math import *
import random
import sys

def sortingCriteria(ls):
    return ls.length()


def headingDistanceToPoints(p, data):
    previousHeading = 0
    obstaclePoint = Point(0, 0)
    allPoints = set()
    positionData = []
    headingData = []
    for dataPoint in data:
        currentHeading = dataPoint[0]
        distanceToObstacle = dataPoint[1]
        currentlyMoving = dataPoint[2]
        averageVelocity = dataPoint[3]
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
    # Input data is a set of points (assume 1 shape), WILL NEED TO CLUSTER BEFORE USING
    # Returns a list of line segments
    # Pick point P closest to (0, 0)
    # Sort all other points based on distance to P
    # For each point Q closest to P not in set P, calculate the slope of PQ
    # If PQ is within bounds of slope P, add Q to set P
    # If not, set Q = P, and continue the algorithm

    closestPoint = points[0]
    for eachPoint in points:
        if LineSegment(eachPoint, Point(0, 0)).length() < LineSegment(closestPoint, Point(0, 0)).length():
            closestPoint = eachPoint

    sortedPoints = points.copy()
    sortedPoints.remove(closestPoint)
    sortClosestPoints(closestPoint, sortedPoints, 0, len(sortedPoints) - 1)
    pointsInLines = dict()
    pointsInLines.update({closestPoint:[closestPoint, sortedPoints[0]]})
    sortedPoints.remove(sortedPoints[0])
    checkNextClosestPoint(closestPoint, sortedPoints, pointsInLines, 0)

    return closestPoint, pointsInLines


def checkNextClosestPoint(p, sortedPoints, collection, index):
    EPSILON = 0.5
    closestPoint = sortedPoints[index]
    if closestPoint not in collection:
        if abs(LineSegment(p, closestPoint).slope() - averageSlope(p, collection[p])) < EPSILON:
            collection[p].append(closestPoint)
            sortedPoints.remove(closestPoint)
            if index < len(sortedPoints) - 1:
                checkNextClosestPoint(p, sortedPoints, collection, index)
        elif index < len(sortedPoints) - 2:
            sortedPoints.remove(closestPoint)
            sortClosestPoints(closestPoint, sortedPoints, 0, len(sortedPoints) - 1)
            collection.update({closestPoint:[closestPoint, sortedPoints[0]]})
            sortedPoints.remove(sortedPoints[0])
            checkNextClosestPoint(closestPoint, sortedPoints, collection, 0)
    elif index < len(sortedPoints) - 1: # May not need logic for this if removing from sortedPoints list
        checkNextClosestPoint(p, sortedPoints, collection, index + 1)

def averageSlope(p, arr):
    slopes = 0
    for q in arr:
        if p != q:
            slopes += LineSegment(p, q).slope()
    return slopes/(len(arr) - 1)








