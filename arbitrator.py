from plab2 import bbcon
import random

class Arbitrator():
    def __init__(self,our_bbcon=bbcon.BBCON()):
        self.bbcon = our_bbcon
        self.motor_recs = None
        self.halt_request = False

    def choose_action(self,stochastic = False):
        if stochastic == False:
            highest_weight = -1
            for behaviours in self.bbcon.active_behaviours:
                if behaviours.weight > highest_weight:
                    highest_weight = behaviours.weight
                    self.motor_recs = behaviours

        elif stochastic == True:
            total_weight = 0
            for behaviours in self.bbcon.active_behaviours:
                total_weight += behaviours.weight
            random_number = random.uniform(0, total_weight)
            range = 0
            for behaviours in self.bbcon.active_behaviours:
                if range <= random_number < behaviours.weight:
                    self.motor_recs = behaviours
                    break
                range= behaviours.weight

        if self.motor_recs.halt_request == True:
            self.halt_request = True
        return self.motor_recs, self.halt_request
