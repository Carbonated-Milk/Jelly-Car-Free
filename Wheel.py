from GameObject import GameObject 
import pygame
from Input import Input
import numpy
from GameSettings import *
import math
from PointMass import *
from Inflation import Inflation
from Camera import Camera

class Wheel(GameObject, Inflation):
    accel = .5

    def __init__(self, position, radius, count, frictionConst= 0.5):
        pointarray = []
        self.radius = radius
        for i in range(count):
            angle =  2 * np.pi * i / count
            pointarray.append(PointInfo([math.cos(angle) * radius, math.sin(angle) * radius], 1))

        super().__init__(position, pointarray, frictionConst)
        super().setInflation(5)

    def update(self):
        if(Input.isKeyDown('a')):
            self.torque(-1)
        if(Input.isKeyDown('d')):
            self.torque(1)
        super().update()
        super().doInflation(self.points)
        Camera.setTargetOffset(self.position)

    def torque(self, direction):
        for point in self.points:
                relPos = point.position - self.position
                movePos = np.matmul(Vector.rotate90, relPos)
                point.addForce(movePos * self.accel * Physics.delta * direction)

    def __repr__(self):
        return f'Wheel({self.position.tolist()}, {self.radius}, {len(self.points)})'

