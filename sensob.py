import reflectance_sensors
import ultrasonic
import camera

class Sensob():
    def update(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class ReflectanceSensOb(Sensob):

    def __init__(self):
        # bruker min og max for å kalibrere. Kan endres til auto_calibrate
        self.sensor = reflectance_sensors.ReflectanceSensors(auto_calibrate=False, min_reading=100, max_reading=1000)
        self.get_value()

    def update(self):
        self.updated_value = self.sensor.update()

    def get_value(self):
        self.value = self.sensor.get_value()
        return self.value

    def reset(self):
        self.sensor.reset()


class UltrasonicSensOb(Sensob):

    def __init__(self):
        self.sensor = ultrasonic.Ultrasonic()

    def update(self):
        self.sensor.update()

    def get_value(self):
        return self.sensor.get_value()

    def reset(self):
        self.sensor.reset()


class CameraSensob(Sensob):

    def __init__(self):
        self.sensor = camera.Camera()

    def update(self):
        self.value = self.sensor.update()

    def get_value(self):
        self.value = self.sensor.get_value()
        return self.value

    def reset(self):
        self.sensor.reset()