from bge import logic as g, events as e
from VehicleController import *


c = g.getCurrentController()
o = c.owner


def start(controller):
    car = Vehicle(
        engineForce = 70,
        brakeForce = 2,
        steering = 10,
    )
    
    controller.owner['car'] = car
    
    car.addWheel('0', True)
    car.addWheel('1', True)
    car.addWheel('2')
    car.addWheel('3')


def update(controller):
    sensors = g.getCurrentController().sensors
    car = controller.owner['car']
    
    def sensorActive(key):
        key in sensors and sensors[key].status == g.KX_SENSOR_ACTIVE
    
    if g.keyboard.events[e.WKEY] or sensorActive('w'):
        car.accelerate()


    if g.keyboard.events[e.SKEY] or sensorActive('s'):
        car.reverse()


    if g.keyboard.events[e.LEFTARROWKEY] or sensorActive('arrowleft'):
        car.steer('left')


    if g.keyboard.events[e.RIGHTARROWKEY] or sensorActive('arrowright'):
        car.steer('right')
        

    if g.keyboard.events[e.SPACEKEY] or sensorActive('space'):
        car.brake()
    
    car.update()
