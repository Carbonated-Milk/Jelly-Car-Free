import pygame
from GameObject import *
from PointMass import *
from Input import Input

class GameRungner:

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Singleton.screen = screen
    clock = pygame.time.Clock()
    running = True


    pointData = [PointInfo([50, 50], 1), PointInfo([-50, 50], 1), PointInfo([-50, -50], 1,isFixed=False), PointInfo([50, -50], 1)]
    simpleSquare = GameObject([600, 0], pointData)
    simpleSquare2 = GameObject([500, 350], pointData)
    simpleSquare3 = GameObject([550, 200], pointData)
    simpleSquare4 = GameObject([400, 300], pointData)

    pointData2 = [PointInfo([500, 50], 1, isFixed=True), PointInfo([-500, 50], 1, isFixed=True), PointInfo([-300, 400], 1, isFixed=True),PointInfo([300, 400], 1, isFixed=True)]
    simpleFloor = GameObject([500, 450], pointData2)

    objects = [simpleFloor, simpleSquare, simpleSquare2,simpleSquare3,simpleSquare4]

    time = 0

    bg = pygame.image.load("Paper.jpg")
    bgScaled = pygame.transform.scale(bg, (1280, 720))
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        Input.updateKeyPress()

        screen.fill("white")
        screen.blit(bgScaled, (0, 0))
        
        # RENDER YOUR GAME HERE
        for obj in objects:
            obj.update(screen)
            obj.doCollisions(objects)

        if(time < pygame.time.get_ticks()):
            time += 3000
            objects.append(GameObject([500, -100], pointData))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()