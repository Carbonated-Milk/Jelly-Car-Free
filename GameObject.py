from PointMass import *
import pygame
import numpy as np
from operator import add
from Frame import *
from Camera import *

class GameObject:

    def __init__(self, position, pointInfo, frictionConst = .5, offset = 0):
        self.offset = offset

        self.pointInfo = pointInfo
        self.points = []
        self.position = np.array(position)
        self.points = self.setUpPoints(pointInfo)

        self.frictionConst = frictionConst
        self.topRight = self.getPosition()
        self.bottomLeft = self.getPosition()

        self.color = np.random.randint(0,255, 3).tolist() + [0.5]

        self.frame = Frame(self, pointInfo)

        self.tag = None
        self.noCollide = []

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
        self.doCollisions(Singleton.activeObjects)
        self.frame.update()
        self.draw()

    def simulateAll(self):
        self.calcBoundingBox()
        
        self.position = self.getCenter()

        for point in self.points:
            point.simulate()
        self.getAvgVelocity()

    def getCenter(self):
        positionSum = np.array([0,0])
        for point in self.points:
            positionSum = np.add(positionSum, point.position)
        if(Settings.debugMode):pygame.draw.circle(Singleton.screen, [0,255,0], Camera.reMap(self.position.tolist(), self.offset), 5)
        return positionSum / len(self.points)
            
    def draw(self):
        surface = Singleton.screen
        points = []
        for i in range(len(self.points)):
            points.append(self.points[i].getPosition())
            if(Settings.debugMode): 
                pygame.draw.line(surface, [0,255, 255], Camera.reMap(self.points[i].getPosition(), self.offset), Camera.reMap(np.add(self.points[i].position, self.points[i].velocity).tolist(), self.offset), 5)
                for connection in self.points[i].connections:
                    pygame.draw.line(surface, [255, 0, 0], Camera.reMap(self.points[i].getPosition()), Camera.reMap(connection.otherPoint.getPosition(), self.offset))
        if(Settings.debugMode):
            pygame.draw.lines(surface, [0,0,0], True, Camera.reMap(points, self.offset), 5)
            pygame.draw.polygon(surface, [0,255,0], Camera.reMap([self.topRight, [self.topRight[0], self.bottomLeft[1]], self.bottomLeft, [self.bottomLeft[0], self.topRight[1]]], self.offset), 3)
        else:
            thickness = Settings.lineThickness
            pygame.draw.polygon(surface, self.color, Camera.reMap(points, self.offset), 0)
            pygame.draw.lines(surface, [0,0,0], True, Camera.reMap(points, self.offset), thickness)
            for point in points:
                pygame.draw.circle(surface, [0,0,0], Camera.reMap(point, self.offset), thickness/2)

    def getTotalMass(self):
        sum = 0
        for point in self.points:
            sum += point.mass
        return sum
    
    def doCollisions(self, objects):
        for obj in objects:
            if obj.tag in self.noCollide: continue
            if obj is self: continue
            if not self.inBoundingBox(obj): continue
            self.collision(obj)

    def collision(self, otherObject):

        lines = otherObject.getLines()

        for point in self.points:
            if self.isInside(point, lines):
                self.fixOverlap(point, lines)
                
    def fixOverlap(self, point, lines):
        closestPos, line, moveVec = self.getClosestLine(point, lines)
        totalMass = point.mass + line.end1.mass + line.end2.mass
        lerpPos = (point.getPosition()[0] - line.end1.getPosition()[0]) / (line.end2.getPosition()[0] - line.end1.getPosition()[0] + .001)

        pointMove = 1 - point.mass / totalMass
        end1Move = (1-lerpPos) * line.end1.mass / totalMass
        end2Move = lerpPos * line.end2.mass / totalMass

        line.end1.move(-moveVec * end1Move)
        line.end2.move(-moveVec * end2Move)
        point.move(moveVec * pointMove)

        # point.velocity = np.array([0,0]) #SUPER LAME BUT KINDA WORKS
        # line.end1.velocity = np.array([0,0])
        # line.end2.velocity = np.array([0,0])
        
        virtualVelocity = line.end1.velocity * line.end1.mass / line.getMass() + line.end2.velocity * line.end2.mass / line.getMass()
        linepV = Vector.scalerProject(moveVec, virtualVelocity)
        pointpV = Vector.scalerProject(moveVec, point.velocity)
        newLineBouncyVelocity = (line.getMass() * linepV - point.mass * linepV + 2 * point.mass * pointpV)/(line.getMass() + point.mass)
        newPointBouncyVelocity = (point.mass * pointpV - line.getMass() * pointpV + 2 * line.getMass() * linepV)/(line.getMass() + point.mass)

        stiffVelocity = (line.getMass() * linepV + point.mass * pointpV)/(line.getMass() + point.mass)

        bounciness = .1
        pointTraction = .8
        newLineVelocity = newLineBouncyVelocity * bounciness + stiffVelocity * (1 - bounciness)
        newPointVelocity = newPointBouncyVelocity * bounciness + stiffVelocity * (1 - bounciness)

        lineVelocity = newLineVelocity * moveVec + (virtualVelocity - Vector.project(moveVec, virtualVelocity)) * (1 - pointTraction) ** (abs(linepV - newLineVelocity) * np.linalg.norm(moveVec))
        pVelocity = newPointVelocity * moveVec + (point.velocity - Vector.project(moveVec, point.velocity)) * (1 - pointTraction) ** (abs(pointpV - newPointVelocity) * np.linalg.norm(moveVec))

        point.velocity = pVelocity
        line.end1.velocity = lineVelocity + (line.end1.velocity - line.end2.velocity) / 2
        line.end2.velocity = lineVelocity - (line.end1.velocity - line.end2.velocity) / 2

        pygame.draw.line(Singleton.screen, [255,0,255], point.getPosition(), Vector.addArrays([-pVelocity,point.getPosition()]))
        
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
        return numInterSects
        
    def getLines(self):
        lines = []
        for i in range(-1,len(self.points) - 1):
            lines.append(Line(self.points[i], self.points[i+1]))
        return lines
    
    def getClosestLine(self, point, lines):
        closest = 2**100
        closestLine = None
        closestPos = None
        moveVec = None

        for line in lines:
            closePos, dist, vecDif = line.projectPointOnLine(point, True)
            if dist < closest: #lastOnLine and not onLine and newRealDist < closest or lastOnLine and onLine and dist < closest or not lastOnLine and onLine and dist < realDist or not lastOnLine and not onLine and newRealDist < realDist:# and newRealDist < realDist): 
                closest = dist
                closestLine = line
                closestPos = closePos
                moveVec = vecDif
        return closestPos, closestLine, moveVec

    def getPosition(self):
        return self.position.tolist()
    
    def getMass(self):
        mass = 0
        for point in self.points:
            mass += point.mass
        return mass

    def getAvgVelocity(self):
        ratio = 1
        avgVel = np.array([0,0])
        for point in self.points:
            avgVel = np.add(avgVel,point.velocity)
        return np.multiply(avgVel,1/len(self.points))

    def addVelocity(self, vel):
        for point in self.points:
            point.velocity = np.add(point.velocity, vel)

    def move(self, vector):
        for point in self.points:
            point.move(vector)
        self.position = self.getCenter()

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
            pygame.draw.circle(screen, [255,50, 255], Camera.reMap([xVal, checkPos[1]]), 5)

        return True
    
    def projectOnLine(self, vel):
        direction = self.end1.getDirection(self.end2)
        projectedDirection = np.dot(vel, direction) / np.dot(direction, direction) * direction
        if np.dot(vel, direction) < 0: projectedDirection = -projectedDirection
        return projectedDirection
    
    def projectPointOnLine(self, point, findClosest = False):
        direction = self.end1.getDirection(self.end2) #vector from point 1 on line to point 2 on line
        relDirection = self.end1.getDirection(point) #vector from point 1 to point
        projectedDirection = np.dot(relDirection, direction) / np.dot(direction, direction) * direction # project vector on line
        projPos = np.add(projectedDirection, self.end1.getPosition()) #add point 1 to get real world position

        if findClosest:
            dif1 = self.end1.getPosition()[1] - projPos[1] #check that y's are the around the point
            dif2 = self.end2.getPosition()[1] - projPos[1]
            dif1y = self.end1.getPosition()[0] - projPos[0] #check that y's are the around the point
            dif2y = self.end2.getPosition()[0] - projPos[0]
            if(np.sign(dif1) == np.sign(dif2) and np.sign(dif1y) == np.sign(dif2y)): 
                projPos = self.end1.position if self.end1.getDist(point) < self.end2.getDist(point) else self.end2.position

        return projPos, np.linalg.norm(point.position - projPos), projPos - point.position
    
    def getMass(self):
        return self.end1.mass + self.end2.mass
    
    def draw(self, color = [0,0,0], width = 1):
        pygame.draw.line(Singleton.screen, color, self.end1.getPosition(), self.end2.getPosition(), width)
