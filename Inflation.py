import numpy as np
from GameSettings import *
from Camera import *
class Inflation:
    
    def setInflation(self, inflation):
        self.inflation = inflation

    def doInflation(self, points):
        for i in range(len(points)):
            pointLeft = points[i - 1]
            pointCenter = points[i]
            pointRight = points[i + 1] if i + 1 != len(points) else points[0]

            vecLeft = pointCenter.getDirection(pointLeft, True)
            vecRight = pointCenter.getDirection(pointRight, True)
            normal = -np.matmul(Vector.rotate90, (vecRight - vecLeft) / np.linalg.norm(vecRight - vecLeft)) * self.inflation

            if Settings.debugMode : pygame.draw.line(Singleton.screen, [100,100,100], Camera.reMap(pointCenter.getPosition()), Camera.reMap((pointCenter.position + normal).tolist()), 5)
            pointCenter.addForce(normal)