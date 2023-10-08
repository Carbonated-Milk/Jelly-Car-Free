import pygame
from GameSettings import *
from PointMass import *
from GameObject import *
import copy
from Input import Input
from Utility import *
import numpy as np
from LevelManager import LevelManager
from GameManager import *
from Wheel import *
from GameRunner import *

class LevelEditor:

    @staticmethod
    def runEditor(fileName):
        
        GameManager.initialize()

        Physics.active = False

        workPoints = []

        workModes = {'z' : WorkMode('standard', [255, 0, 100]),
                    'x' : WorkMode('floor', [0, 255, 100]),
                    'c' : WorkMode('car', [0, 0, 150])}
        
        pointModes = {'1' : PointDefault('standard', [0, 0, 255]),
                      '2' : PointDefault('Fixed', [255, 0, 0], PointInfo(isFixed=True))}
        
        currentWorkMode = workModes['z']
        currentPointMode = pointModes['1']

        displaySize = 5

        levelObjects = LevelManager.loadLevel(fileName)

        isSaved = True

        Singleton.runEditor = LevelEditor.runEditor
        
        Camera.setScreenOffset([0,0])

        while Singleton.running:

            GameManager.beginningStuff()

            Singleton.screen.fill('white')
            Utility.blitAlpha(lambda s : s.fill(currentWorkMode.color), 50)
            
            moveMult = 2 if Input.isKeyDown('shift') else 1
            Camera.moveScreenOffset(Input.getAxis(2 * moveMult))
            LevelEditor.drawGrid()

            if Input.isKeyDown('r'):
                Camera.setScreenOffset([0,0])

            for key in workModes.keys():
                if Input.isKeyDown(key):
                    if currentWorkMode == workModes[key]: continue
                    currentWorkMode = workModes[key]
                    workPoints = []
            
            for key in pointModes.keys():
                if Input.isKeyDown(key):
                    if currentPointMode == pointModes[key]: continue
                    currentPointMode = pointModes[key]

            if Input.mousePressed:
                isDelete = False
                for point in workPoints:
                    if Vector.getMagnitude(Input.mousePosReal - point.position, True) < displaySize**2:
                        workPoints.remove(point)
                        isDelete = True
                if not isDelete:
                    newPoint = copy.deepcopy(currentPointMode)
                    newPoint.setPosition(Input.mousePosReal)
                    workPoints.append(newPoint)
                if len(workPoints) == currentWorkMode.maxPoints:
                    workPoints.pop(0)

            for i in range(-1, len(workPoints) - 1):
                point = workPoints[i]
                nextpoint = workPoints[i + 1]
                pygame.draw.line(Singleton.screen, [0,0,0], Camera.reMap(point.position), Camera.reMap(nextpoint.position), displaySize)

            for point in workPoints:
                drawColor = point.color
                if Vector.getMagnitude(Input.mousePosReal - point.position, True) < displaySize**2: drawColor = [255,255,0]
                pygame.draw.circle(Singleton.screen, drawColor, Camera.reMap(point.position), displaySize)

            pygame.draw.circle(Singleton.screen, [0,255,0] if isSaved else [255,0,0], [15,15], 7.5)
            
            if Input.isKeyDown('enter') and len(workPoints) >= 3:
                levelObjects.append(GameObject([0,0], [p.pointInfo for p in workPoints]))
                workPoints = []
                isSaved = False

            for obj in levelObjects:
                obj.draw()

            if Input.isKeyDown('ctrl'):
                if Input.isKeyPressed('s') or Input.isKeyPressed('p') :
                    LevelManager.saveLevel(fileName, levelObjects)
                    isSaved = True
                    if Input.isKeyPressed('p') :
                        GameRunner.runLevel(fileName, True)

            if Input.isKeyPressed('q'):
                Settings.debugMode = not Settings.debugMode

            if Input.isKeyPressed('e'): 
                Singleton.levelSelect()
                break

            GameManager.endStuff()
            

    @staticmethod
    def drawGrid(spacing = 100):
        screenSize = Singleton.screenSize
        screenMiddle = Singleton.screenCenter
        camOffset = Camera.cameraOffset.copy()
        screenMiddleFloored = np.asarray(camOffset)
        screenMiddleFloored[0] = camOffset[0] % spacing #math.floor(camOffset[0] / spacing) * spacing
        screenMiddleFloored[1] = camOffset[1] % spacing #math.floor(camOffset[1] / spacing) * spacing

        for i in range(screenSize[1] // spacing + 2):
            yCoord =  -screenMiddleFloored[1] + spacing * i
            pygame.draw.line(Singleton.screen, [100,100,100], [screenMiddle[0] - screenSize[0]/2, yCoord],[screenMiddle[0] + screenSize[0]/2, yCoord], 2)

        for i in range(screenSize[0] // spacing + 2):
                    xCoord = -screenMiddleFloored[0] + spacing * i
                    pygame.draw.line(Singleton.screen, [100,100,100], [xCoord, camOffset[1] - screenSize[1]/2], [xCoord, camOffset[1] + screenSize[1]], 2)

class WorkMode():
     
    def __init__(self, name, color, maxPoints = 100):
        self.name = name
        self.color = color
        self.maxPoints = maxPoints

class PointDefault():
     
    def __init__(self, name, color, genericPointInfo = PointInfo()):
        self.name = name
        self.color = color
        self.pointInfo = genericPointInfo

    def setPosition(self, position):
        self.position = np.array(position)
        self.pointInfo.position = np.array(position)
        

if __name__ == '__main__':
    LevelEditor.runEditor('test.txt')
    