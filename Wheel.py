from GameObject import GameObject 
import pygame
from Input import Input
import numpy
from GameSettings import *
import math
from PointMass import *
from Inflation import Inflation

class Wheel(GameObject, Inflation):
    accel = .5

    def __init__(self, position, radius, count, frictionConst= 0.5):
        pointarray = []
        for i in range(count):
            angle =  2 * np.pi * i / count
            pointarray.append(PointInfo([math.cos(angle) * radius, math.sin(angle) * radius], 1))

        super().__init__(position, pointarray, frictionConst)
        super().setInflation(5)

    def update(self):
        if(Input.isKeyPressed('a')):
            self.torque(-1)
        if(Input.isKeyPressed('d')):
            self.torque(1)
        super().update()
        super().doInflation(self.points)
        #Singleton.cameraOffset = self.getPosition()

    def torque(self, direction):
        for point in self.points:
                relPos = point.position - self.position
                movePos = np.matmul(Vector.rotate90, relPos)
                point.addForce(movePos * self.accel * Physics.delta * direction)

