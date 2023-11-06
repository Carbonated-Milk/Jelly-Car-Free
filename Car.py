from GameObject import GameObject
from PointMass import *
from Wheel import Wheel
from Input import Input
from Camera import Camera


class Car(GameObject):
    def __init__(self, position, frictionConst=0.5, offset=0):
        pointInfo = [
            [0, 0],
            [
                PointInfo(np.array([466.0, 387.0]), 1, False, 1),
                PointInfo(np.array([647.0, 388.0]), 1, False, 1),
                # PointInfo(np.array([649.0, 340.0]), 1, False, 1),
                # PointInfo(np.array([607.0, 336.0]), 1, False, 1),
                # PointInfo(np.array([591.0, 286.0]), 1, False, 1),
                # PointInfo(np.array([529.0, 285.0]), 1, False, 1),
                # PointInfo(np.array([503.0, 327.0]), 1, False, 1),
                PointInfo(np.array([500, 387.0]), 1, False, 1),
            ],
            0.5,
        ]
        super().__init__(*pointInfo)
        self.tag = "car"
        self.noCollide = ["wheel"]
        self.position = np.array(position)

        self.setUpWheels()

    def setUpWheels(self):
        wheelSize = 50
        self.wheel1 = Wheel(self.position + np.array([-50, 50]), wheelSize)
        self.wheel2 = Wheel(self.position + np.array([50, 50]), wheelSize)
        Singleton.activeObjects.append(self.wheel1)
        Singleton.activeObjects.append(self.wheel2)
        self.wheel1.move(self.points[1].position - self.wheel1.position)
        self.wheel2.move(self.points[0].position - self.wheel2.position)

    def simulate(self):
        super().simulate()

    def update(self):
        if self.wheel1 not in Singleton.activeObjects:
            self.setUpWheels()
        super().update()
        self.keepWheelsAttatched(self.wheel1, 1)
        self.keepWheelsAttatched(self.wheel2, 0)
        Camera.targetOffset = self.position

    def keepWheelsAttatched(self, obj, pointNum):
        carMass = self.points[pointNum].mass
        wheelMass = obj.getMass()
        ratio = carMass / (carMass + wheelMass)
        fixVector = self.points[pointNum].position - obj.position
        self.points[pointNum].move(-fixVector * (1 - ratio))
        obj.move(fixVector * ratio)

        avgVel = (
            ratio * self.points[pointNum].velocity + (1 - ratio) * obj.getAvgVelocity()
        )
        self.points[pointNum].velocity = avgVel
        obj.addVelocity(avgVel - obj.getAvgVelocity())

    def __repr__(self):
        return f"Car({self.position.tolist()})"
