import bbcon
import sensob
import motob
import random

class Behavior():

    def __init__(self):
        # Pointer to the controller that uses this behavior
        self.bbcon = bbcon.BBCON()
        self.sensobs = []
        self.motor_recs = ('L', 0) # Recs motor to the arbitrator
        self.active_flag = False
        self.halt_request = False
        self.priority = 0 # Static
        self.match_degree = 0.0 # Et reelt tall mellom 0 og 1
        self.weight = 0.0 # Product of priority og match_degre

    def consider_deactivation(self):
        raise NotImplementedError

    def consider_activation(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def sense_and_act(self):
        raise NotImplementedError

class Color(Behavior):

    def __init__(self):
        super(Color, self).__init__()
        self.priority = 1
        self.line_status = self.bbcon.line_status
        self.sensor = sensob.CameraSensob()
        self.sensobs.append(self.sensor)

    def consider_deactivation(self):
        if self.active_flag: # Forsørg at testen skjer bare når den er på
            self.active_flag = False

    def consider_activation(self):
        # Aktiveres kun når enden av linjen er funnet
        if self.line_status == 2:
            self.active_flag = True

    def update(self):
        if not self.active_flag:
            self.sensor.reset()
        else:
            self.sense_and_act()
            self.weight = self.priority*self.match_degree

    def sense_and_act(self):
        """
        Rød: Snu venstre
        Blå: Snu høyre
        Grønn: Snu 180 grader og stopp
        """
        self.sensor.update()
        color = self.sensor.get_color()
        if color == 'red':
            self.motor_recs = ('L', 90)
        elif color == 'blue':
            self.motor_recs = ('R', 90)
        else:
            self.motor_recs = ('L', 180)
            self.halt_request = True # Stopper hele testen dersom


class FollowLine(Behavior):
    def __init__(self):
        super(FollowLine, self).__init__()
        sensor = sensob.ReflectanceSensOb()
        self.sensobs.append(sensor)
        self.priority = 0.7
        self.steps_line_followed = 0
        self.line_found_flag = False
        self.line_status = 0  # 0:found, 1: follows, 2: end reached
        self.last_left = False

    def consider_deactivation(self):
        if self.line_status == 2:
            self.active_flag = False
            return True

    def consider_activation(self):
        if self.line_status == 0:
            self.active_flag = True
            return True
        elif self.line_status == 1:
            self.active_flag = True
            return True

    def update(self):
        if self.active_flag:
            self.consider_deactivation()
            if self.active_flag:
                self.sense_and_act()
        else:
            self.consider_activation()
            if self.active_flag:
                self.sense_and_act()

    def sense_and_act(self):
        if self.line_found_flag:
            self.follow_line()
        else:
            self.find_line()
        self.weight = self.match_degree * self.priority

    def find_line(self):
        self.sensobs[0].update()
        sensor_values = self.sensobs[0].get_value()

        threshold = 0.75

        if sensor_values[5] - sensor_values[1] > threshold:
            # black line found
            self.line_found_flag = True
            # turn 30 degrees left
            self.motor_recs = ('L', 30)
            self.match_degree = 1
            self.line_status = 1
        elif sensor_values[0] - sensor_values[5] < threshold:
            # white line found
            # turn around (180 degrees left)
            self.motor_recs = ('L', 180)
            self.match_degree = 1

    def follow_line(self):
        threshold = 0.75

        self.sensobs[0].update()
        sensor_values = self.sensobs[0].get_value()

        if sensor_values[5] == sensor_values[4] and sensor_values[3] - sensor_values[5] > threshold:
            # end of line found
            self.line_status = 2
            self.match_degree = 1
            self.motor_recs = ('L', 0)
        elif sensor_values[5] == sensor_values[3] and sensor_values[1] - sensor_values[4] > threshold:
            if self.last_left:
                self.last_left = False
                self.motor_recs = ('R', 5)
            else:
                self.last_left = True
                self.motor_recs = ('L', 5)
            self.match_degree = sensor_values[1] - sensor_values[4]
        else:
            self.motor_recs = ('L', 0)
            self.match_degree = 0.9

    def get_line_status(self):
        return self.line_status

class Wander(Behavior):

    def __init__(self):
        super(Wander, self).__init__()
        self.priority = 0.3
        self.steps_this_direction = 0
        self.line_status = self.bbcon.line_status

    def consider_activation(self):
        if self.line_status == 0:
            self.active_flag = True

    def consider_deactivation(self):
        if self.line_status != 0:
            self.active_flag = False

    def update(self):
        self.line_status = self.bbcon.line_status
        if self.active_flag:
            self.consider_deactivation()
            if self.active_flag:
                self.sense_and_act()
        else:
            self.consider_activation()
            if self.active_flag:
                self.sense_and_act()
        self.weight = self.match_degree * self.motor_recs

    def sense_and_act(self):
        threshold = 3
        self.match_degree = 1
        if self.steps_this_direction > threshold:
            rand1 = random.randint(0, 1)
            direction = 'L'
            if rand1 == 0:
                direction = 'R'

            degrees = random.randint(0, 90)

            self.motor_recs = (direction, degrees)

            self.steps_this_direction = 0
        else:
            self.steps_this_direction += 1


class StartButton(Behavior):

    def __init__(self):
        super(StartButton, self).__init__()
       # self.active_flag = True
        sensor = sensob.ZumoButton()
       # self.active_flag = False

    def consider_activation(self):
        pass

    def consider_deactivation(self):
        self.active_flag = False

    def update(self):
        pass

    def sense_and_act(self):
        pass