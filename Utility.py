from Input import Input
from GameSettings import *

class Utility:

    @staticmethod
    def keyUpdate():
        Input.updateInput()

    @staticmethod
    def blitAlpha(drawFunc, alpha):
        s = pygame.Surface(Singleton.screenSize)  # the size of your rect
        s.set_alpha(alpha)                # alpha level
        drawFunc(s)          # this fills the entire surface
        Singleton.screen.blit(s, (0,0))