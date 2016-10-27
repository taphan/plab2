import bbcon
import sensob
import motob

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

    def consider_deactivation(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def sense_and_act(self):
        raise NotImplementedError

class FollowLine(Behavior):

    def __init__(self):
        super(FollowLine, self).__init__()

class Color(Behavior):

    def __init__(self):
        super(Color, self).__init__()
        self.priority = 1
        self.line_status = self.bbcon.line_status

    def consider_deactivation(self):
        if self.active_flag: # Forsørg at testen skjer bare når den er på


    def consider_activation(self):
        # Aktiveres kun når enden av linjen er funnet
        if self.line_status == 2:
            self.active_flag = True


    def update(self):
        pass

    def sense_and_act(self):
        pass