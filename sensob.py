import reflectance_sensors
import ultrasonic
import zumo_button

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

class ZumoButton():

    def __init__(self):
        self.button = zumo_button.ZumoButton()
        self.button.wait_for_press() # ZumoButton må bli instansiert i en høyere klasse, venter for trykk