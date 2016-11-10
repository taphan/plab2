import bbcon
import sensob
import motob
import math
import random
import motors

class Behavior():

    def __init__(self, bbcon):
        # self.bbcon = (bbcon object)  # Pointer to the controller that uses this behavior
        # Pointer to the controller that uses this behavior
        self.bbcon = bbcon
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

    def __init__(self,bbcon):
        super(Color, self).__init__(bbcon)
        self.priority = 1
        self.line_status = self.bbcon.line_status
        self.sensor = sensob.CameraSensob()
        self.bbcon.add_sensob(self.sensor)
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
            self.line_status = self.bbcon.line_status
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
        print("Test color:", color)
        print("Test value: ", self.sensor.get_value())

        if color == 'red':
            self.motor_recs = ('L', 90)
        elif color == 'blue':
            self.motor_recs = ('R', 90)
        else:
            self.motor_recs = ('L', 180)
            self.halt_request = True # Stopper hele testen dersom


class FindLine(Behavior):
    def __init__(self,bbcon):
        super(FindLine, self).__init__(bbcon)
        sensor = sensob.ReflectanceSensOb()
        self.bbcon.add_sensob(sensor)
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
        self.find_line()

    def find_line(self):
        self.sensobs[0].update()
        sensor_values = self.sensobs[0].get_value()

        threshold = 0.75
        self.weight = self.match_degree * self.priority

<<<<<<< HEAD
        if sum(sensor_values) < 1:   # If sensor found a dark area
            self.line_found_flag = True
            # turn 30 degrees left
            self.motor_recs = ('L', 0)
            self.match_degree = 1
            self.line_status = 2  # Set line_status to 2
=======
        if sum(sensor_values) < 1:
            #line found
            # black line found
            self.line_found_flag = True
            # turn 30 degrees left
            self.motor_recs = ('L', 30)
            self.match_degree = 1
            self.line_status = 1
>>>>>>> 04a2a73e8a3971b62ec945ec7602a1a893360b11

    def follow_line(self):
        threshold = 0.75

        self.sensobs[0].update()
        sensor_values = self.sensobs[0].get_value()

        if sensor_values[5] == sensor_values[3] and sensor_values[1] - sensor_values[4] > threshold:
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

    def __init__(self,bbcon):
        super(Wander, self).__init__(bbcon)
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
        self.weight = self.match_degree * self.priority

    def sense_and_act(self):
        self.match_degree = 1
        if True:
            rand1 = random.randint(0, 2)
            direction = 'L'
            if rand1 == 0:
                direction = 'R'
            elif rand1 == 2:
                direction = 'F'

            degrees = random.randint(1, 90)

            self.motor_recs = (direction, degrees)
            self.bbcon.add_behavior(self)

            self.steps_this_direction = 0


class AvoidObstacles(Behavior):
    def __init__(self,bbcon):
        super(AvoidObstacles, self).__init__(bbcon)
        # Denne Behavior-klassen bruker IRProx og Ultrasonic sensobene
        self.ir = sensob.IRProximitySensob()
        self.ultra = sensob.UltrasonicSensob()
        self.sensobs.append(self.ir) ; self.sensobs.append(self.ultra)
        self.bbcon.add_sensob(self.ir)
        self.bbcon.add_sensob(self.ultra)
        self.priority = 0.9

    # Update match_degree according to readings from our sensors
    def sense_and_act(self):
        # First check the obstacles on the side
        print(self.ir.values)
        if self.ir.values[0] == True and self.ir.values[1] == False:    # If right side of the robot meets a wall
            self.match_degree = 1
            self.motor_recs = ('R',90)   # Turn left 90 degrees
        else:
            self.motor_recs = ('F',90)

        # For ultrasonic, only active when distance is in the range [0cm , 20cm]
        # Får feilmelding, self.ultraget_value() er NoneType
        '''elif self.ultra.get_value() > 20:    # If targets too far away, don't consider
            self.match_degree = 0
        else:    # If distance is between 0 to 20cm
            self.match_degree = abs( (self.ultra.get_value()/20) - 1)  # -1 to invert the scaled value
            self.motor_recs = ('L', 90)   # Guarantee that robot will move away from the wall at one point
'''

    def update(self):
        # Denne skal alltid søke etter obstacles så den skal ikke slås av
        self.sense_and_act()
        self.weight = self.priority*self.match_degree

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

class TestClass(Behavior):
    '''
def dancer():
    ZumoButton().wait_for_press()
    m = Motors()
    m.forward(.2,3)
    m.backward(.2,3)
    m.right(.5,3)
    m.left(.5,3)
    m.backward(.3,2.5)
    m.set_value([.5,.1],10)
    m.set_value([-.5,-.1],10)'''
    def __init__(self):
        super(TestClass, self).__init__()
        sensor = sensob.ZumoButton()

    def update(self):
        m =  motors.Motors()
        m.forward(.2, 3)
        m.backward(.2, 3)
        m.right(.5, 3)
        m.left(.5, 3)
        m.backward(.3, 2.5)
        m.set_value([.5, .1], 10)
        m.set_value([-.5, -.1], 10)