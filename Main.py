import math
import pygame

# Pygame Functions
def drawCircle(color, x, y, r):
    pygame.draw.circle(screen, color, (x, SCREEN_HEIGHT - y), r)
def drawHollowCircle(color, x, y, r, t):
    pygame.draw.circle(screen, color, (x, SCREEN_HEIGHT - y), r, t)
def drawRectangle(color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - y, w, h))
def drawHollowRectangle(color, x, y, w, h, t):
    pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - y, w, h), t)
def drawLine(color, x1, y1, x2, y2):
    pygame.draw.line(screen, color, (x1, SCREEN_HEIGHT - y1), (x2, SCREEN_HEIGHT - y2))
def writeText(color, text, size, x, y):
    font = pygame.font.SysFont("arial", size).render(text, True, color)
    screen.blit(font, (x, SCREEN_HEIGHT - y))
# Algorithm Logic
def headingDistanceToPoints(x, y, data):
    previousHeading = 0
    pointX, pointY = 0, 0
    allPoints = set()
    positionData = []
    # Position starts at (0, 0)
    # If heading is different from previous heading:
    # Take distance and heading to calculate a vector that is added to current position to find the location of a wall/obstacle
    # If heading is same as previous heading:
    # Update position based on previous point
    for dataPoint in data:
        currentHeading = dataPoint[0]
        distanceToObstacle = dataPoint[1]
        currentlyMoving = dataPoint[2]
        averageVelocity = dataPoint[3]
        if currentlyMoving:
            if currentHeading != previousHeading:
                pointX = x + (distanceToObstacle + averageVelocity) * math.cos(math.radians(currentHeading))
                pointY = y + (distanceToObstacle + averageVelocity) * math.sin(math.radians(currentHeading))
                previousHeading = currentHeading
                allPoints.add((pointX, pointY))
            deltaDistance = distance(x, y, pointX, pointY) - distanceToObstacle
            x += deltaDistance * math.cos(math.radians(currentHeading))
            y += deltaDistance * math.sin(math.radians(currentHeading))
        elif currentHeading != previousHeading:
            pointX = x + distanceToObstacle * math.cos(math.radians(currentHeading))
            pointY = y + distanceToObstacle * math.sin(math.radians(currentHeading))
            allPoints.add((pointX, pointY))
            previousHeading = currentHeading
        positionData.append((x, y, currentHeading))
    return allPoints, positionData

# Pygame/Program Initialization
pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH = 1200, 800, 200
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
# Roomba Initialization
startingX, startingY = xPos, yPos = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
heading = math.pi/2
roombaRadius = 20
# Map Layout
allExamples = [[[(400, 200), (800, 200), (800, 600), (400, 600), (400, 200)]], [[(200, 100), (1000, 100), (800, 700), (400, 700), (400, 400), (200, 400), (200, 100)]], [[(200, 200), (900, 200), (900, 600), (200, 600), (200, 200)], [(300, 300), (400, 300), (400, 350), (300, 350), (300, 300)]]]
basicBoxExample = [[(400, 200), (800, 200), (800, 600), (400, 600), (400, 200)]]
complicatedShapeExample = [[(200, 100), (1000, 100), (800, 700), (400, 700), (400, 400), (200, 400), (200, 100)]]
boxObstacleExample = [[(200, 200), (900, 200), (900, 600), (200, 600), (200, 200)], [(300, 300), (400, 300), (400, 350), (300, 350), (300, 300)]]
obstaclePositions = allExamples[0]
# Runtime Variables
isRecording = False
recordedData = []
estimatedPoints = set()
pastPositions = []
positionIndex = 0
delay = 0
notificationDisplayTime = 0
displayPoints = False

while running:
    # Handles timers
    if delay > 0:
        delay -= 1
    if notificationDisplayTime > 0:
        notificationDisplayTime -= 1

    # Stops the program if the pygame window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # User input
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        heading += 0.05
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        heading -= 0.05

    if pygame.key.get_pressed()[pygame.K_UP]:
        xPos += math.cos(heading)
        yPos += math.sin(heading)
        isMoving = True
        if checkCollisions(xPos, yPos, roombaRadius, obstaclePositions):
            xPos -= math.cos(heading)
            yPos -= math.sin(heading)
            isMoving = False
    else:
        isMoving = False

    # Draws background and side panel
    screen.fill((255, 255, 255))
    drawRectangle((67, 80, 88), SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    # Draws buttons for layout
    for i in range(6):
        rectX = SCREEN_WIDTH + 20 + 60 * (i % 3)
        if i > 2:
            rectY = SCREEN_HEIGHT - 100
        else:
            rectY = SCREEN_HEIGHT - 40
        rectWidth = 40
        rectHeight = 40
        drawHollowRectangle((125, 187, 195), rectX, rectY, 40, 40, 1)
        writeText((125, 187, 195), str(i + 1), 20, rectX + 15, rectY - 7)
        if pygame.mouse.get_pressed()[0]:
            mousePosition = pygame.mouse.get_pos()
            if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
                obstaclePositions = allExamples[i]
                xPos = SCREEN_WIDTH/2
                yPos = SCREEN_HEIGHT/2
                isRecording = False
    # Draws the "recording" button
    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 300
    rectWidth = SIDEBAR_WIDTH - 40
    rectHeight = 40
    drawHollowRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    if isRecording:
        writeText((138, 131, 195), "Stop Recording", 24, rectX + 12, rectY - 5)
    else:
        writeText((138, 131, 195), "Start Recording", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            isRecording = not isRecording
            if isRecording:
                recordedData = []
                startingX, startingY = xPos, yPos
            delay = 15
    # Draws the button to load data
    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 400
    rectWidth = SIDEBAR_WIDTH - 40
    rectHeight = 40
    drawHollowRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    writeText((138, 131, 195), "Load Data", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            pass
    # Draws the simulation button
    rectX = SCREEN_WIDTH + 20
    rectY = SCREEN_HEIGHT - 500
    rectWidth = SIDEBAR_WIDTH - 40
    rectHeight = 40
    drawHollowRectangle((138, 131, 195), rectX, rectY, rectWidth, rectHeight, 1)
    if displayPoints:
        writeText((138, 131, 195), "Stop Simulation", 24, rectX + 10, rectY - 5)
    else:
        writeText((138, 131, 195), "Run Simulation", 24, rectX + 12, rectY - 5)
    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = pygame.mouse.get_pos()
        if pointInsideRectangle(rectX, rectY, rectWidth, rectHeight, mousePosition[0], SCREEN_HEIGHT - mousePosition[1]):
            if len(recordedData) == 0:
                notificationDisplayTime = 50
            else:
                estimatedPoints, pastPositions = headingDistanceToPoints(startingX, startingY, recordedData)
                displayPoints = not displayPoints
                positionIndex = 0
                delay = 15

    # Iteratively form a line with the next closest neighbour, if the slope of the line deviates then you know there is a change in direction

    # Start with random point P
    # Pick the closest point to P and form a line, measuring the slope and add it to a set visitedPoints and array [[p1, p2, p3], [p1, p2], etc, where each subarr is a collection of points that form a line]
    # Pick the next closest point, if the slope is within bounds K then add the point to the list and set
    # If the slope deviation is larger than bounds K, then create a new starting point P'
    # Repeat to pick the closest points to P' that are not in the set


    if notificationDisplayTime > 0:
        writeText((255, 0, 0), "No data available", 20, rectX, 50)
    if displayPoints:
        for eachPoint in estimatedPoints:
            drawCircle((100, 255, 100), eachPoint[0], eachPoint[1], 2)
        if positionIndex < len(pastPositions):
            retraceX = pastPositions[positionIndex][0]
            retraceY = pastPositions[positionIndex][1]
            retraceHeading = pastPositions[positionIndex][2]
            drawHollowCircle((0, 0, 0), retraceX, retraceY, 10, 1)
            drawLine((100, 100, 255), retraceX, retraceY, retraceX + 30 * math.cos(math.radians(retraceHeading)), retraceY + 30 * math.sin(math.radians(retraceHeading)))
            positionIndex += 1
        else:
            displayPoints = False
    else:
        drawCircle((0, 0, 0), xPos, yPos, roombaRadius)
        drawLine((100, 100, 255), xPos, yPos, xPos + 60 * math.cos(heading), yPos + 60 * math.sin(heading))


    # -------------------------------------------------- Calculates line based on roomba heading -------------------------------------------------- #
    if math.sin(heading) == 1:  # Points straight down
        roombaToBorderSegment = [xPos, yPos, xPos, SCREEN_HEIGHT]
    elif math.sin(heading) == -1:  # Points straight up
        roombaToBorderSegment = [xPos, yPos, xPos, 0]
    else:
        slope = math.tan(heading)
        if math.cos(heading) < 0:
            roombaToBorderSegment = [xPos, yPos, 0, yPos - slope * xPos]
        else:
            roombaToBorderSegment = [xPos, yPos, SCREEN_WIDTH, yPos + slope * (SCREEN_WIDTH - xPos)]
#    drawLine((100, 100, 255), xPos, yPos, roombaToBorderSegment[2], roombaToBorderSegment[3])

    intersections = []
    for eachShape in obstaclePositions:
        for i in range(len(eachShape) - 1):
            drawLine((0, 0, 0), eachShape[i][0], eachShape[i][1], eachShape[i+1][0], eachShape[i+1][1])
            obstacleLineSegment = [eachShape[i][0], eachShape[i][1], eachShape[i+1][0], eachShape[i+1][1]]
            intersectionPoint = calculateSegmentIntersection(roombaToBorderSegment, obstacleLineSegment)
            if intersectionPoint != -1:
                intersections.append(intersectionPoint)

    closestIntersection = []
    if len(intersections) >= 1:
        closestIntersection = intersections[0]
        for intersection in intersections:
            if distance(xPos, yPos, intersection[0], intersection[1]) < distance(xPos, yPos, closestIntersection[0], closestIntersection[1]):
                closestIntersection = intersection

    if len(closestIntersection) > 0:
        if isRecording:
            recordedData.append((round(math.degrees(heading) % 360, 4), round(distance(xPos, yPos, closestIntersection[0], closestIntersection[1]), 4), isMoving, 1))

    pygame.display.update()
    clock.tick(60)  # limits FPS to 60

pygame.quit()