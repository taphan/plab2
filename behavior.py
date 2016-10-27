import bbcon
import sensob
import motob

class Behavior():

    def __init__(self):
        # Pointer to the controller that uses this behavior
        self.bbcon = bbcon.BBCON()
        self.sensobs = []
        self.motor_recs = ('L', 0) # Recs motor to the arbitrator
        self.active_flag = False
        self.halt_request = False
        self.priority = 0 # Static
        self.match_degree = 0.0 # Et reelt tall mellom 0 og 1
        self.weight = 0.0 # Product of priority og match_degre

    def consider_deactivation(self):
        raise NotImplementedError

    def consider_activation(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def sense_and_act(self):
        raise NotImplementedError

class Color(Behavior):

    def __init__(self):
        super(Color, self).__init__()
        self.priority = 1
        self.line_status = self.bbcon.line_status
        self.sensor = sensob.CameraSensob()
        self.sensobs.append(self.sensor)

    def consider_deactivation(self):
        if self.active_flag: # Forsørg at testen skjer bare når den er på
            self.active_flag = False

    def consider_activation(self):
        # Aktiveres kun når enden av linjen er funnet
        if self.line_status == 2:
            self.active_flag = True

    def update(self):
        if not self.active_flag:
            self.sensor.reset()
        else:
            self.sense_and_act()
            self.weight = self.priority*self.match_degree

    def sense_and_act(self):
        """
        Rød: Snu venstre
        Blå: Snu høyre
        Grønn: Snu 180 grader og stopp
        """
        self.sensor.update()
        color = self.sensor.get_color()
        if color == 'red':
            self.motor_recs = ('L', 90)
        elif color == 'blue':
            self.motor_recs = ('R', 90)
        else:
            self.motor_recs = ('L', 180)
            self.halt_request = True # Stopper hele testen dersom


class FollowLine(Behavior):

    def __init__(self):
        super(FollowLine, self).__init__()
        sensor = sensob.ReflectanceSensOb()
        self.sensobs.append(sensor)
        self.active_flag = True
        self.priority = 0.7
        self.steps_line_followed = 0
        self.line_found_flag = False

    def consider_deactivation(self):
        line_status = 1
        if line_status == 2:
            self.active_flag = False
            return True

    def consider_activation(self):
        line_status = 0
        if line_status == 0:
            self.active_flag = True
            return True
        elif line_status == 1:
            self.active_flag = True
            return True

    def sense_and_act(self):
        if self.line_found_flag:
            self.follow_line()
        else:
            self.find_line()

    def follow_line(self):
        pass

    def find_line(self):
        sensor = self.sensobs[0]