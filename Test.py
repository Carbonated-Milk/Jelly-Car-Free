import pygame
from GameObject import *
from PointMass import *
import numpy as np
from Wheel import Wheel
from Input import Input

class GameRunner:

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Singleton.screen = screen
    clock = pygame.time.Clock()
    running = True
    center = (1280/2, 720/2)

    pointData = [PointInfo([100, 40], 1), PointInfo([-40, 40], 1), PointInfo([-40, -40], 1), PointInfo([40, -40], 1)]
    simpleSquare = GameObject(screen, [300, 150], pointData)
    simpleSquare2 = GameObject(screen, [400, 250], pointData)

    pointData2 = [PointInfo([500, 50], 1, isFixed=True), PointInfo([-300, 50], 1, isFixed=True), PointInfo([-300, 400], 1, isFixed=True),PointInfo([300, 400], 1, isFixed=True)]
    simpleFloor = GameObject(screen, [500, 300], pointData2)

    firstWheel = Wheel(screen, [500,0], 40, 10)
    firstWheel2 = Wheel(screen, [600,0], 40, 10)

    testPoint = PointMass(GameObject(screen, [0,0], []), PointInfo([0,0], 1))

    timeSinceStart = 0

    objects = [simpleFloor, firstWheel, simpleSquare, simpleSquare2, firstWheel2]
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        Input.updateKeyPress()
        screen.fill("white")

        # t = pygame.time.get_ticks()
        # Physics.delta = (t - timeSinceStart) / 1000.0
        # timeSinceStart = t
        
        screen.scroll()
        # RENDER YOUR GAME HERE
        for obj in objects:
            obj.update()
            obj.doCollisions(objects)

        testPoint.position = np.array(pygame.mouse.get_pos())
        lines = simpleFloor.getLines()
        lines2 = simpleSquare.getLines()
        pos, line, g = simpleFloor.getClosestLine(testPoint, lines)
        if(line != None):
            pygame.draw.line(screen, [255,0,0], line.end1.getPosition(), line.end2.getPosition(), 5)
            pygame.draw.circle(screen, [0,0,0], testPoint.getPosition(), 5)
            pygame.draw.circle(screen, [0,0,255], pos, 5)

        for line in lines2:
            line.doesIntersectRight(testPoint, screen)
        #lines[0].doesIntersectRight(testPoint, screen)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()