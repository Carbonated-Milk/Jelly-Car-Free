from GameManager import *
from GameSettings import *
from Input import *
from LevelManager import *
from GameObject import *

class GameRunner:

    @staticmethod
    def runLevel(fileName, inEditMode = False):
        GameManager.initialize()
        Physics.active = True

        Singleton.activeObjects = LevelManager.loadLevel(fileName)

        while Singleton.running:
            GameManager.beginningStuff()
            
            Singleton.screen.fill('white')
            for obj in Singleton.activeObjects:
                obj.update()

            if Input.isKeyDown('e'): 
                Singleton.runEditor(fileName) if inEditMode else Singleton.levelSelect()
                break

            if inEditMode and Input.isKeyPressed('q'):
                Settings.debugMode = not Settings.debugMode

            GameManager.endStuff()


