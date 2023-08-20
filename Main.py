import pygame
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
def drawButtons(recording, sim1Running, sim2Running, numBeacons):
    TEAL = (125, 187, 195)
    PURPLE = (138, 131, 195)
    ORANGE = (247, 179, 43)
    writeText(TEAL, "Sample Floor Layouts", 20, SCREEN_WIDTH + 20, SCREEN_HEIGHT - 10)
    for i in range(len(buttons)):
        if i < 3:
            drawHollowRectangle(TEAL, buttons[i], 1)
            writeText(TEAL, "Example " + str(i + 1), 20, buttons[i].topLeft.x + 40, buttons[i].topLeft.y - 7)
        elif i == 3:
            drawHollowRectangle(PURPLE, buttons[i], 1)
            writeText(PURPLE, "Place Beacon (" + str(numBeacons) + "/3)", 20, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 8)
        elif i == 4:
            drawHollowRectangle(PURPLE, buttons[i], 1)
            writeText(PURPLE, "Clear Beacons", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
        elif i == 5: # Recording Button
            drawHollowRectangle(PURPLE, buttons[i], 1)
            if recording:
                writeText(PURPLE, "Stop Recording", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
            else:
                writeText(PURPLE, "Start Recording", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
        elif i == 6: # Load Data Button
            drawHollowRectangle(PURPLE, buttons[i], 1)
            writeText(PURPLE, "Load Data", 24, buttons[i].topLeft.x + 12, buttons[i].topLeft.y - 5)
        elif i == 7:
            drawHollowRectangle(ORANGE, buttons[i], 1)
            if sim1Running:
                writeText(ORANGE, "Stop", 22, buttons[i].topLeft.x + 65, buttons[i].topLeft.y - 5)
            else:
                writeText(ORANGE, "Distance-Heading", 22, buttons[i].topLeft.x + 10, buttons[i].topLeft.y - 5)
            writeText(ORANGE, "Simulation", 22, buttons[i].topLeft.x + 38, buttons[i].topLeft.y - 35)
        elif i == 8:
            drawHollowRectangle(ORANGE, buttons[i], 1)
            if sim2Running:
                writeText(ORANGE, "Stop", 22, buttons[i].topLeft.x + 65, buttons[i].topLeft.y - 5)
            else:
                writeText(ORANGE, "Triangulation", 22, buttons[i].topLeft.x + 28, buttons[i].topLeft.y - 5)
            writeText(ORANGE, "Simulation", 22, buttons[i].topLeft.x + 38, buttons[i].topLeft.y - 35)

# Pygame/Program Initialization
pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH = 1200, 800, 200
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
buttons = []
# Initialize Buttons
for i in range(9):
    if i < 3:
        buttons.append(Rectangle(SCREEN_WIDTH + 20, SCREEN_HEIGHT - 50 - 50 * i, SIDEBAR_WIDTH - 40, 40))
    elif i < 7:
        buttons.append(Rectangle(SCREEN_WIDTH + 20, SCREEN_HEIGHT - 100 - 50 * i, SIDEBAR_WIDTH - 40, 40))
    else:
        buttons.append(Rectangle(SCREEN_WIDTH + 20, SCREEN_HEIGHT + 100 - 90 * i, SIDEBAR_WIDTH - 40, 70))
# Initialize Colors
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
listOfColors = []
for i in range(10000):
    listOfColors.append((10 * random.randint(0, 25), 10 * random.randint(0, 25), 10 * random.randint(0, 25)))

# Roomba Initialization
currentPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
startingPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
roombaHeading, roombaRadius, roombaSpeed = math.pi/2, 20, 2
# Map Layout
basicBoxLayout = [coordinatesToPoints([(4, 2), (8, 2), (8, 6), (4, 6), (4, 2)])]
basicObstacleLayout = [coordinatesToPoints([(1, 1), (4, 1), (4, 3), (10, 3), (10, 7), (1, 7), (1, 1)]), coordinatesToPoints([(7, 6), (9, 6), (9, 5), (7, 5), (7, 6)])]
complexShapeLayout = [coordinatesToPoints([(1, 3), (3, 1), (5, 1), (7, 3), (8, 3), (8, 1), (9.5, 1), (9.5, 3), (11, 3), (11, 7), (9.5, 7), (9.5, 5), (7, 5), (5, 7), (3, 7), (1, 5), (1, 3)]), coordinatesToPoints([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])]
allFloorLayouts = [basicBoxLayout, basicObstacleLayout, complexShapeLayout]
floorLayout = allFloorLayouts[0]
# Runtime
isRecording, headingDistanceSimulationRunning, triangulationSimulationRunning, placingBeacons = False, False, False, False
notificationDisplayTime, mouseInputDelay = 0, 0
headingDistanceToWall, distancesToBeacons, wallPoints, truePositions, trueHeadings = [], [], [], [], []
pastPositions, pastHeadings, groupedPoints = [], [], dict()
positionIndex = 0
currentFloorLayout = []
beacons = [Point(500, 100), Point(200, 300), Point(800, 700)]

while running:
    # Handles timers
    if mouseInputDelay > 0:
        mouseInputDelay -= 1
    if notificationDisplayTime > 0:
        notificationDisplayTime -= 1

    # Stops the program if the pygame window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Heading direction input
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        roombaHeading += 0.05
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        roombaHeading -= 0.05

    # Movement input
    if pygame.key.get_pressed()[pygame.K_UP]:
        currentPosition.x += roombaSpeed * math.cos(roombaHeading)
        currentPosition.y += roombaSpeed * math.sin(roombaHeading)
        isMoving = True
        anyCollisions = checkCollisions(currentPosition, roombaRadius, floorLayout)
        if len(anyCollisions) > 0:
            currentPosition.x -= roombaSpeed * math.cos(roombaHeading)
            currentPosition.y -= roombaSpeed * math.sin(roombaHeading)
            wallPoints.extend(anyCollisions)
            isMoving = False
    else:
        isMoving = False

    # Draws background and side panel
    screen.fill(WHITE)
    drawRectangle((67, 80, 88), SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    drawButtons(isRecording, headingDistanceSimulationRunning, triangulationSimulationRunning, len(beacons))

    # Draws floor layout
    for eachShape in floorLayout:
        for i in range(len(eachShape) - 1):
            connectingLineSegment = LineSegment(eachShape[i], eachShape[i + 1])
            drawLine(BLACK, connectingLineSegment)

    # Process mouse input
    mousePosition = Point(pygame.mouse.get_pos()[0], SCREEN_HEIGHT - pygame.mouse.get_pos()[1])
    if pygame.mouse.get_pressed()[0] and mouseInputDelay == 0:
        mouseInputDelay = 15
        for i in range(len(buttons)):
            if buttons[i].insideRect(mousePosition):
                if i < 3:
                    floorLayout = allFloorLayouts[i]
                    currentPosition = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    isRecording = False
                    simulationRunning = False
                    beacons.clear()
                elif i == 3 and len(beacons) < 3:
                    placingBeacons = True
                elif i == 4:
                    beacons.clear()
                    isRecording = False
                elif i == 5 and len(beacons) == 3: # Records Data
                    isRecording = not isRecording
                    simulationRunning = False
                    if isRecording:
                        headingDistanceToWall = []
                        distancesToBeacons = []
                        wallPoints = []
                        startingPosition = Point(currentPosition.x, currentPosition.y)
                        currentFloorLayout = floorLayout.copy()
                        currentBeacons = beacons.copy()
                        trueHeadings, truePositions = [], []
                elif i == 6:
                    pass
                elif i == 7 and not isRecording:
                    if len(headingDistanceToWall) == 0:
                        notificationDisplayTime = 50
                    else:
                        estimatedPoints, pastPositions, pastHeadings = headingDistanceToPoints(Point(startingPosition.x, startingPosition.y), headingDistanceToWall)
                        groupedPoints = fitLineToData(list(estimatedPoints))
                        headingDistanceSimulationRunning = not headingDistanceSimulationRunning
                        positionIndex = 0
                        floorLayout = currentFloorLayout.copy()
                elif i == 8 and not isRecording:
                    if len(distancesToBeacons) == 0:
                        notificationDisplayTime = 50
                    else:
                        pastPositions = triangulation(beacons, distancesToBeacons)
                        triangulationSimulationRunning = not triangulationSimulationRunning
                        groupedPoints = fitLineToData(removeDuplicatePoints(wallPoints))
                        positionIndex = 0
                        floorLayout = currentFloorLayout.copy()
        if placingBeacons and mousePosition.x < SCREEN_WIDTH:
            beacons.append(mousePosition)
            placingBeacons = False

    # Handles simulations when running
    if notificationDisplayTime > 0:
        writeText(RED, "No data available", 20, SCREEN_WIDTH + 20, 50)

    if headingDistanceSimulationRunning or triangulationSimulationRunning:
        colorIndex = 0
        # Draws lines
        for eachCollectionPoints in groupedPoints:
            for eachPoint in groupedPoints[eachCollectionPoints]:
                drawCircle(listOfColors[colorIndex], eachPoint, 2)
            colorIndex += 1
        # Draws roomba
        if positionIndex < min(len(pastPositions), len(trueHeadings)):
            estimatedHeading, trueHeading = pastHeadings[positionIndex], trueHeadings[positionIndex]
            # True roomba data
            drawHollowCircle(BLACK, truePositions[positionIndex], roombaRadius, 1)
            drawLine(BLACK, LineSegment(truePositions[positionIndex], Point(truePositions[positionIndex].x + 40 * math.cos(math.radians(trueHeading)), pastPositions[positionIndex].y + 40 * math.sin(math.radians(trueHeading)))))
            # Estimated roomba data
            drawHollowCircle(RED, pastPositions[positionIndex], roombaRadius, 1)
            drawLine(RED, LineSegment(pastPositions[positionIndex], Point(pastPositions[positionIndex].x + 40 * math.cos(math.radians(estimatedHeading)), pastPositions[positionIndex].y + 40 * math.sin(math.radians(estimatedHeading)))))
            positionIndex += 1
        else:
            headingDistanceSimulationRunning, triangulationSimulationRunning = False, False
    else:
        drawCircle(BLACK, currentPosition, roombaRadius)
        drawLine((100, 100, 255), LineSegment(currentPosition, Point(currentPosition.x + 40 * math.cos(roombaHeading), currentPosition.y + 40 * math.sin(roombaHeading))))


    if placingBeacons:
        drawHollowCircle((0, 0, 255), mousePosition, 10, 1)

    for beacon in beacons:
        drawHollowCircle((0, 0, 255), beacon, 10, 1)

    # Calculates line from roomba to border
    if math.sin(roombaHeading) == 1:  # Points straight down
        roombaToBorderSegment = LineSegment(currentPosition, Point(currentPosition.x, SCREEN_HEIGHT))
    elif math.sin(roombaHeading) == -1:  # Points straight up
        roombaToBorderSegment = LineSegment(currentPosition, Point(currentPosition.x, 0))
    else:
        slope = math.tan(roombaHeading)
        if math.cos(roombaHeading) < 0:
            roombaToBorderSegment = LineSegment(currentPosition, Point(0, currentPosition.y - slope * currentPosition.x))
        else:
            roombaToBorderSegment = LineSegment(currentPosition, Point(SCREEN_WIDTH, currentPosition.y + slope * (SCREEN_WIDTH - currentPosition.x)))

    # Calculates point of intersection (if any) between roomba-border line and floor layout
    intersections, closestIntersection = [], -1
    for eachShape in floorLayout:
        for i in range(len(eachShape) - 1):
            intersectionPoint = calculateSegmentIntersection(roombaToBorderSegment, LineSegment(eachShape[i], eachShape[i + 1]))
            if intersectionPoint != -1:
                intersections.append(intersectionPoint)
    if len(intersections) >= 1:
        closestIntersection = intersections[0]
        for intersection in intersections:
            if LineSegment(currentPosition, intersection).length() < LineSegment(currentPosition, closestIntersection).length():
                closestIntersection = intersection

    # Records data
    if isRecording and closestIntersection != -1:
        headingDistanceToWall.append((round(math.degrees(roombaHeading) % 360, 4), round(LineSegment(currentPosition, closestIntersection).length(), 4), isMoving, roombaSpeed))
        distanceToBeacon = []
        for eachBeacon in beacons:
            distanceToBeacon.append(LineSegment(currentPosition, eachBeacon).length())
        distancesToBeacons.append(distanceToBeacon)
        truePositions.append(Point(currentPosition.x, currentPosition.y))
        trueHeadings.append(round(math.degrees(roombaHeading) % 360, 4))

    pygame.display.update()
    clock.tick(60)  # limits FPS to 60

pygame.quit()