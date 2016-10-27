import reflectance_sensors
import ultrasonic

class Sensob():
    def update(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class ReflectanceSensOb(Sensob):

    def __init__(self):
<<<<<<< HEAD
        # bruker min og max for å kalibrere. Kan endres til auto_calibrate
        self.sensor = reflectance_sensors.ReflectanceSensors(auto_calibrate=False, min_reading=100, max_reading=1000)
        self.get_value()

    def update(self):
        self.updated_value = self.sensor.update()

    def get_value(self):
        self.value = self.sensor.get_value()

    def reset(self):
        self.sensor.reset()

=======
        pass
<<<<<<< HEAD

class UltrasonicSensOb(Sensob):

    def __init__(self):
        self.sensor = ultrasonic.Ultrasonic()

    def update(self):
        self.sensor.update()

    def get_value(self):
        return self.sensor.get_value()

    def reset(self):
        self.sensor.reset()

=======
>>>>>>> 8bd62f43ea012c869422fc0c361a5e503f685409
>>>>>>> d35c6a8ae1bc0d3d7d5796cda43ea47f18f6a565
