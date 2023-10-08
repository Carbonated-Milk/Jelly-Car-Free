from GameManager import *
from GameSettings import *
from Input import *
from LevelManager import *
from GameObject import *

class GameRunner:

    @staticmethod
    def runLevel(fileName):
        GameManager.initialize()
        Physics.active = True

        Singleton.activeObjects = LevelManager.loadLevel(fileName)

        while Singleton.running:
            GameManager.beginningStuff()
            
            Singleton.screen.fill('white')
            for obj in Singleton.activeObjects:
                obj.update()

            if Input.isKeyPressed('e'): 
                Singleton.levelSelect()
                break

            GameManager.endStuff()


