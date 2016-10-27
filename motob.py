import motors

class Motob():
    # Den skal få motor recommendation fra Arbitrator, og send videre motor settings til Motor-ene av klasse Motors

    def __init__(self, motors_list=motors.Motors(), value=[]):
        # Forslag: value kan være en stack?
        self.motors = motors_list # Egentlig bare ett Motors-objekt, trenger ikke å være en liste
        self.value = value

    def update(self, motor_rec): # Får inn en mr, last inn i value
        self.value.append(motor_rec)
        self.operationalize(motor_rec)

    def operationalize(self, motor_rec):
        # Først sjekk om mr er for venstre eller høyre hjul, mr er f.eks. (L, 45)
        if motor_rec[0] == 'L':
            self.motors.set_value((0.5, -0.5)) # Endrer på disse verdiene etter testing
        elif motor_rec[0] == 'R':
            self.motors.set_value((-0.5, 0.5))

