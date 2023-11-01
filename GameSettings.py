import numpy as np
import math
import pygame

class Settings:
    gravityConst = 10
    debugMode = True
    lineThickness = 10

class Physics:
    active = True
    delta = .1

class Vector:
    up = np.array([0,-1])
    down = np.array([0,1])
    right = np.array([1,0])
    left = np.array([-1,0])
    zero = np.array([0,0])

    rotate90 = np.array([[0,-1],[1,0]])

    @staticmethod
    def getRotMatrix(rad):
        cosRad = math.cos(rad)
        sinRad = math.sin(rad)
        return np.array([[cosRad,-sinRad],[sinRad,cosRad]])
    
    @staticmethod
    def addArrays(arrays):
        arraySum = np.array(arrays[0])
        for array in arrays[1:]:
            arraySum = arraySum + np.array(array)
        return arraySum.tolist()
    
    def getMagnitude(vec, returnSquared = False):
        calcVec = vec if isinstance(vec, np.ndarray) else np.array(vec)
        magnitude = np.dot(calcVec, calcVec)
        if not returnSquared: magnitude = magnitude ** 1/2
        return magnitude
    
    def arrayDist(array1, array2):
        a1 = np.array(array1)
        a2 = np.array(array2)
        a3 = a1 - a2
        return np.linalg.norm(a3)
    
    def project(v, u):
        return v * np.dot(u, v) / np.dot(v, v)

    def scalerProject(v,u):
        return np.dot(u, v) / np.dot(v, v)
            

    
class Singleton:
    screen = None
    screenSize = (1280, 720)
    screenCenter = (1280/2, 720/2)
    cameraScale = 1
    running = True
    clock = None
    activeObjects = []
    levelSelect = None
    runEditor = None
