import arbitrator

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
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)

    def deactive_behavior(self, behavior):
        # Remove an existing behavior from the active behaviors list.
        if behavior in self.behaviors:
            self.active_behaviors.remove(behavior)