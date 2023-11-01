import numpy as np
from GameSettings import *
from Camera import *
class Inflation:
    pressure = 500

    def setInflation(self, inflation):
        self.inflation = inflation

    def doInflation(self, points):
        area = self.getArea()
        inflationMult = self.pressure / area

        for i in range(len(points)):
            pointLeft = points[i - 1]
            pointCenter = points[i]
            pointRight = points[i + 1] if i + 1 != len(points) else points[0]

            vec = self.points[i].position - self.position
            normal = vec/np.linalg.norm(vec) * self.inflation
            print('run')
            if Settings.debugMode : pygame.draw.line(Singleton.screen, [0,20,0], Camera.reMap(pointCenter.getPosition()), Camera.reMap((pointCenter.position + normal * inflationMult).tolist()), 10)
            pointCenter.addForce(normal * inflationMult)

    def getArea(self):
        area = 0
        for i in range(len(self.points)):
            dist1 = self.points[i-1].getDist(self.points[i])
            dist2 = np.linalg.norm((self.points[i-1].position - self.position))
            area += dist1 * dist2
        return area / 2