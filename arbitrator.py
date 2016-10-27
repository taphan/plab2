import bbcon

class Arbitrator():

    def __init__(self, our_bbcon = bbcon.BBCON()):
        self.bbcon = our_bbcon
        self.active_behaviors = self.bbcon.active_behaviors

    def choose_action(self):

        motor_recs = []
        halt_request = False
        return motor_recs, halt_request

    def choose_deterministic(self):
        pass
