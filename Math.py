import math
import sys


class Point:
    def __init__(self, x, y):
        self.x = round(x, 5)
        self.y = round(y, 5)


class LineSegment:
    def __init__(self, p1, p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y

    def length(self):
        return math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2)

    def slope(self):
        if self.isVerticalLine():
            return sys.maxsize
        return (self.y1 - self.y2) / (self.x1 - self.x2)

    def verticalSlope(self):
        return (self.x1 - self.x2) / (self.y1 - self.y2)

    def intercept(self):
        return self.y1 - self.slope() * self.x1

    def isVerticalLine(self):
        return self.x1 == self.x2

    def maxX(self):
        return max(self.x1, self.x2)

    def maxY(self):
        return max(self.y1, self.y2)

    def minX(self):
        return min(self.x1, self.x2)

    def minY(self):
        return min(self.y1, self.y2)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.topLeft = Point(x, y)
        self.width = w
        self.height = h

    def insideRect(self, p):
        return (self.topLeft.x + self.width >= p.x >= self.topLeft.x) and (self.topLeft.y >= p.y >= self.topLeft.y - self.height)

# Basic Helper Functions
def quadraticFormula(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        return [(-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)]
def coordinatesToPoints(coordinates):
    points = []
    for eachCoordinate in coordinates:
        points.append(Point(eachCoordinate[0], eachCoordinate[1]))
    return points

# Intersection/Collision Logic
def calculateLineIntersection(m1, b1, m2, b2):
    if m1 == m2:
        return -1
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return Point(x, y)


def calculateSegmentIntersection(ls1, ls2):
    # Check if both lines are vertical
    if ls1.isVerticalLine() and ls2.isVerticalLine():
        return -1
    # First line is vertical
    if ls1.isVerticalLine():
        intersectionPoint = Point(ls1.x1, ls2.slope() * ls1.x1 + ls2.intercept())
    # Second line is vertical
    elif ls2.isVerticalLine():
        intersectionPoint = Point(ls2.x1, ls1.slope() * ls2.x1 + ls1.intercept())
    else:
        intersectionPoint = calculateLineIntersection(ls1.slope(), ls1.intercept(), ls2.slope(), ls2.intercept())
        if intersectionPoint == -1:
            return -1
    lowerBoundX = max(ls1.minX(), ls2.minX())
    lowerBoundY = max(ls1.minY(), ls2.minY())
    upperBoundX = min(ls1.maxX(), ls2.maxX())
    upperBoundY = min(ls1.maxY(), ls2.maxY())
    if upperBoundX >= intersectionPoint.x >= lowerBoundX and upperBoundY >= intersectionPoint.y >= lowerBoundY:
        return intersectionPoint
    else:
        return -1

def circleLineSegmentIntersection(circleCenter, radius, ls):
    if ls.isVerticalLine():  # Vertical Line
        if abs(circleCenter.x - ls.x1) < radius:
            yDistance = math.sqrt(radius ** 2 - (circleCenter.x - ls.x1) ** 2)
            if ls.maxY() >= circleCenter.y + yDistance >= ls.minY():
                return True
            elif ls.maxY() >= circleCenter.y - yDistance >= ls.minY():
                return True
        return False

    a = 1 + ls.slope() ** 2
    b = -2 * circleCenter.x + 2 * ls.slope() * (ls.intercept() - circleCenter.y)
    c = circleCenter.x ** 2 + (ls.intercept() - circleCenter.y) ** 2 - radius ** 2
    intersectionPointsX = quadraticFormula(a, b, c)
    if len(intersectionPointsX) == 0:
        return False
    for eachX in intersectionPointsX:
        if ls.maxX() >= eachX >= ls.minX():
            return True
    return False


def checkCollisions(circleCenter, radius, allObstacles):
    anyCollision = False
    for eachObstacle in allObstacles:
        for i in range(len(eachObstacle) - 1):
            if circleLineSegmentIntersection(circleCenter, radius, LineSegment(eachObstacle[i], eachObstacle[i + 1])):
                anyCollision = True
    return anyCollision
