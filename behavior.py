<<<<<<< HEAD
=======
import sensob
import motob

class Behavior():

    def __init__(self):
        # Pointer to the controller that uses this behavior
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

>>>>>>> 1c284e654b8fbe120ca9e9f2bade65600b0e0d67
