import math
import pygame

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
def calculateSlope(segment):
    return (segment[3] - segment[1]) / (segment[2] - segment[0])
def calculateIntercept(segment):
    return segment[1] - calculateSlope(segment) * segment[0]
def quadraticFormula(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        return [(-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)]

def drawCircle(color, x, y, r):
    pygame.draw.circle(screen, color, (x, SCREEN_HEIGHT - y), r)
def drawRectangle(color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - y, w, h))
def drawTransparentRectangle(color, x, y, w, h, t):
    pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - y, w, h), t)
def drawLine(color, x1, y1, x2, y2):
    pygame.draw.line(screen, color, (x1, SCREEN_HEIGHT - y1), (x2, SCREEN_HEIGHT - y2))
def writeText(color, text, size, x, y):
    font = pygame.font.SysFont("arial", size).render(text, True, color)
    screen.blit(font, (x, SCREEN_HEIGHT - y))

def calculateLineIntersection(m1, b1, m2, b2):
    if m1 == m2:
        return -1
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return round(x, 4), round(y, 4)
def calculateSegmentIntersection(segment1, segment2):
    # Check if both lines are vertical
    if segment1[0] == segment1[2] and segment2[0] == segment2[2]:
        return -1
    # First line is vertical
    if segment1[0] == segment1[2]:
        intersectionPoint = (segment1[0], calculateSlope(segment2) * segment1[0] + calculateIntercept(segment2))
    # Second line is vertical
    elif segment2[0] == segment2[2]:
        intersectionPoint = (segment2[0], calculateSlope(segment1) * segment2[0] + calculateIntercept(segment1))
    else:
        intersectionPoint = calculateLineIntersection(calculateSlope(segment1), calculateIntercept(segment1), calculateSlope(segment2), calculateIntercept(segment2))
        if intersectionPoint == -1:
            return -1
    lowerBoundX = max(min(segment1[0], segment1[2]), min(segment2[0], segment2[2]))
    lowerBoundY = max(min(segment1[1], segment1[3]), min(segment2[1], segment2[3]))
    upperBoundX = min(max(segment1[0], segment1[2]), max(segment2[0], segment2[2]))
    upperBoundY = min(max(segment1[1], segment1[3]), max(segment2[1], segment2[3]))
    if upperBoundX >= intersectionPoint[0] >= lowerBoundX and upperBoundY >= intersectionPoint[1] >= lowerBoundY:
        return intersectionPoint
    else:
        return -1
def circleLineSegmentIntersection(circleX, circleY, radius, segment):
    if segment[0] == segment[2]: # Vertical Line
        if abs(circleX - segment[0]) < radius:
            yDistance = math.sqrt(radius ** 2 - (circleX - segment[0]) ** 2)
            if max(segment[1], segment[3]) >= circleY + yDistance >= min(segment[1], segment[3]):
                return True
            elif max(segment[1], segment[3]) >= circleY - yDistance >= min(segment[1], segment[3]):
                return True
        return False

    lineSlope = calculateSlope(segment)
    intercept = calculateIntercept(segment)
    a = 1 + lineSlope ** 2
    b = -2 * circleX + 2 * lineSlope * (intercept - circleY)
    c = circleX ** 2 + (intercept - circleY) ** 2 - radius ** 2
    pointsOfIntersection = quadraticFormula(a, b, c)
    if len(pointsOfIntersection) == 0:
        return False
    for eachIntersection in pointsOfIntersection:
        if max(segment[0], segment[2]) >= eachIntersection >= min(segment[0], segment[2]):
            return True
    return False
def pointInsideRectangle(x, y, w, h, pointX, pointY):
    return (x + w >= pointX >= x) and (y >= pointY >= y - h)
def checkCollisions(circleX, circleY, radius, allObstacles):
    anyCollision = False
    for eachObstacle in allObstacles:
        for i in range(len(eachObstacle) - 1):
            segment = [eachObstacle[i][0], eachObstacle[i][1], eachObstacle[i+1][0], eachObstacle[i+1][1]]
            if circleLineSegmentIntersection(circleX, circleY, radius, segment):
                anyCollision = True
    return anyCollision




# pygame setup
pygame.init()
pygame.font.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIDEBAR_LENGTH = 200
heading = math.pi/2
xPos = SCREEN_WIDTH/2
yPos = SCREEN_HEIGHT/2
roombaRadius = 20
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_LENGTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
allExamples = [[[(400, 200), (800, 200), (800, 600), (400, 600), (400, 200)]], [[(200, 100), (1000, 100), (800, 700), (400, 700), (400, 400), (200, 400), (200, 100)]], [[(200, 200), (900, 200), (900, 600), (200, 600), (200, 200)], [(300, 300), (400, 300), (400, 350), (300, 350), (300, 300)]]]
basicBoxExample = [[(400, 200), (800, 200), (800, 600), (400, 600), (400, 200)]]
complicatedShapeExample = [[(200, 100), (1000, 100), (800, 700), (400, 700), (400, 400), (200, 400), (200, 100)]]
boxObstacleExample = [[(200, 200), (900, 200), (900, 600), (200, 600), (200, 200)], [(300, 300), (400, 300), (400, 350), (300, 350), (300, 300)]]
obstaclePositions = allExamples[0]
recordingData = False
headingDistanceData = []
delay = 0
notificationDisplayTime = 0

while running:
    if delay > 0:
        delay -= 1
    if notificationDisplayTime > 0:
        notificationDisplayTime -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        heading += 0.05
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        heading -= 0.05
    if pygame.key.get_pressed()[pygame.K_UP]:
        xPos += math.cos(heading)
        yPos += math.sin(heading)
        if checkCollisions(xPos, yPos, roombaRadius, obstaclePositions):
            xPos -= math.cos(heading)
            yPos -= math.sin(heading)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        xPos -= math.cos(heading)
        yPos -= math.sin(heading)
        if checkCollisions(xPos, yPos, roombaRadius, obstaclePositions):
            xPos += math.cos(heading)
            yPos += math.sin(heading)

    screen.fill((255, 255, 255))
    drawRectangle((67, 80, 88), SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_LENGTH, SCREEN_HEIGHT)

    # ------------------ Draws Side Panel ------------------ #
    for i in range(6):
        rectX = SCREEN_WIDTH + 20 + 60 * (i % 3)
        if i > 2:
            rectY = SCREEN_HEIGHT - 100
        else:
            rectY = SCREEN_HEIGHT - 40
        rectWidth = 40
        rectHeight = 40
        drawTransparentRectangle((125, 187, 195), rectX, rectY, 40, 40, 1)
        writeText((125, 187, 195), str(i + 1), 20, rectX + 15, rectY - 7)
        if pygame.mouse.get_pressed()[0]:
            mousePosition = pygame.mouse.get_pos()
            if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
                obstaclePositions = allExamples[i]
                xPos = SCREEN_WIDTH/2
                yPos = SCREEN_HEIGHT/2
                recordingData = False


    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 300
    rectWidth = SIDEBAR_LENGTH - 40
    rectHeight = 40
    drawTransparentRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    if recordingData:
        writeText((138, 131, 195), "Stop Recording", 24, rectX + 12, rectY - 5)
    else:
        writeText((138, 131, 195), "Start Recording", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            recordingData = not recordingData
            if recordingData:
                headingDistanceData = []
            delay = 15

    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 400
    rectWidth = SIDEBAR_LENGTH - 40
    rectHeight = 40
    drawTransparentRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    writeText((138, 131, 195), "Load Data", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            pass


    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 500
    rectWidth = SIDEBAR_LENGTH - 40
    rectHeight = 40
    drawTransparentRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    writeText((138, 131, 195), "Run Simulation", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            if len(headingDistanceData) == 0:
                notificationDisplayTime = 50
            pass
            # ???

    # Iteratively form a line with the next closest neighbour, if the slope of the line deviates then you know there is a change in direction

    # Start with random point P
    # Pick the closest point to P and form a line, measuring the slope and add it to a set visitedPoints and array [[p1, p2, p3], [p1, p2], etc, where each subarr is a collection of points that form a line]
    # Pick the next closest point, if the slope is within bounds K then add the point to the list and set
    # If the slope deviation is larger than bounds K, then create a new starting point P'
    # Repeat to pick the closest points to P' that are not in the set



    if notificationDisplayTime > 0:
        writeText((255, 0, 0), "No data available", 20, rectX, 50)

    drawCircle((0, 0, 0), xPos, yPos, roombaRadius)
    drawLine((100, 100, 255), xPos, yPos, xPos + 60 * math.cos(heading), yPos + 60 * math.sin(heading))


    # -------------------- Calculates line based on roomba heading -------------------- #
    if math.sin(heading) == 1:  # Points straight down
        segment1 = [xPos, yPos, xPos, SCREEN_HEIGHT]
    elif math.sin(heading) == -1:  # Points straight up
        segment1 = [xPos, yPos, xPos, 0]
    else:
        slope = math.tan(heading)
        if math.cos(heading) < 0:
            segment1 = [xPos, yPos, 0, yPos - slope * xPos]
        else:
            segment1 = [xPos, yPos, SCREEN_WIDTH, yPos + slope * (SCREEN_WIDTH - xPos)]
    drawLine((100, 100, 255), xPos, yPos, segment1[2], segment1[3])

    intersections = []
    for eachShape in obstaclePositions:
        for i in range(len(eachShape) - 1):
            drawLine((0, 0, 0), eachShape[i][0], eachShape[i][1], eachShape[i+1][0], eachShape[i+1][1])
            segment2 = [eachShape[i][0], eachShape[i][1], eachShape[i+1][0], eachShape[i+1][1]]
            intersectionPoint = calculateSegmentIntersection(segment1, segment2)
            if intersectionPoint != -1:
                intersections.append(intersectionPoint)

    closestIntersection = []
    if len(intersections) >= 1:
        closestIntersection = intersections[0]
        for intersection in intersections:
            if distance(xPos, yPos, intersection[0], intersection[1]) < distance(xPos, yPos, closestIntersection[0], closestIntersection[1]):
                closestIntersection = intersection



    if len(closestIntersection) > 0:
        drawCircle((255, 0, 0), closestIntersection[0], closestIntersection[1], 5)
        if recordingData:
            headingDistanceData.append((round(math.degrees(heading) % 360, 4), round(distance(xPos, yPos, closestIntersection[0], closestIntersection[1]), 4)))
#            print(round(math.degrees(heading) % 360, 4), round(distance(xPos, yPos, closestIntersection[0], closestIntersection[1]), 4))

    pygame.display.update()




    # Position starts at (0, 0)
    # If heading is different from previous heading:
    # Take distance and heading to calculate a vector that is added to current position to find the location of a wall/obstacle
    # If heading is same as previous heading:
    # Update position based on previous point



    clock.tick(60)  # limits FPS to 60

pygame.quit()