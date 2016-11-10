import bbcon
import random

class Arbitrator():

    def __init__(self,our_bbcon):
        self.bbcon = our_bbcon
        self.motor_recs = None
        self.halt_request = False

    def choose_action(self,stochastic = False):
        if stochastic == False:
            highest_weight = -1
            for behavior in self.bbcon.active_behaviors:
                if behavior.weight > highest_weight:
                    highest_weight = behavior.weight
                    self.motor_recs = behavior.motor_recs

        elif stochastic == True:
            total_weight = 0
            for behavior in self.bbcon.active_behaviors:
                total_weight += behavior.weight
            random_number = random.uniform(0, total_weight)
            range = 0
            for behavior in self.bbcon.active_behaviors:
                if range <= random_number < behavior.weight:
                    self.motor_recs = behavior.motor_recs
                    break
                range= behavior.weight

        return self.motor_recs, self.halt_request
