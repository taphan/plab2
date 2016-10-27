import arbitrator
import sensob
import behavior
import motob

class BBCON():
    def __init__(self):
        """
        0: Line not found
        1: Line found
        2: Line end found
        """
        self.line_status = 0 # Blir lest av Color og Wander behaviors for å sjekke om de kan bli aktivert
        self.timestep = 0

        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = arbitrator.Arbitrator()

    def add_behavior(self, behavior):
        # Append a newly-created behavior onto the behaviors list.
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        # Append a newly-created sensob onto the sensobs list.
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        # Add an existing behavior onto the active-behaviors list.
        if behavior in self.behaviors and behavior.active_flag == True:
            self.active_behaviors.append(behavior)

    def deactive_behavior(self, behavior):
        # Remove an existing behavior from the active behaviors list.
        if behavior in self.behaviors and behavior.active_flag == False:
            self.active_behaviors.remove(behavior)

    def run_one_step(self):
        for sob in self.sensobs: # Update all sensobs
            sob.update()

        for behavior in self.active_behaviors: # Update all behaviors
            behavior.update()

        # Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and
        # return that behavior's motor recommendations and halt request flag.
        motor_recs, halt_request = self.arbitrator.choose_action()

        # Update the motobs based on these motor recommendations. The motobs will then update the settings of all motors
        for motob in self.motobs:
            motob.update(motor_recs)



        for sob in self.sensobs: # Reset the sensobs
            sob.reset()
