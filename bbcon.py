import arbitrator
import sensob
import behavior
import motob
import time

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
        self.motob = motob.Motob()
        self.arbitrator = arbitrator.Arbitrator(self)


    def add_behavior(self, behavior):
        # Append a newly-created behavior onto the behaviors list.
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        # Append a newly-created sensob onto the sensobs list.
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        # Add an existing behavior onto the active-behaviors list.
        if behavior in self.behaviors:
            behavior.active_flag = True
            self.active_behaviors.append(behavior)

    def deactive_behavior(self, behavior):
        # Remove an existing behavior from the active behaviors list.
        if behavior in self.behaviors:
            behavior.active_flag = False
            self.active_behaviors.remove(behavior)

    def run_one_step(self):
        for sob in self.sensobs: # Update all sensobs
            sob.update()
        for behavior in self.behaviors:
            behavior.consider_activation()
            if behavior not in self.active_behaviors and behavior.active_flag == True:
                self.activate_behavior(behavior)
        for behavior in self.active_behaviors: # Update all behaviors
            behavior.consider_deactivation()
            if behavior.active_flag == False:
                self.deactive_behavior(behavior)
            else:
                behavior.update()
            if behavior.name == 'FindLine':
                self.line_status = behavior.get_line_status()
        # Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and
        # return that behavior's motor recommendations and halt request flag.
        motor_recs, halt_request = self.arbitrator.choose_action()
        # Update the motobs based on these motor recommendations. The motobs will then update the settings of all motors
        if not halt_request:
            self.motob.update(motor_recs)
            print("bbcon runonestep test gir motor recs: ", motor_recs)
        else:
            self.motob.stop_motor()
        # Wait - This pause (in code execution) will allow the motor settings to remain active for a short period
        # of time, e.g., one half second, thus producing activity in the robot, such as moving forward or turning.
<<<<<<< HEAD
        time.sleep(0.5)

=======
        time.sleep(1.5)
>>>>>>> f9b144e90ed9501f72d55de2211164d1c64a9d72
        for sob in self.sensobs: # Reset the sensobs
            sob.reset()
            motor_recs = ('F',90)
