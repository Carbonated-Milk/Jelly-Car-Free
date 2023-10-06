from PointMass import *
import pygame
import numpy as np
from operator import add
from Frame import *

class GameObject:

    # def __init__(self, pointInfo, frictionConst = .5):
    #     self.__init__([0,0], pointInfo, frictionConst = .5)

    def __init__(self, position, pointInfo, frictionConst = .5):
        self.pointInfo = pointInfo
        self.points = []
        self.position = np.array(position)
        self.points = self.setUpPoints(pointInfo)

        self.frictionConst = frictionConst
        self.topRight = self.getPosition()
        self.bottomLeft = self.getPosition()

        self.color = np.random.randint(0,255, 3).tolist() + [0.5]

        self.frame = Frame(self, pointInfo)

    def subDivide(self, pointInfo, subdivide = 1):
        if len(pointInfo) == 0: return []
        for s in range(subdivide):
            for i in range(len(pointInfo) - 1, 0, -1):
                pointInfo.insert(i, PointInfo((np.add(np.array(pointInfo[i].position), np.array(pointInfo[i - 1].position))/2).tolist()))
            pointInfo.insert(0, PointInfo((np.add(np.array(pointInfo[0].position), np.array(pointInfo[- 1].position))/2).tolist()))
        return pointInfo

    def setUpPoints(self, pointInfo):

        newPoints = [PointMass(self, info) for info in pointInfo]

        for i in range(len(newPoints) - 1):
            for j in range(i + 1, len(newPoints)):
                newPoints[i].addConnection(newPoints[j])

        return newPoints

    def update(self):
        self.simulateAll()
        self.frame.update()
        self.draw()

    def simulateAll(self):
        self.calcBoundingBox()
        
        self.position = self.getCenter()

        for point in self.points:
            point.simulate()

    def getCenter(self):
        positionSum = np.array([0,0])
        for point in self.points:
            positionSum = np.add(positionSum, point.position)
        if(Settings.debugMode):pygame.draw.circle(Singleton.screen, [0,255,0], Singleton.reMap(self.position.tolist()), 5)
        return positionSum / len(self.points)
            
    def draw(self):
        surface = Singleton.screen
        points = []
        for i in range(len(self.points)):
            points.append(self.points[i].getPosition())
            if(Settings.debugMode): 
                pygame.draw.line(surface, [0,255, 255], Singleton.reMap(self.points[i].getPosition()), Singleton.reMap(np.add(self.points[i].position, self.points[i].velocity).tolist()), 5)
                for connection in self.points[i].connections:
                    pygame.draw.line(surface, [255, 0, 0], Singleton.reMap(self.points[i].getPosition()), Singleton.reMap(connection.otherPoint.getPosition()))
        if(Settings.debugMode):
            pygame.draw.lines(surface, [0,0,0], True, Singleton.reMap(points), 5)
            pygame.draw.polygon(surface, [0,255,0], Singleton.reMap([self.topRight, [self.topRight[0], self.bottomLeft[1]], self.bottomLeft, [self.bottomLeft[0], self.topRight[1]]]), 3)
        else:
            thickness = Settings.lineThickness
            pygame.draw.polygon(surface, self.color, Singleton.reMap(points), 0)
            pygame.draw.lines(surface, [0,0,0], True, Singleton.reMap(points), thickness)
            for point in points:
                pygame.draw.circle(surface, [0,0,0], Singleton.reMap(point), thickness/2)

    def getTotalMass(self):
        sum = 0
        for point in self.points:
            sum += point.mass
        return sum
    
    def doCollisions(self, objects):
        for obj in objects:
            if obj is self: continue
            if not self.inBoundingBox(obj): continue
            self.collision(obj)

    def collision(self, otherObject):

        lines = otherObject.getLines()

        for point in self.points:
            if self.isInside(point, lines):
                closestPos, closestLine, moveVec = self.getClosestLine(point, lines)
                lerpPos = (point.getPosition()[0] - closestLine.end1.getPosition()[0]) / (closestLine.end2.getPosition()[0] - closestLine.end1.getPosition()[0] + .001)
                
                totalMass = point.mass + closestLine.end1.mass + closestLine.end2.mass

                moveVec2 = closestPos - point.position
                closestLine.end1.move(-moveVec2/2)# * (1 - closestLine.end1.mass / totalMass) * lerpPos)
                closestLine.end2.move(-moveVec2/2)# * (1 - closestLine.end2.mass / totalMass) * (1 - lerpPos))
                point.move(moveVec2/2)# * (1 - point.mass / totalMass))
                point.velocity = Vector.zero
                avgVel = np.add(closestLine.end1.velocity, closestLine.end2.velocity)/2
                relVel = np.add(point.velocity, -avgVel)
                avgFric = (self.frictionConst + otherObject.frictionConst)/2
                projVel = -closestLine.projectOnLine(relVel) * avgFric
                # point.addForce(projVel)
                # closestLine.end1.addForce(-projVel)
                # closestLine.end2.addForce(-projVel)

                #closestLine.end1.addAcceleration(point.velocity)
                #closestLine.end2.addAcceleration(point.velocity)
                #point.addAcceleration(-avgVel)

    def calcBoundingBox(self):
        topRight = self.position.tolist()
        bottomLeft = self.position.tolist()
        for point in self.points:
            position = point.getPosition()
            if(position[0] > topRight[0]): topRight[0] = position[0]
            elif(position[0] < bottomLeft[0]): bottomLeft[0] = position[0]
            if(position[1] > topRight[1]): topRight[1] = position[1]
            elif(position[1] < bottomLeft[1]): bottomLeft[1] = position[1]
        self.topRight = topRight
        self.bottomLeft = bottomLeft

    def inBoundingBox(self, other):
        for point in [self.topRight, [self.topRight[0], self.bottomLeft[1]], self.bottomLeft, [self.bottomLeft[0], self.topRight[1]]]:
            if(other.bottomLeft[0] <= point[0] and point[0] <= other.topRight[0]):
                if(other.bottomLeft[1] <= point[1] and point[1] <= other.topRight[1]):
                    return True
        return False

    
    def isInside(self, point, lines):
        return self.countInterSections(point, lines) % 2 != 0

    def countInterSections(self, point, lines):
        numInterSects = 0
        for line in lines:
            if line.doesIntersectRight(point): numInterSects += 1
        #if(numInterSects > 0): print(numInterSects)
        return numInterSects
        
    def getLines(self):
        lines = []
        for i in range(len(self.points) - 1):
            lines.append(Line(self.points[i], self.points[i+1]))
        lines.append(Line(self.points[-1], self.points[0]))
        return lines
    
    def getClosestLine(self, point, lines):
        closest = 2**100
        closestLine = None
        closestPos = None
        realDist = 10*15
        moveVec = None
        lastOnLine = False

        for line in lines:
            closePos, dist, moveVec, newRealDist, onLine = line.projectPointOnLine(point)
            if dist < closest: #lastOnLine and not onLine and newRealDist < closest or lastOnLine and onLine and dist < closest or not lastOnLine and onLine and dist < realDist or not lastOnLine and not onLine and newRealDist < realDist:# and newRealDist < realDist): 
                closest = dist
                closestLine = line
                realDist = newRealDist
                closestPos = closePos
                lastOnLine = onLine
        return closestPos, closestLine, moveVec

    def getPosition(self):
        return self.position.tolist()
    
    def __repr__(self) -> str:
        return f'GameObject({self.position.tolist()}, {self.pointInfo.__repr__()}, {self.frictionConst})'

class Line:
    def __init__(self, end1, end2):
        self.end1 = end1
        self.end2 = end2

    def doesIntersectRight(self, point, screen = None):
        pos1 = self.end1.getPosition()
        pos2 = self.end2.getPosition()
        checkPos = point.getPosition()

        dif1 = pos1[1] - checkPos[1] #check that y's are the around the point
        dif2 = pos2[1] - checkPos[1]
        if np.sign(dif1) == np.sign(dif2):return False

        interpVal = np.abs(dif1 / (dif1 - dif2))
        if(dif1 > 0): interpVal = 1 - interpVal
        if(pos2[1] > pos1[1]):interpVal = 1 - interpVal
        xVal = (pos1[0] - pos2[0]) * interpVal + pos2[0]
        
        if xVal <= checkPos[0]: return False

        if(screen != None):
            pygame.draw.circle(screen, [255,50, 255], Singleton.reMap([xVal, checkPos[1]]), 5)

        return True
    
    def projectOnLine(self, vel):
        direction = self.end1.getDirection(self.end2)
        projectedDirection = np.dot(vel, direction) / np.dot(direction, direction) * direction
        if np.dot(vel, direction) < 0: projectedDirection = -projectedDirection
        return projectedDirection
    
    def projectPointOnLine(self, point):
        direction = self.end1.getDirection(self.end2)
        relDirection = self.end1.getDirection(point)
        projectedDirection = np.dot(relDirection, direction) / np.dot(direction, direction) * direction
        projPos = np.add(projectedDirection, self.end1.getPosition())
        #if np.dot(projectedDirection, projectedDirection) > np.dot(direction,direction): return None Should be fine without
        dif1 = self.end1.getPosition()[1] - projPos[1] #check that y's are the around the point
        dif2 = self.end2.getPosition()[1] - projPos[1]
        realDist = np.linalg.norm(point.position - projPos)
        
        wasOnLine = True
        if(np.sign(dif1) == np.sign(dif2)): 
            realDist = min(self.end1.getDist(point), self.end2.getDist(point))
            wasOnLine == False

        return projPos, np.linalg.norm(point.position - projPos), projPos - point.position, realDist, wasOnLine
