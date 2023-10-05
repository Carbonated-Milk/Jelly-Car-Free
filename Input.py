import pygame
import keyboard

class Input:
    keys = {}

    usedKeys = ['w', 'a', 's', 'd']

    @staticmethod
    def updateKeyPress():
        for k in Input.usedKeys:
            Input.keys[k] = keyboard.is_pressed(k)

    @staticmethod
    def isKeyPressed(key):
        return Input.keys[key]