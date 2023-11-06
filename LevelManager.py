from GameObject import *
from Wheel import *
import os
from Car import *


class LevelManager:
    folderName = "Levels/"

    @staticmethod
    def getAllLevels():
        fileNames = os.listdir(LevelManager.folderName)
        return fileNames

    @staticmethod
    def loadLevel(fileName):
        fileLocation = LevelManager.folderName + fileName
        try:
            with open(fileLocation, "x") as levelFile:
                print("new level file created")
                return
        except:
            pass

        levelObjs = []

        with open(fileLocation, "r") as levelFile:
            for line in levelFile.readlines():
                levelObjs.append(eval(line.replace("\n", "")))

        return levelObjs

    @staticmethod
    def saveLevel(fileName, objects):
        fileLocation = LevelManager.folderName + fileName
        try:
            with open(fileLocation, "x") as levelFile:
                print("new level file created")
        except:
            pass

        with open(fileLocation, "w") as levelFile:
            for obj in objects:
                levelFile.write(obj.__repr__() + "\n")


if __name__ == "__main__":
    Singleton.screen = pygame.Surface([500, 1])
    for thing in LevelManager.loadLevel(LevelManager.getAllLevels()[2]):
        print(thing)
