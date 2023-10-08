from GameManager import *
from LevelManager import *
import numpy as np
from GameRunner import *
from LevelEditor import *


class LevelSelect:

    iconsPerRow = 4
    spacing = (100, 100)

    @staticmethod
    def runLevelSelect():
        GameManager.initialize()
        Singleton.screen.fill("cyan")
        Singleton.levelSelect = LevelSelect.runLevelSelect
        

        levelIcons = [LevelIcon(fileName) for fileName in LevelManager.getAllLevels()]

        for i in range(len(levelIcons)):
            row = i // LevelSelect.iconsPerRow
            col = i % LevelSelect.iconsPerRow
            halfWay = (LevelSelect.iconsPerRow - 1) / 2
            pos = np.array([LevelSelect.spacing[0] * (col - halfWay), LevelSelect.spacing[1] * (row - halfWay)])
            levelIcons[i].position = np.array(Singleton.screenCenter) + pos
            levelIcons[i].color = [255 / len(levelIcons) * i] * 3

        while Singleton.running:
            GameManager.beginningStuff()

            for icon in levelIcons:
                if icon.checkPressed():
                    if(Input.isKeyDown('ctrl')):
                        LevelEditor.runEditor(icon.fileName)
                    else:
                        GameRunner.runLevel(icon.fileName)
                    break
                icon.draw()
            
            GameManager.endStuff()


class LevelIcon:

    size = 30

    def __init__(self, fileName):
        self.fileName = fileName
        self.position = np.array([0,0])
        self.color = [100,100,100]

    def draw(self):
        pygame.draw.circle(Singleton.screen, self.color, self.position, LevelIcon.size)

    def checkPressed(self):
        if Vector.getMagnitude(Vector.addArrays([Input.mousePos, -self.position]), True) < LevelIcon.size**2:
            return Input.mousePressed
        
    
if __name__ == '__main__':
    LevelSelect.runLevelSelect()