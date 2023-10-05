import numpy as np
from GameSettings import *
import pygame

class PointMass:

    damping = .1

    def __init__(self, parent, pointInfo):
        self.isFixed = pointInfo.isFixed
        self.velocity = np.array([0,0])
        self.mass = pointInfo.mass
        self.parent = parent
        self.position = pointInfo.position + parent.position
        self.strength = pointInfo.strength
        self.connections = []

    
    def addForce(self, forceVector):
       self.addAcceleration(forceVector / self.mass)

    def addAcceleration(self, accelerationVector):
        self.velocity = np.add(self.velocity, accelerationVector)

    def simulate(self):
        if(self.isFixed): 
            self.velocity = Vector.zero
            return

        self.velocity = np.add(self.velocity, Vector.down * Settings.gravityConst * Physics.delta) #gravity

        for connection in self.connections:
            correctionConst = (connection.distance - self.getDist(connection.otherPoint))
            correctionVel = self.getDirection(connection.otherPoint, True) * -correctionConst * self.strength * Physics.delta * 4

            #if np.dot(self.velocity, correctionVel > 0): correctionVel *= self.damping
            self.velocity = np.add(self.velocity, correctionVel)
            if not connection.otherPoint.isFixed: connection.otherPoint.velocity = np.add(connection.otherPoint.velocity, -correctionVel)

        self.position = np.add(self.position, self.velocity * Physics.delta)

    def addConnection(self, otherPoint, strenght = 1):
        distance = self.getDist(otherPoint)
        self.connections.append(PointConnection(otherPoint, distance, strenght))
        otherPoint.connections.append(PointConnection(self, distance, strenght))

    def getDist(self, otherPoint):
        return np.linalg.norm(self.position - otherPoint.position)
    
    def getDirection(self, otherPoint, isNormal = False):
        directionVec = otherPoint.position - self.position
        if isNormal: directionVec = directionVec / np.linalg.norm(directionVec)
        return directionVec
        
    def getPosition(self):
        return self.position.tolist()
    
    def move(self, vector):
        if(self.isFixed): return
        self.position = np.add(self.position, vector)
    
class PointInfo:
    def __init__(self, position, mass = 1, isFixed = False, strength = 1):
        self.position = position
        self.mass = mass
        self.isFixed = isFixed
        self.strength = strength

class PointConnection:
    def __init__(self, otherPoint, distance, strength = 1):
        self.otherPoint = otherPoint
        self.distance = distance
        self.strength = strength