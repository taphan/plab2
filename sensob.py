import reflectance_sensors


class Sensob():
    def update(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class ReflectanceSensOb(Sensob):

    def __init__(self):
        pass