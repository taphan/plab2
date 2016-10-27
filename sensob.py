import reflectance_sensors
import ultrasonic
<<<<<<< HEAD
import zumo_button
=======
import camera
from PIL import Image

>>>>>>> 7cc6b53b2c801de3890d4c6d16bcf952ea8617a6

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

<<<<<<< HEAD

=======
>>>>>>> 7cc6b53b2c801de3890d4c6d16bcf952ea8617a6

class UltrasonicSensOb(Sensob):

    def __init__(self):
        self.sensor = ultrasonic.Ultrasonic()

    def update(self):
        self.sensor.update()

    def get_value(self):
        return self.sensor.get_value()

    def reset(self):
        self.sensor.reset()

<<<<<<< HEAD
class ZumoButton():

    def __init__(self):
        self.button = zumo_button.ZumoButton()
        self.button.wait_for_press() # ZumoButton må bli instansiert i en høyere klasse, venter for trykk
=======

class CameraSensob(Sensob):

    def __init__(self):
        self.img_width = 128
        self.img_height = 96
        self.sensor = camera.Camera(self.img_width, self.img_height)

    def update(self):
        self.value = self.sensor.update()

    def get_value(self):
        self.value = self.sensor.get_value()
        return self.value

    def reset(self):
        self.sensor.reset()

    def get_color(self):
        """
        Får bilde fra camera via get_value
        Regner ut gjennomsnittsfargen i bildet
        :return: fargen som dominerer, eventuelt 'unknown' hvis ingen dominerer
        """
        img = self.get_value()
        img = img.resize((50,50))
        width = 50
        height = 50

        r_ave = 0
        g_ave = 0
        b_ave = 0

        for x in range(0, width):
            for y in range(0, height):
                r, g, b = img.getpixel((x, y))
                r_ave = (r + r_ave) / 2
                g_ave = (g + g_ave) / 2
                b_ave = (b + b_ave) / 2

        if r_ave >= g_ave and r_ave >= b_ave:
            self.color = 'red'
        elif g_ave >= r_ave and g_ave >= b_ave:
            self.color = 'green'
        elif b_ave >= r_ave and b_ave >= g_ave:
            self.color = 'blue'
        else:
            self.color = 'unknown'

        return self.color
>>>>>>> 7cc6b53b2c801de3890d4c6d16bcf952ea8617a6
