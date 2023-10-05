import numpy as np
import math
import pygame

class Settings:
    gravityConst = 20
    debugMode = True
    lineThickness = 10

class Physics:
    delta = .1

class Vector:
    up = np.array([0,-1])
    down = np.array([0,1])
    right = np.array([1,0])
    left = np.array([-1,0])
    zero = np.array([0,0])

    rotate90 = np.array([[0,-1],[1,0]])

    def getRotMatrix(rad):
        cosRad = math.cos(rad)
        sinRad = math.sin(rad)
        return np.array([[cosRad,-sinRad],[sinRad,cosRad]])
    
class Singleton:
    screen = None