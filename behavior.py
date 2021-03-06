import bbcon
import sensob
import motob
import math
import random
import motors
import imager2 as IMR


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
        self.name = ''

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
        self.picture_taken = False
        self.name = 'Color'

    def consider_deactivation(self):
        self.line_status = self.bbcon.line_status
        if self.line_status == 0: # Forsørg at testen skjer bare når den er på
            self.active_flag = False

    def consider_activation(self):
        # Aktiveres kun når enden av linjen er funnet
        self.line_status = self.bbcon.line_status
        if self.line_status != 0:
            self.active_flag = True

    def update(self):
        if not self.active_flag:
            self.sensor.reset()
        else:
            self.line_status = self.bbcon.line_status
            #self.weight = self.priority*self.match_degree
            self.weight = 1
            self.sense_and_act()
            self.halt_request = True # Stopper programmet etter vi har tatt et bilde

    def sense_and_act(self):
        """
        Rød: Snu venstre
        Grønn: Snu høyre
        """
        if self.picture_taken == True:
            self.motor_recs = ('S', 0)
            self.weight = 1
        else:
            print('Tar bildet.')
            im = IMR.Imager(image=self.sensor.update()).scale(1, 1)
            im.dump_image('tatt_bilde.jpeg')
            color = self.sensor.get_color()
            print("Test color:", color)
            self.match_degree = 1
            self.weight = 1
            if color == 'red':
                self.motor_recs = ('L', 90)
            elif color == 'green':
                self.motor_recs = ('R', 90)
            else:
                self.motor_recs = ('L', 180)
                self.halt_request = True # Stopper hele testen dersom
            self.picture_taken = True
            self.bbcon.active_count = False # Stopp hele programmet

class IRFollow(Behavior):
    def __init__(self, bbcon):
        super(IRFollow, self).__init__(bbcon)
        self.ir = sensob.IRProximitySensob()
        self.sensobs.append(self.ir)
        self.bbcon.add_sensob(self.ir)
        self.priority = 0.9
        self.name = 'IRFollow'
        self.line_status = self.bbcon.line_status

    def consider_deactivation(self):
        self.line_status = self.bbcon.line_status
        if self.line_status != 0:
            self.active_flag = False

    def consider_activation(self):
        self.line_status = self.bbcon.line_status
        if self.line_status == 0:
            self.active_flag = True

    def update(self):
        self.line_status = self.bbcon.line_status
        if self.line_status == 0 or True:
            self.sense_and_act()
            self.weight = self.match_degree * self.priority
        else:
            self.weight = self.priority

    def sense_and_act(self):
        print(self.ir.values)
        # First check the obstacles on the side
        if self.ir.values[0] == True and self.ir.values[1] == False:    # If right side of the robot meets a wall
            self.match_degree = 1
            self.motor_recs = ('R',30)   # Turn left 90 degrees
        elif self.ir.values[0] == False and self.ir.values[1] == True:
            self.match_degree = 1
            self.motor_recs = ('L',30)
        else:
            self.match_degree = 0
            self.motor_recs = ('F',90) # In case this gets activated by mistake

class FindLine(Behavior):
    def __init__(self,bbcon):
        super(FindLine, self).__init__(bbcon)
        sensor = sensob.ReflectanceSensOb()
        self.bbcon.add_sensob(sensor)
        self.sensobs.append(sensor)
        self.priority = 0.9
        self.steps_line_followed = 0
        self.line_found_flag = False
        self.line_status = 0  # 0:found, 1: follows, 2: end reached
        self.last_left = False
        self.name = 'FindLine'

    def consider_deactivation(self):
        if self.line_status == 2:
            #self.active_flag = False
            pass


    def consider_activation(self):
        if self.line_status == 0:
            self.active_flag = True

        elif self.line_status == 1:
            self.active_flag = True


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

        #self.weight = self.match_degree * self.priority
        self.weight = 0
        print("Les sensor: ", sensor_values)
        # if sum(sensor_values) < 1:   # If sensor found a dark area
        if sensor_values.count(0.0) >= 1: # If any (total six) sensors read dark (0.0)
            self.line_found_flag = True
            self.motor_recs = ('S', 0) # Send stop signal to motob
            print("Found line!!")
            self.match_degree = 1
            self.weight = self.match_degree * self.priority
            self.line_status = 2  # Set line_status to 2

    '''
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
    '''
    def get_line_status(self):
        return self.line_status

class Wander(Behavior):

    def __init__(self,bbcon):
        super(Wander, self).__init__(bbcon)
        self.priority = 0.3
        self.steps_this_direction = 0
        self.line_status = self.bbcon.line_status
        self.name = 'Wander'

    def consider_activation(self):
        self.line_status = self.bbcon.line_status
        if self.line_status == 0:
            self.active_flag = True

    def consider_deactivation(self):
        self.line_status = self.bbcon.line_status
        if self.line_status != 0:
            self.active_flag = False

    def update(self):
        self.line_status = self.bbcon.line_status
        if self.line_status == 0 or True:
            self.sense_and_act()
            self.weight = self.match_degree * self.priority
        else:
            self.weight = self.priority

    def sense_and_act(self):
        self.match_degree = 1

        rand1 = random.randint(0, 2)
        direction = 'L'
        if rand1 == 0:
            direction = 'R'
        elif rand1 == 2:
            direction = 'F'

        degrees = random.randint(1, 90)

        self.motor_recs = (direction, None)
        self.bbcon.add_behavior(self)

class AvoidObstacles(Behavior):
    # Endrer til å bruke ultralyd sensor
    def __init__(self,bbcon):
        super(AvoidObstacles, self).__init__(bbcon)
        # Denne Behavior-klassen bruker IRProx og Ultrasonic sensobene
        self.ultra = sensob.UltrasonicSensob()
        self.sensobs.append(self.ultra)
        self.bbcon.add_sensob(self.ultra)
        self.priority = 0.7
        self.name = 'AvoidObstacles'

    # Update match_degree according to readings from our sensors
    def sense_and_act(self):

        # For ultrasonic, only active when distance is in the range [0cm , 20cm]
        if self.ultra.get_value() > 20:    # If targets too far away, don't consider
            self.match_degree = 0
            self.motor_recs = ('F', 90)
        else:    # If distance is between 0 to 20cm
            print("Found an obstacle with Ultrasonic sensor.")
            self.match_degree = 1-(self.ultra.get_value()/20)   # scale the value
            self.motor_recs = ('L', 90)   # Guarantee that robot will move away from the wall at one point


    def update(self):
        # Denne skal alltid søke etter obstacles så den skal ikke slås av
        self.sense_and_act()
        self.weight = self.priority*self.match_degree

    def consider_activation(self):
        self.active_flag = True

    def consider_deactivation(self):
        self.active_flag = True

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
