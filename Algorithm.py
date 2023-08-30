from CustomRegression import *

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
        m = -LineSegment(b1, b2).verticalSlope()
        k = b1.x ** 2 + b1.y ** 2 - b2.x ** 2 - b2.y ** 2 + eachPoint[1] ** 2 - eachPoint[0] ** 2
        intercept = -k / (2 * (b2.y - b1.y))
        n = intercept - b1.y
        a = 1 + m ** 2
        b = -2 * b1.x + 2 * m * n
        c = b1.x ** 2 + n ** 2 - eachPoint[0] ** 2
        xIntercepts = quadraticFormula(a, b, c)
        distances = []
        for xInt in xIntercepts:
            yInt = m * xInt + intercept
            distances.append(distanceToCircle(Point(xInt, yInt), b3, eachPoint[2]))
        if len(xIntercepts) == 0:
            positionData.append(Point(xIntercepts[0], m * xIntercepts[0] + intercept))
        elif distanceToCircle(Point(xIntercepts[0], m * xIntercepts[0] + intercept), b3, eachPoint[2]) < distanceToCircle(Point(xIntercepts[1], m * xIntercepts[1] + intercept), b3, eachPoint[2]):
            positionData.append(Point(xIntercepts[0], m * xIntercepts[0] + intercept))
        else:
            positionData.append(Point(xIntercepts[1], m * xIntercepts[1] + intercept))

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

def cleanPositionDataNoise(data, n):
    averagedPoints = []
    cleanedPoints = []
    for i in range(int(len(data)/n)):
        averageX, averageY = averageXY(data[n * i:n * (i + 1)])
        averagedPoints.append(Point(averageX, averageY))
    for i in range(len(averagedPoints) - 1):
        cleanedPoints.extend(extrapolatePoints(averagedPoints[i], averagedPoints[i+1], n))
    return cleanedPoints


def extrapolatePoints(p1, p2, n):
    points = [p1]
    stepX, stepY = (p1.x - p2.x)/n, (p1.y - p2.y)/n
    for i in range(n):
        points.append(Point((i + 1) * stepX + p1.x, (i + 1) * stepY + p1.y))
    return points

def distanceToCircle(p, circleCenter, r):
    return abs(LineSegment(p, circleCenter).length() - r)

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
    # Returns an empty dictionary if there is insufficient data
    if len(points) < 2:
        return dict()
    EPSILON = 0.5
    VERTICAL_LINE_THRESHOLD = 10
    copiedPoints = points.copy()
    # Finds the closest point to (0, 0)
    print(len(points))
    startingPoint = closestPointToP(Point(0, 0), copiedPoints)
    # Finds the closest point to the starting point
    closestPoint = closestPointToP(startingPoint, copiedPoints)
    groupedPoints = dict()
    groupedPoints.update({closestPoint:[closestPoint, closestPoint]})
    index = closestPoint
    startingPoint = closestPoint
    continueIterating = True
    while continueIterating:
        continueIterating = False
        # Finds the closest point to the initial point
        closestPoint = closestPointToP(startingPoint, copiedPoints)
        lineToPoint = LineSegment(startingPoint, closestPoint)
        # Checks if vertical line
        if abs(lineToPoint.slope()) > VERTICAL_LINE_THRESHOLD:
            # Measures slope deviation compared to slope of points in the group
            if abs(lineToPoint.verticalSlope()) < VERTICAL_LINE_THRESHOLD < abs(averageSlope(startingPoint, groupedPoints[index])):
                groupedPoints[index].append(closestPoint)
                if len(copiedPoints) > 1:
                    startingPoint = closestPoint
                    continueIterating = True
            # If point is outside deviation bounds, it creates a new group
            elif len(copiedPoints) > 2:
                nextClosestPoint = closestPointToP(closestPoint, copiedPoints)
                if absoluteDifference(LineSegment(nextClosestPoint, closestPoint).verticalSlope(), lineToPoint.verticalSlope()) > EPSILON:
                    groupedPoints[index].append(closestPoint)
                    startingPoint = closestPoint
                else:
                    groupedPoints.update({closestPoint: [closestPoint, nextClosestPoint]})
                    index, startingPoint = closestPoint, nextClosestPoint
                continueIterating = True
        else:
            if absoluteDifference(lineToPoint.slope(), averageSlope(startingPoint, groupedPoints[index])) < EPSILON:
                groupedPoints[index].append(closestPoint)
                if len(copiedPoints) > 1:
                    startingPoint = closestPoint
                    continueIterating = True
            elif len(copiedPoints) > 2:
                nextClosestPoint = closestPointToP(closestPoint, copiedPoints)
                if absoluteDifference(LineSegment(nextClosestPoint, closestPoint).slope(), lineToPoint.slope()) > EPSILON:
                    groupedPoints[index].append(closestPoint)
                    startingPoint = closestPoint
                else:
                    groupedPoints.update({closestPoint: [closestPoint, nextClosestPoint]})
                    index, startingPoint = closestPoint, nextClosestPoint
                continueIterating = True


        if abs(lineToPoint.slope()) > VERTICAL_LINE_THRESHOLD:
            # Measures slope deviation compared to sloe of points in the group
            if abs(lineToPoint.verticalSlope()) < VERTICAL_LINE_THRESHOLD < abs(averageSlope(startingPoint, groupedPoints[index])):
                groupedPoints[index].append(closestPoint)
                if len(copiedPoints) > 1:
                    startingPoint = closestPoint
                    continueIterating = True
            # If point is outside deviation bounds, it creates a new group
            elif len(copiedPoints) > 2:
                nextClosestPoint = closestPointToP(closestPoint, copiedPoints)
                groupedPoints.update({closestPoint: [closestPoint, nextClosestPoint]})
                index, startingPoint = closestPoint, nextClosestPoint
                continueIterating = True
        # Performs the same slope check except for non-vertical lines
        elif absoluteDifference(lineToPoint.slope(), averageSlope(startingPoint, groupedPoints[index])) < EPSILON:
            groupedPoints[index].append(closestPoint)
            if len(copiedPoints) > 1:
                startingPoint = closestPoint
                continueIterating = True
        elif len(copiedPoints) > 2:
            nextClosestPoint = closestPointToP(closestPoint, copiedPoints)
            groupedPoints.update({closestPoint: [closestPoint, nextClosestPoint]})
            index, startingPoint = closestPoint, nextClosestPoint
            continueIterating = True
    return groupedPoints

def averageGroupedPoints(groupedPoints):
    averagedGroup = dict()
    averagedPoints = []
    for eachGroup in groupedPoints:
        averagedGroup.update({eachGroup:[]})
        group = groupedPoints[eachGroup]
        for i in range(len(group) - 1):
#            averagedGroup[eachGroup].append(LineSegment(group[i], group[i + 1]).midPoint())
            averagedPoints.append(LineSegment(group[i], group[i + 1]).midPoint())
    return averagedPoints

def averageNonGroupedPoints(points):
    averagedPoints = []
    THRESHOLD = 75
    for i in range(len(points) - 1):
        ls = LineSegment(points[i], points[i + 1])
        if ls.length() < THRESHOLD:
            averagedPoints.append(ls.midPoint())
    return averagedPoints



def findClosestPoint(p, points, collection, index):
    EPSILON = 1
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
    points.remove(closestPoint)
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
        if len(groupedPoints[eachGroup]) > 4:
            groupedPoints[eachGroup].remove(firstPoint)
            groupedPoints[eachGroup].remove(secondPoint)
            firstPoint = furthestPointToP(groupedPoints[eachGroup][0], groupedPoints[eachGroup])
            secondPoint = furthestPointToP(firstPoint, groupedPoints[eachGroup])

        lines.append(LineSegment(firstPoint, secondPoint))

#    lines.clear()
#    slopeInterceptGroups = []
#    intersectionPoints = []
#    for eachGroup in groupedPoints:
#        slope, intercept, isVertical = leastSquaresRegression(groupedPoints[eachGroup])
#        slopeInterceptGroups.append((slope, intercept))
#    for i in range(len(slopeInterceptGroups) - 1):
#        firstLine = slopeInterceptGroups[i]
#        secondLine = slopeInterceptGroups[i + 1]
#        intersectionPoint = calculateLineIntersection(firstLine[0], firstLine[1], secondLine[0], secondLine[1])
#        intersectionPoints.append(intersectionPoint)
#        print(intersectionPoint.toString())
#    for i in range(len(intersectionPoints) - 1):
#        lines.append(LineSegment(intersectionPoints[i], intersectionPoints[i+1]))
    return lines



