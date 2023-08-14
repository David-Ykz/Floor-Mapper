import sys
import time

import pygame
from Math import *
import random
from Algorithm import *

# Pygame Functions
def drawCircle(color, p, r):
    pygame.draw.circle(screen, color, (p.x, SCREEN_HEIGHT - p.y), r)
def drawHollowCircle(color, p, r, t):
    pygame.draw.circle(screen, color, (p.x, SCREEN_HEIGHT - p.y), r, t)
def drawRectangle(color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - y, w, h))
def drawHollowRectangle(color, rectangle, t):
    pygame.draw.rect(screen, color, (rectangle.topLeft.x, SCREEN_HEIGHT - rectangle.topLeft.y, rectangle.width, rectangle.height), t)
def drawLine(color, ls):
    pygame.draw.line(screen, color, (ls.x1, SCREEN_HEIGHT - ls.y1), (ls.x2, SCREEN_HEIGHT - ls.y2))
def writeText(color, text, size, x, y):
    font = pygame.font.SysFont("arial", size).render(text, True, color)
    screen.blit(font, (x, SCREEN_HEIGHT - y))
def drawButtons(recording, simRecording):
    TEAL = (125, 187, 195)
    PURPLE = (138, 131, 195)
    for i in range(len(buttons)):
        if i < 6:
            drawHollowRectangle(TEAL, buttons[i], 1)
            writeText(TEAL, str(i + 1), 20, buttons[i].topLeft.x + 15, buttons[i].topLeft.y - 7)
        elif i == 6: # Recording Button
            drawHollowRectangle(PURPLE, buttons[i], 1)
            if recording:
                writeText(PURPLE, "Stop Recording", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
            else:
                writeText(PURPLE, "Start Recording", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
        elif i == 7: # Load Data Button
            drawHollowRectangle(PURPLE, buttons[i], 1)
            writeText(PURPLE, "Load Data", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
        elif i == 8:
            drawHollowRectangle(PURPLE, buttons[i], 1)
            if simRecording:
                writeText(PURPLE, "Stop Simulation", 24, buttons[i].topLeft.x + 10, buttons[i].topLeft.y - 5)
            else:
                writeText(PURPLE, "Run Simulation", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)


# Pygame/Program Initialization
pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH = 1200, 800, 200
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
buttons = []
for i in range(6):
    rectX = SCREEN_WIDTH + 20 + 60 * (i % 3)
    if i > 2:
        rectY = SCREEN_HEIGHT - 100
    else:
        rectY = SCREEN_HEIGHT - 40
    buttons.append(Rectangle(rectX, rectY, 40, 40))
for i in range(3):
    buttons.append(Rectangle(SCREEN_WIDTH + 20, SCREEN_HEIGHT - 300 - 100 * i, SIDEBAR_WIDTH - 40, 40))

listOfColors = []
for i in range(10000):
    listOfColors.append((10 * random.randint(0, 25), 10 * random.randint(0, 25), 10 * random.randint(0, 25)))


# Roomba Initialization
currentPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
startingPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
heading = math.pi/2
roombaRadius = 20
# Map Layout
basicBoxLayout = [coordinatesToPoints([(400, 200), (800, 200), (800, 600), (400, 600), (400, 200)])]
complicatedShapeLayout = [coordinatesToPoints([(200, 100), (1000, 100), (800, 700), (400, 700), (400, 400), (200, 400), (200, 100)])]
boxObstacleLayout = [coordinatesToPoints([(200, 200), (900, 200), (900, 600), (200, 600), (200, 200)]), coordinatesToPoints([(300, 300), (400, 300), (400, 350), (300, 350), (300, 300)])]
allFloorLayouts = [basicBoxLayout, complicatedShapeLayout, boxObstacleLayout]
floorLayout = allFloorLayouts[0]
# Runtime
isRecording = False
recordedData = []
estimatedPoints = set()
pastPositions = []
pastHeadings = []
groupedPoints = dict()
positionIndex = 0
delay = 0
startingPoint = Point(0, 0)
notificationDisplayTime = 0
simulationRunning = False
currentFloorLayout = []

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
        currentPosition.x += math.cos(heading)
        currentPosition.y += math.sin(heading)
        isMoving = True
        if checkCollisions(currentPosition, roombaRadius, floorLayout):
            currentPosition.x -= math.cos(heading)
            currentPosition.y -= math.sin(heading)
            isMoving = False
    else:
        isMoving = False

    # Draws background and side panel
    screen.fill((255, 255, 255))
    drawRectangle((67, 80, 88), SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    drawButtons(isRecording, simulationRunning)

    if pygame.mouse.get_pressed()[0] and delay == 0:
        mousePosition = Point(pygame.mouse.get_pos()[0], SCREEN_HEIGHT - pygame.mouse.get_pos()[1])
        for i in range(len(buttons)):
            if buttons[i].insideRect(mousePosition):
                if i < 6:
                    floorLayout = allFloorLayouts[i]
                    currentPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    isRecording = False
                    simulationRunning = False
                elif i == 6:
                    isRecording = not isRecording
                    simulationRunning = False
                    if isRecording:
                        recordedData = []
                        startingPosition = Point(currentPosition.x, currentPosition.y)
                        currentFloorLayout = floorLayout.copy()
                    delay = 15
                elif i == 7:
                    pass
                elif i == 8 and not isRecording:
                    if len(recordedData) == 0:
                        notificationDisplayTime = 50
                    else:
                        estimatedPoints, pastPositions, pastHeadings = headingDistanceToPoints(startingPosition, recordedData)
                        groupedPoints = fitLineToData(list(estimatedPoints))
                        simulationRunning = not simulationRunning
                        positionIndex = 0
                        floorLayout = currentFloorLayout.copy()
                        delay = 15


    if notificationDisplayTime > 0:
        writeText((255, 0, 0), "No data available", 20, SCREEN_WIDTH + 20, 50)
    if simulationRunning:
        colorIndex = 0
        for eachCollectionPoints in groupedPoints:
            for eachPoint in groupedPoints[eachCollectionPoints]:
                drawCircle(listOfColors[colorIndex], eachPoint, 2)
            colorIndex += 1

        if positionIndex < len(pastPositions):
            retraceHeading = pastHeadings[positionIndex]
            drawHollowCircle((0, 0, 0), pastPositions[positionIndex], roombaRadius, 1)
            drawLine((100, 100, 255), LineSegment(pastPositions[positionIndex], Point(pastPositions[positionIndex].x + 40 * math.cos(math.radians(retraceHeading)), pastPositions[positionIndex].y + 40 * math.sin(math.radians(retraceHeading)))))
            positionIndex += 1
        else:
            simulationRunning = False
    else:
        drawCircle((0, 0, 0), currentPosition, roombaRadius)
        drawLine((100, 100, 255), LineSegment(currentPosition, Point(currentPosition.x + 40 * math.cos(heading), currentPosition.y + 40 * math.sin(heading))))


    # -------------------------------------------------- Calculates line based on roomba heading -------------------------------------------------- #
    if math.sin(heading) == 1:  # Points straight down
        roombaToBorderSegment = LineSegment(currentPosition, Point(currentPosition.x, SCREEN_HEIGHT))
    elif math.sin(heading) == -1:  # Points straight up
        roombaToBorderSegment = LineSegment(currentPosition, Point(currentPosition.x, 0))
    else:
        slope = math.tan(heading)
        if math.cos(heading) < 0:
            roombaToBorderSegment = LineSegment(currentPosition, Point(0, currentPosition.y - slope * currentPosition.x))
        else:
            roombaToBorderSegment = LineSegment(currentPosition, Point(SCREEN_WIDTH, currentPosition.y + slope * (SCREEN_WIDTH - currentPosition.x)))

    intersections = []
    for eachShape in floorLayout:
        for i in range(len(eachShape) - 1):
            connectingLineSegment = LineSegment(eachShape[i], eachShape[i + 1])
            drawLine((0, 0, 0), connectingLineSegment)
            intersectionPoint = calculateSegmentIntersection(roombaToBorderSegment, connectingLineSegment)
            if intersectionPoint != -1:
                intersections.append(intersectionPoint)

    closestIntersection = -1
    if len(intersections) >= 1:
        closestIntersection = intersections[0]
        for intersection in intersections:
            if LineSegment(currentPosition, intersection).length() < LineSegment(currentPosition, closestIntersection).length():
                closestIntersection = intersection

    if closestIntersection != -1:
        if isRecording:
            recordedData.append((round(math.degrees(heading) % 360, 4), round(LineSegment(currentPosition, closestIntersection).length(), 4), isMoving, 1))

    pygame.display.update()
    clock.tick(60)  # limits FPS to 60

pygame.quit()