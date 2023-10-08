from PointMass import *
from GameSettings import *
import pygame
import copy
from Camera import *

class Frame:

    def __init__(self, parent, pointInfo, pullStrength = 1):
        self.parent = parent
        self.pullStrength = pullStrength
        self.position = parent.position
        self.framePoints = self.createFramePoints(pointInfo)


    def createFramePoints(self, pointInfos):
        framePoints = []
        for pointInfo in pointInfos:
            framePoints.append(FramePoint(pointInfo, self))
        return framePoints
    
    def update(self):
        self.position = self.parent.getCenter()
        for point in self.framePoints:
            point.position = np.add(point.relPos, self.position)
        rot = self.getAvgAngle()
        self.addForceToPoints(rot)

    def getAvgAngle(self):
        return 0
        sumAngles = 0
        for point, framePoint in zip(self.parent.points, self.framePoints):
            vecP = np.add(point.position, -self.position)
            vecPF = framePoint.relPos
            if Settings.debugMode:pygame.draw.lines(Singleton.screen, [255,0,0], False, Camera.reMap([point.getPosition(), self.position.tolist(), framePoint.getPosition()]))
            try: addAngle = math.acos(np.dot(vecP, vecPF) / (np.linalg.norm(vecP) * np.linalg.norm(vecPF)))
            except: pass
            if(np.dot(np.matmul(Vector.rotate90,vecPF), vecP) < 0): addAngle = 2 * np.pi - addAngle
            sumAngles += addAngle
        return sumAngles / len(self.framePoints)
    
    def addForceToPoints(self, angleRad):
        if not Physics.active: return
        radMat = Vector.getRotMatrix(angleRad)
        rotpoints = []
        for point, framePoint in zip(self.parent.points, self.framePoints):
            pointTransformed = np.add(np.matmul(radMat, framePoint.relPos), self.position)
            rotpoints.append(pointTransformed)
            correctionVec = np.add(pointTransformed, -point.position)
            #point.addForce(correctionVec)
        
        if Settings.debugMode: pygame.draw.polygon(Singleton.screen,[255, 0, 255], Camera.reMap(rotpoints), 7)

class FramePoint:

    def __init__(self, pointInfo, parent):
        self.relPos = pointInfo.position + parent.position - parent.parent.getCenter()
        self.position = np.array([0,0])

    def getPosition(self):
        return self.position.tolist()