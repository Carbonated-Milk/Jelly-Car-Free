import pygame
import keyboard
import numpy as np
from GameSettings import Vector
from GameSettings import Singleton

class Input:
    keys = {}
    singleKeys = 'abcdefghijklmnopqrstuvwxyz0123456789'
    specialKeys = ['enter', 'ctrl']
    usedKeys = [k for k in singleKeys] + specialKeys

    @staticmethod
    def updateInput():
        Input.updateKeyPress()
        Input.mouseUpdate()

    @staticmethod
    def updateKeyPress():
        for k in Input.usedKeys:
            Input.keys[k] = keyboard.is_pressed(k)

    mousePressed = False
    mouseDown = False

    mousePos = Vector.zero
    mousePosReal = Vector.zero

    def mouseUpdate():
        Input.mousePos = np.array(pygame.mouse.get_pos())
        Input.mousePosReal = Vector.addArrays([Input.mousePos, -np.array(Singleton.screenCenter), Singleton.cameraOffset])
        
        if pygame.mouse.get_pressed(3)[0]:
            Input.mousePressed = not Input.mouseDown
            Input.mouseDown = True
        else:
            Input.mousePressed = False
            Input.mouseDown = False

    @staticmethod
    def isKeyPressed(key):
        return Input.keys[key]
    
    @staticmethod
    def getAxis(mult = 1):
        axis = [0,0]
        if Input.isKeyPressed('a'): axis[0] -= mult
        if Input.isKeyPressed('d'): axis[0] += mult
        if Input.isKeyPressed('s'): axis[1] -= mult
        if Input.isKeyPressed('w'): axis[1] += mult
        return axis