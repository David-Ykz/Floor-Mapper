import pygame
import time
import random

# pygame setup
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    rectX = []
    rectY = []
    colors = []
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            pygame.event.get()
            R = random.randint(0, 255)
            G = random.randint(0, 255)
            B = random.randint(0, 255)
            rectX.append(j)
            rectY.append(i)
            colors.append((R, G, B))
    #    pygame.draw.rect(screen, (R, G, B), (j, i, 1, 1))

    for i in range(len(rectX)):
        pygame.draw.rect(screen, colors[i], (rectX[i], rectY[i], 1, 1))
    pygame.display.update()

    # Position starts at (0, 0)
    # If heading is different from previous heading:
    # Take distance and heading to calculate a vector that is added to current position to find the location of a wall/obstacle
    # If heading is same as previous heading:
    # Update position based on previous point



#    clock.tick(120)  # limits FPS to 60

pygame.quit()