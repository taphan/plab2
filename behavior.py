import sensob
import motob

class Behavior():

    def __init__(self):
        # Pointer to the controller that uses this behavior
        self.sensobs = []
        self.motor_recs = [] # Recs motor to the arbitrator
        self.active_flag = False
        self.halt_request = False
        self.priority = 0 # Static
        self.match_degree = 0.0 # Et reelt tall mellom 0 og 1
        self.weight = 0.0 # Product of priority og match_degre

    