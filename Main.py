import math

import pygame
import time
import random

# pygame setup
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIDEBAR_LENGTH = 200
heading = 0.0
xOffset = 200
yOffset = 200
xPos = (SCREEN_WIDTH-SIDEBAR_LENGTH)/2
yPos = SCREEN_HEIGHT/2
obstaclePositions = []
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

obstaclePositions.append([0, 0])
obstaclePositions.append([400, 0])
obstaclePositions.append([400, 400])
obstaclePositions.append([0, 400])
obstaclePositions.append([0, 0])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if pygame.key.get_pressed()[pygame.K_a]:
        heading -= 0.05
    elif pygame.key.get_pressed()[pygame.K_d]:
        heading += 0.05

    if pygame.key.get_pressed()[pygame.K_w]:
        xPos += math.cos(heading)
        yPos += math.sin(heading)
    elif pygame.key.get_pressed()[pygame.K_s]:
        xPos -= math.cos(heading)
        yPos -= math.sin(heading)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (208, 225, 212), (SCREEN_WIDTH-SIDEBAR_LENGTH, 0, SIDEBAR_LENGTH, SCREEN_HEIGHT))
    pygame.draw.circle(screen, (0, 0, 0), (xPos, yPos), 20)
    pygame.draw.line(screen, (100, 100, 255), (xPos, yPos), (xPos + 60 * math.cos(heading), yPos + 60 * math.sin(heading)))

    for i in range(len(obstaclePositions) - 1):
        pygame.draw.line(screen, (0, 0, 0), (obstaclePositions[i][0] + xOffset, obstaclePositions[i][1] + yOffset), (obstaclePositions[i+1][0] + xOffset, obstaclePositions[i+1][1] + yOffset))

    pygame.display.update()




    # Position starts at (0, 0)
    # If heading is different from previous heading:
    # Take distance and heading to calculate a vector that is added to current position to find the location of a wall/obstacle
    # If heading is same as previous heading:
    # Update position based on previous point



    clock.tick(60)  # limits FPS to 60

pygame.quit()