__author__ = 'keithd'

from time import sleep
import random
import imager2 as IMR
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from motors import Motors
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
import arbitrator
import bbcon
import sensob
import behavior
import motob


## BE SURE TO RUN THESE DEMOS ON THE FLOOR or to have plenty of people guarding
## #  the edges of a table if it is run there.

# This just moves the robot around in a fixed dance pattern.  It uses no sensors.
zumobutton = ZumoButton()

def main():
    zumobutton.wait_for_press()
    our_bbcon = bbcon.BBCON()
    our_arbitrator = our_bbcon.arbitrator

    wander = behavior.Wander(our_bbcon)
    avoid_obs = behavior.AvoidObstacles(our_bbcon)
    color = behavior.Color(our_bbcon)
    find_line = behavior.FindLine(our_bbcon)
    ir = behavior.IRFollow(our_bbcon)

    wander.active_flag = True
    wander.update()
    our_arbitrator.motor_recs = wander.motor_recs

    our_bbcon.add_behavior(color)

    our_bbcon.add_behavior(wander)
    our_bbcon.activate_behavior(wander)

    our_bbcon.add_behavior(avoid_obs)
    our_bbcon.activate_behavior(avoid_obs)

    our_bbcon.add_behavior(find_line)
    our_bbcon.activate_behavior(find_line)

    our_bbcon.add_behavior(ir)
    our_bbcon.activate_behavior(ir)
    count = 0
    while count <10:
        our_bbcon.run_one_step()
        count+=1
        if our_bbcon.halt_request:
            break


def dancer():
    ZumoButton().wait_for_press()
    m = Motors()
    m.forward(.2,3)
    m.backward(.2,3)
    m.right(.5,3)
    m.left(.5,3)
    m.backward(.3,2.5)
    m.set_value([.5,.1],10)
    m.set_value([-.5,-.1],10)


# This tests the UV (distance) sensors.  The robot moves forward to within 10 cm of the nearest obstacle.  It
# then does a little dancing before backing up to approximately 50 cm from the nearest obstacle.

def explorer(dist=10):
    ZumoButton().wait_for_press()
    m = Motors(); u = Ultrasonic()
    while u.update() > dist:
        m.forward(.2,0.2)
    m.backward(.1,.5)
    m.left(.5,3)
    m.right(.5,3.5)
    sleep(2)
    print("test:", u.get_value())
    while u.update() < dist*5:
        print(u.update())
        m.backward(.2,0.2)
    m.left(.75,5)


def random_step(motors,speed=0.25,duration=1):
    dir = random.choice(['forward','backward','left','right'])
    eval('Motors.'+ dir)(motors,speed,duration)

# This moves around randomly until it gets to a dark spot on the floor (detected with the infrared belly sensors).
# It then rotates around, snapping pictures as it goes.  It then pastes all the pictures together into a
# panoramo view, many of which may be created per "vacation".

def tourist(steps=25,shots=5,speed=.25):
    zumobutton.wait_for_press()
    rs = ReflectanceSensors(); m = Motors(); c = Camera()
    for i in range(steps):
        random_step(m,speed=speed,duration=0.5)
        vals = rs.update()
        if sum(vals) < 1:  # very dark area
            #im = shoot_panorama(c,m,shots)
            #im.dump_image('vacation_pic'+str(i)+'.jpeg')
            print("Found line! Vals: ",vals)

def shoot_panorama(camera=Camera(),motors=Motors(),shots=5):
    s = 1
    im = IMR.Imager(image=camera.update()).scale(s,s)
    rotation_time = 3/shots # At a speed of 0.5(of max), it takes about 3 seconds to rotate 360 degrees
    for i in range(shots-1):
        motors.right(0.5,rotation_time)
        im = im.concat_horiz(IMR.Imager(image=camera.update()))
    return im

