import pygame
import keyboard
import numpy as np
from GameSettings import Vector
from GameSettings import Singleton
from Camera import *

class Input:
    keys = {}
    singleKeys = 'abcdefghijklmnopqrstuvwxyz0123456789'
    specialKeys = ['enter', 'ctrl', 'shift']
    usedKeys = [k for k in singleKeys] + specialKeys

    @staticmethod
    def updateInput():
        Input.updateKeyPress()
        Input.mouseUpdate()

    @staticmethod
    def updateKeyPress():
        for k in Input.usedKeys:
            isPressed = keyboard.is_pressed(k) and not Input.keys[k][1]
            Input.keys[k] = [isPressed, keyboard.is_pressed(k)]

    mousePressed = False
    mouseDown = False

    mousePos = Vector.zero
    mousePosReal = Vector.zero

    def mouseUpdate():
        Input.mousePos = np.array(pygame.mouse.get_pos())
        Input.mousePosReal = Vector.addArrays([Input.mousePos, -np.array(Singleton.screenCenter), Camera.cameraOffset])
        
        if pygame.mouse.get_pressed(3)[0]:
            Input.mousePressed = not Input.mouseDown
            Input.mouseDown = True
        else:
            Input.mousePressed = False
            Input.mouseDown = False

    
    @staticmethod
    def isKeyPressed(key):
        return Input.keys[key][0]

    @staticmethod
    def isKeyDown(key):
        return Input.keys[key][1]
    
    @staticmethod
    def getAxis(mult = 1):
        axis = [0,0]
        if Input.isKeyDown('a'): axis[0] -= mult
        if Input.isKeyDown('d'): axis[0] += mult
        if Input.isKeyDown('s'): axis[1] -= mult
        if Input.isKeyDown('w'): axis[1] += mult
        return axis