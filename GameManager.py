import pygame
from GameSettings import *
from Input import Input
from Camera import *
class GameManager:

    setUp = False

    @staticmethod
    def initialize():
        if GameManager.setUp : return
        pygame.init()
        Singleton.screenSize = (1280, 720)
        Singleton.screen = pygame.display.set_mode(Singleton.screenSize)
        Singleton.clock = pygame.time.Clock()
        Singleton.screenCenter = (1280/2, 720/2)
        GameManager.setUp = True

    @staticmethod
    def checkRun():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Singleton.running = False

    @staticmethod
    def endStuff():
        pygame.display.flip()
        Singleton.clock.tick(60)  # limits FPS to 60

    # @staticmethod
    # def updateDelta():

    
    @staticmethod
    def beginningStuff():
        GameManager.checkRun()
        Input.updateInput()
        Camera.cameraUpdate()