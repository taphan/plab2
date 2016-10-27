import motors

class Motob():
    # Den skal få motor recommendation (mr) fra Arbitrator, og send videre motor settings til Motor-ene av klasse Motors

    def __init__(self, motors_list=motors.Motors(), value=[]):
        # Forslag: value kan være en stack?
        self.motors = motors_list # Egentlig bare ett Motors-objekt, trenger ikke å være en liste
        self.value = value

    def update(self, mr): # Får inn en mr, last inn i value
        self.value.append(mr)
        self.operationalize(mr)

    def operationalize(self, mr):
        # Først sjekk om mr er for venstre eller høyre hjul, mr er f.eks. (L, 45)
        if mr[0] == 'L':
            self.motors.set_value((mr[1], 0))
        elif mr[0] == 'R':
            self.motors.set_value((0, mr[1]))

