import motors

class Motob():
    # Den skal få motor recommendation fra Arbitrator, og send videre motor settings til Motor-ene av klasse Motors

    def __init__(self, value=[]):
        # Forslag: value kan være en stack?
        self.motors = motors.Motors() # Egentlig bare ett Motors-objekt, trenger ikke å være en liste
        self.value = value

    def update(self, motor_rec): # Får inn en mr, last inn i value
        self.value.append(motor_rec)
        self.operationalize(motor_rec)

    def operationalize(self, motor_rec):
        # Først sjekk om mr er for venstre eller høyre hjul, mr er f.eks. (L, 45)
        # Make robot rotate 90 grader
        if motor_rec[0] == 'L':
            self.motors.set_value([.5, -.5], motor_rec[1] / 60) # Endrer på disse verdiene etter testing
        elif motor_rec[0] == 'R':
            self.motors.set_value([-.5, .5], motor_rec[1] / 60) # 90 grader = 1 second, 180 grader = 3 seconds
        elif motor_rec[0] == 'F':
            self.motors.forward(.4,0.4)
        elif motor_rec[0] == 'S':
            self.motors.stop()

    def stop_motor(self):
        self.motors.stop()