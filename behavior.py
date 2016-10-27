import bbcon
import sensob
import motob
import math

class Behavior():

    def __init__(self):
        # self.bbcon = (bbcon object)  # Pointer to the controller that uses this behavior
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

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        # Aktiveres kun når enden av linjen er funnet
        if self.line_status == 2:
            self.active_flag == True
        

    def update(self):
        pass

    def sense_and_act(self):
        pass

class FollowLine(Behavior):

    def __init__(self):
        super(FollowLine, self).__init__()
        sensor = sensob.ReflectanceSensOb()
        self.sensobs.append(sensor)
        self.active_flag = True
        self.priority = 0.7
        self.steps_line_followed = 0
        self.line_found_flag = False

    def consider_deactivation(self):
        line_status = 1
        if line_status == 2:
            self.active_flag = False
            return True

    def consider_activation(self):
        line_status = 0
        if line_status == 0:
            self.active_flag = True
            return True
        elif line_status == 1:
            self.active_flag = True
            return True

    def sense_and_act(self):
        if self.line_found_flag:
            self.follow_line()
        else:
            self.find_line()
    def find_line(self):
        sensor = self.sensobs[0]

    def follow_line(self):
        pass


class AvoidObstacles(Behavior):
    def __init__(self):
        super(AvoidObstacles, self).__init__()
        # Denne Behavior-klassen bruker IRProx og Ultrasonic sensobene
        self.ir = sensob.IRProximitySensob()
        self.ultra = sensob.UltrasonicSensob()
        self.sensobs.append(self.ir) ; self.sensobs.append(self.ultra)
        self.priority = 0.9

    # Update match_degree according to readings from our sensors
    def sense_and_act(self):
        # First check the obstacles on the side
        if self.ir.values[0] == True:    # If right side of the robot meets a wall
            self.match_degree = 1
            self.motor_recs = ('L',90)   # Turn left 90 degrees
        elif self.ir.values[1] == True:  # If left side meets a wall
            self.match_degree = 1
            self.motor_recs = ('R',90)   # Turn right 90 degrees

        # For ultrasonic, only active when distance is in the range [0cm , 20cm]
        elif self.ultra.get_value() > 20:    # If targets too far away, don't consider
            self.match_degree = 0
        else:    # If distance is between 0 to 20cm
            self.match_degree = abs( (self.ultra.get_value()/20) - 1)  # -1 to invert the scaled value
            self.motor_recs = ('L', 90)


    def update(self):
        # Denne skal alltid søke etter obstacles så den skal ikke slås av
        self.sense_and_act()
        self.weight = self.priority*self.match_degree

