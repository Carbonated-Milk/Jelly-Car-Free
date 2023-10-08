from GameSettings import *

class Camera:

    cameraOffset = Singleton.screenCenter
    targetOffset = Singleton.screenCenter

    isGradual = True

    @staticmethod
    def reMap(data):
        if isinstance(data[0], list):
            reMappedData = []
            for coord in data:
                newPos = Camera.reMap(coord)
                reMappedData.append(newPos)
            return reMappedData
        
        return Camera.mapSingle(data) #if number

    @staticmethod 
    def mapSingle(point):
        return ((np.array(point) - np.array(Camera.cameraOffset) + np.array(Singleton.screenCenter))).tolist()
    
    @staticmethod 
    def setScreenOffset(point):
        Camera.targetOffset = np.array(Singleton.screenCenter) + np.array(point)
    
    @staticmethod 
    def moveScreenOffset(vec):
        Camera.targetOffset = np.add(np.array(Camera.targetOffset), np.array([vec[0], -vec[1]]))

    @staticmethod
    def setTargetOffset(position):
        Camera.targetOffset = position

    @staticmethod
    def cameraUpdate():
        Camera.cameraOffset = np.add(np.array(Camera.targetOffset), - np.array(Camera.cameraOffset)) / 10 + np.array(Camera.cameraOffset)