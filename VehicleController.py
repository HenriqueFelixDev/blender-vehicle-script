from bge import logic as g, constraints

o = g.getCurrentController().owner
objects = g.getCurrentScene().objects

class Vehicle:
    def __init__(
        self,
        engineForce,
        steering,
        brakeForce,
        downForce = [0.0, 0.0, -1.0],
        wheelSuspensionLength = 1,
        wheelRadius = 0.5
    ):
        vehicleConstraint = constraints.createConstraint(o.getPhysicsId(), 0, constraints.VEHICLE_CONSTRAINT)
        self._car = constraints.getVehicleConstraint(vehicleConstraint.getConstraintId())
        
        self._engineForce = engineForce
        self._steering = steering
        self._brakeForce = brakeForce
        self._currentEngineForce = 0
        self._currentSteering = 0
        self._currentBrakeForce = 0
        
        self._wheelRotationAxis = [1, 0, 0]
        self._downForce = downForce
        self._wheelSuspensionLength = wheelSuspensionLength
        self._wheelRadius = wheelRadius
        self._wheels = []
    
    
    def update(self):
        self._applyEngineForce()
        self._applySteering()
        self._applyBrake()
        
        self._currentEngineForce = 0
        self._currentSteering = 0
        self._currentBrakeForce = 0
    
    
    def addWheel(self, wheelObjectName, steer = False):
        wheelObject = objects[wheelObjectName]
        wheelPosition = o.worldPosition + wheelObject.worldPosition
        
        self._wheels.append({
            'objectName': wheelObjectName,
            'steer': steer,
        })
        
        self._car.addWheel(
            wheelObject,
            wheelPosition,
            self._downForce,
            self._wheelRotationAxis,
            self._wheelSuspensionLength,
            self._wheelRadius,
            steer,
        )
    
    def _applyEngineForce(self):
        for wheelIndex in range(len(self._wheels)):
            if not self._wheels[wheelIndex]['steer']:
                self._car.applyEngineForce(self._currentEngineForce, wheelIndex)
    
    
    def _applySteering(self):
        for wheelIndex in range(len(self._wheels)):
            if self._wheels[wheelIndex]['steer']:
                self._car.setSteeringValue(self._currentSteering, wheelIndex)
    
    
    def _applyBrake(self):
        for wheelIndex in range(len(self._wheels)):
            if not self._wheels[wheelIndex]['steer']:
                self._car.applyBraking(self._currentBrakeForce, wheelIndex)
    
    def accelerate(self):
        self._currentEngineForce = self._engineForce
        
    
    def reverse(self):
        self._currentEngineForce = -self._engineForce
    
    
    def brake(self):
        self._currentBrakeForce = self._brakeForce
    
    
    def steer(self, direction):
        if direction == 'left':
            self._currentSteering = self._steering
        elif direction == 'right':
            self._currentSteering = -self._steering
            
