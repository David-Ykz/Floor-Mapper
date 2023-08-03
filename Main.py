import math

import pygame
import time
import random



# pygame setup
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIDEBAR_LENGTH = 200
heading = 3.14
xPos = (SCREEN_WIDTH-SIDEBAR_LENGTH)/2
yPos = SCREEN_HEIGHT/2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
obstaclePositions = [[200, 200], [600, 200], [600, 600], [200, 600], [200, 200]]
lines = []

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def slope(segment):
    return (segment[3] - segment[1]) / (segment[2] - segment[0])

def intercept(segment):
    return segment[1] - slope(segment) * segment[0]

def calculateLineIntersection(m1, b1, m2, b2):
    if m1 == m2:
        return -1
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return [x, y]

def calculateSegmentIntersection(segment1, segment2):
    intersectionPoint = [0, 0]

    # Check if both lines are vertical
    if segment1[0] == segment1[2] and segment2[0] == segment2[2]:
        return -1
    # First line is vertical
    if segment1[0] == segment1[2]:
        intersectionPoint = (segment1[0], slope(segment2) * segment1[0] + intercept(segment2))
#        intersectionPoint[0] = segment1[0]
#        intersectionPoint[1] = slope(segment2) * segment1[0] + intercept(segment2)
    elif segment2[0] == segment2[0]:
        intersectionPoint[0] = segment2[0]
        intersectionPoint[1] = slope(segment1) * segment2[0] + intercept(segment1)
    else:
        intersectionPoint = calculateLineIntersection(slope(segment1), intercept(segment1), slope(segment2), intercept(segment2))

    lowerBoundX = max(segment1[0], segment2[0])
    lowerBoundY = max(segment1[1], segment2[1])
    upperBoundX = min(segment1[2], segment2[2])
    upperBoundY = min(segment1[3], segment2[3])
    if upperBoundX >= intersectionPoint[0] >= lowerBoundX and upperBoundY >= intersectionPoint[1] >= lowerBoundY:
        return intersectionPoint
    else:
        return -1









for i in range(len(obstaclePositions) - 1):
    pointA = obstaclePositions[i]
    pointB = obstaclePositions[i + 1]
    deltaX = pointB[0] - pointA[0]
    deltaY = pointB[1] - pointA[1]
    if deltaX == 0: # Vertical Line
        lines.append([pointA[1], pointB[1], 1, pointA[0]])
    else:
        lines.append([pointA[0], pointB[0], 0, pointA[1]])

print(lines)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if pygame.key.get_pressed()[pygame.K_LEFT]:
        heading -= 0.05
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        heading += 0.05

    if pygame.key.get_pressed()[pygame.K_UP]:
        xPos += math.cos(heading)
        yPos += math.sin(heading)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        xPos -= math.cos(heading)
        yPos -= math.sin(heading)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (208, 225, 212), (SCREEN_WIDTH-SIDEBAR_LENGTH, 0, SIDEBAR_LENGTH, SCREEN_HEIGHT))
    pygame.draw.circle(screen, (0, 0, 0), (xPos, yPos), 20)
    pygame.draw.line(screen, (100, 100, 255), (xPos, yPos), (xPos + 60 * math.cos(heading), yPos + 60 * math.sin(heading)))

    intersections = []

    for line in lines:
        if line[2] == 1: # Vertical Line
            horizontalDistance = xPos - line[3]
            yValue = horizontalDistance * math.sin(heading) + yPos
            if max(line[0], line[1]) >= yValue >= min(line[0], line[1]):
                intersections.append([line[3], yValue])
            else:
                print("sdjkfhsdkfjsdhf")
        else: # Horizontal Line
            verticalDistance = line[3] - yPos
            xValue = verticalDistance * math.cos(heading) + xPos
            print (verticalDistance * math.cos(heading))
            print("")
            if max(line[0], line[1]) >= xValue >= min(line[0], line[1]):
                intersections.append([xValue, line[3]])
                print(xValue)
            else:
                print("qhsweuygsdbvfsdjfh")
    closestIntersection = intersections[0]
    for intersection in intersections:
        pygame.draw.circle(screen, (255, 0, 0), (intersection[0], intersection[1]), 5)
        if distance(xPos, yPos, intersection[0], intersection[1]) < distance(xPos, yPos, closestIntersection[0], closestIntersection[1]):
            closestIntersection = intersection

    pygame.draw.line(screen, (100, 100, 255), (xPos, yPos), (closestIntersection[0], closestIntersection[1]))

    for i in range(len(obstaclePositions) - 1):
        pygame.draw.line(screen, (0, 0, 0), (obstaclePositions[i][0], obstaclePositions[i][1]), (obstaclePositions[i+1][0], obstaclePositions[i+1][1]))

    pygame.display.update()




    # Position starts at (0, 0)
    # If heading is different from previous heading:
    # Take distance and heading to calculate a vector that is added to current position to find the location of a wall/obstacle
    # If heading is same as previous heading:
    # Update position based on previous point



    clock.tick(60)  # limits FPS to 60

pygame.quit()