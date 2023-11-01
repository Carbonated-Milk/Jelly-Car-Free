import pygame
from GameObject import *
from PointMass import *
import numpy as np
from Wheel import Wheel
from Input import Input
from GameManager import GameManager
from Car import Car

class GameRunner:

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Singleton.screen = screen
    Singleton.screen = screen
    clock = pygame.time.Clock()
    running = True
    center = (1280/2, 720/2)
    GameManager.initialize()


    pointData = [PointInfo([100, 40], 1), PointInfo([-40, 40], 1), PointInfo([-40, -40], 1), PointInfo([40, -40], 1)]
    simpleSquare = GameObject( [300, 150], pointData)
    simpleSquare2 = GameObject( [400, 250], pointData)

    pointData2 = [PointInfo([500, 50], 1, isFixed=True), PointInfo([-300, 50], 1, isFixed=True), PointInfo([-300, 400], 1, isFixed=True),PointInfo([300, 400], 1, isFixed=True)]
    simpleFloor = GameObject( [500, 300], pointData2)
    simpleFloor2 = GameObject( [1500, 400], pointData2)
    car = Car([800,100])

    firstWheel = Wheel( [500,0], 40, 10)
    firstWheel2 = Wheel( [600,0], 40, 10)

    testPoint = PointMass(GameObject( [0,0], []), PointInfo([0,0], 1))

    timeSinceStart = 0
    time = 0
    [Singleton.activeObjects.append(i) for i in [simpleFloor, simpleFloor2, car]]
    while Singleton.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Singleton.running = False

        # fill the screen with a color to wipe away anything from last frame
        Input.updateKeyPress()
        Singleton.screen.fill("white")

        # t = pygame.time.get_ticks()
        # Physics.delta = (t - timeSinceStart) / 1000.0
        # timeSinceStart = t

        # RENDER YOUR GAME HERE
        for obj in Singleton.activeObjects:
            obj.update()

        Camera.setScreenOffset([pygame.mouse.get_pos()[0], 0])

        if(time < pygame.time.get_ticks()):
            time += 3000
            #Singleton.activeObjects.append(GameObject([500, -100], pointData))

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
        lines[0].doesIntersectRight(testPoint, screen)
        #flip() the display to put your work on screen
        pygame.display.flip()
        Singleton.clock.tick(60)
        #clock.tick(60)  # limits FPS to 60

    pygame.quit()