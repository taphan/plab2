class BBCON():
    def __init__(self):
        """
        0: Line not found
        1: Line found
        2: Line end found
        """
        self.line_status = 0 # Blir lest av Color og Wander behaviors for å sjekke om de kan bli aktivert
