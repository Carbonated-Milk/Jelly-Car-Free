from GameSettings import *

class Camera:

    cameraOffset = Singleton.screenCenter
    targetOffset = Singleton.screenCenter

    camSize = 1
    targetCameraSize = 1

    isGradual = True

    @staticmethod
    def reMap(data, offSet = 0):
        if isinstance(data[0], list):
            reMappedData = []
            for coord in data:
                newPos = Camera.reMap(coord, offSet)
                reMappedData.append(newPos)
            return reMappedData
        
        return Camera.mapSingle(data, offSet) #if number
    
    def inverseReMap(data, offSet = 0):
        if isinstance(data[0], list):
            reMappedData = []
            for coord in data:
                newPos = Camera.inverseMap(coord, offSet)
                reMappedData.append(newPos)
            return reMappedData
        if isinstance(data, list):
            return Camera.inverseMap(data, offSet) #if number
        return data / Camera.camSize
    
    @staticmethod
    def inverseMap(point, offset = 0):
        changeSize = Camera.camSize - offset / 100
        return ((np.array(point) - np.array(Singleton.screenCenter)) * changeSize + np.array(Camera.cameraOffset)).tolist()

    @staticmethod 
    def mapSingle(point, offset = 0):
        changeSize = 1 / (Camera.camSize - offset / 100)
        return ((np.array(point) - np.array(Camera.cameraOffset)) * changeSize + np.array(Singleton.screenCenter)).tolist()
    
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
    def setTargetCameraSize(target):
        Camera.targetCameraSize = target

    @staticmethod
    def scaleTargetCameraSize(scale, times = 1):
        Camera.targetCameraSize *= scale ** times

    changeReducer = 10
    @staticmethod
    def cameraUpdate():
        Camera.cameraOffset = np.add(np.array(Camera.targetOffset), - np.array(Camera.cameraOffset)) / Camera.changeReducer + np.array(Camera.cameraOffset)
        Camera.camSize = np.add(np.array(Camera.targetCameraSize), - np.array(Camera.camSize)) / Camera.changeReducer + np.array(Camera.camSize)