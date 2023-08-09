from Math import *

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
