import sensob
import motob

class Behavior():

    def __init__(self):
        # self.bbcon = (bbcon object)  # Pointer to the controller that uses this behavior
        self.sensobs = []
        self.motor_recs = ('L', 0) # Recs motor to the arbitrator
        self.active_flag = False
        self.halt_request = False
        self.priority = 0 # Static
        self.match_degree = 0.0 # Et reelt tall mellom 0 og 1
        self.weight = 0.0 # Product of priority og match_degre

    def consider_deactivation(self):
        raise NotImplementedError

    def consider_deactivation(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def sense_and_act(self):
        raise NotImplementedError

class FollowLine(Behavior):

    def __init__(self):
        super(FollowLine, self).__init__()


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
        # (if) For IRProximity where ir.values=[leftdistance,rightdistance], if one of the sides are close
            # Find out what # the readings show then divide accordingly to achieve range [0,1]
            # Then set motor_recs to *turn 90 degrees to the side that doesn't meet obstacles*
        # (else) For ultrasonic, calculate distance in the range [1cm , 20cm]?
            # Find out what # the readings show then divide accordingly to achieve range [0,1]
            # Set motor_recs to *turn 90 degrees to the left* bc why not
        pass

    def update(self):
        # Denne skal alltid søke etter obstacles så den skal ikke slås av (active_flag = True)
        self.sense_and_act()
        self.weight = self.priority*self.match_degree