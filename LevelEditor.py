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
        selectedPoints = []
        startMousePos = [-100,-100]

        workModes = {'z' : WorkMode('standard', [255, 0, 100]),
                    'x' : WorkMode('edit', [0, 255, 100]),
                    'c' : WorkMode('delete', [0, 0, 150], removePoints = True)}
        
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
            
            LevelEditor.editorBackground()

            #Handes Edit Modes
            for key in workModes.keys():
                if Input.isKeyDown(key):
                    if currentWorkMode == workModes[key]: continue
                    currentWorkMode = workModes[key]
                    if currentWorkMode.removePoints: workPoints = []
                    selectedPoints = []
            
            for key in pointModes.keys():
                if Input.isKeyDown(key):
                    if currentPointMode == pointModes[key]: continue
                    currentPointMode = pointModes[key]

            #Does stuff
            
            match currentWorkMode.name:
                case 'standard':
                    if Input.mousePressed:
                        isDelete = False
                        clickedPoints = getClickedPoints()
                        for point in clickedPoints:
                            workPoints.remove(point)
                            isDelete = True
                        if not isDelete:
                            newPoint = copy.deepcopy(currentPointMode)
                            newPoint.setPosition(Input.mousePosReal)
                            workPoints.append(newPoint)
                        if len(workPoints) == currentWorkMode.maxPoints:
                            workPoints.pop(0)
                case 'edit':
                    if Input.mousePressed:
                        startMousePos = Input.mousePos
                    if not Input.mouseDown:
                        if Vector.arrayDist(Input.mousePos, startMousePos) < displaySize:
                            addPointsToSelected(selectedPoints, getClickedPoints())
                        else: 
                            pass #find points inside box
                        #add some kind of g grab and move
                        #this code is starting to look really messy
                case 'delete':
                    #point = PointMass()
                    #pass delete point that its on
                    pass

            def addPointsToSelected(selectedPoints, points):
                if not Input.isKeyDown('shift'):
                    selectedPoints = []
                if isinstance(points, list):
                    for p in points:
                        if p not in selectedPoints:
                            selectedPoints.append(p)
                    return selectedPoints
                if p in points:
                    selectedPoints.remove(p)
                else: selectedPoints.append(p)
                return selectedPoints


            def getClickedPoints():
                returnPoints = []
                for point in workPoints:
                    if Vector.getMagnitude(Input.mousePosReal - point.position, True) < displaySize**2:
                        returnPoints.append(point)
                return returnPoints
                                
                        
            for i in range(-1, len(workPoints) - 1):
                point = workPoints[i]
                nextpoint = workPoints[i + 1]
                pygame.draw.line(Singleton.screen, [0,0,0], Camera.reMap(point.position), Camera.reMap(nextpoint.position), displaySize)

            for point in workPoints:
                drawColor = point.color
                if Vector.getMagnitude(Input.mousePosReal - point.position, True) < displaySize**2 or point in selectedPoints: drawColor = [255,255,0]
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
                    levelObjects.sort(key=lambda obj: obj.offset)
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
    def editorBackground():
        shiftMult = 2 if Input.isKeyDown('shift') else 1
        Camera.moveScreenOffset(Input.getAxis(2 * shiftMult * Camera.camSize))
        LevelEditor.drawGrid()

        if Input.isKeyPressed('+') :
            Camera.scaleTargetCameraSize(1.3, shiftMult)
        if Input.isKeyPressed('-') :
            Camera.scaleTargetCameraSize(1/1.3, shiftMult)

        if Input.isKeyDown('r'):
            Camera.setScreenOffset([0,0])
            Camera.setTargetCameraSize(1)

    @staticmethod
    def drawGrid(spacing = 100):
        topLeft, bottomRight = Camera.inverseReMap([[0,0], Singleton.screenSize])
        topLeft = np.array(topLeft)
        bottomRight = np.array(bottomRight)
        flooredTopLeft = topLeft/spacing//1 * spacing
        number = (bottomRight - topLeft) // spacing

        for i in range(int(number[1]) + 2):
            yCoord =  flooredTopLeft[1] + spacing * i
            pygame.draw.line(Singleton.screen, [100,100,100], Camera.reMap([topLeft[0], yCoord]),Camera.reMap([bottomRight[0], yCoord]), 2)

        for i in range(int(number[0]) + 2):
            xCoord = flooredTopLeft[0] + spacing * i
            pygame.draw.line(Singleton.screen, [100,100,100], Camera.reMap([xCoord, topLeft[1]]), Camera.reMap([xCoord, bottomRight[1]]), 2)

class WorkMode():
     
    def __init__(self, name, color, maxPoints = 100, removePoints = False):
        self.name = name
        self.color = color
        self.maxPoints = maxPoints
        self.removePoints = removePoints


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
    