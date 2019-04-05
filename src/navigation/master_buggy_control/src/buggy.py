#!/usr/bin/env python

import rospy
import time
import math
from std_msgs.msg import Int16
from std_msgs.msg import Float64

'''
*****************************************************************
*   This function contains the main functionality of the buggy  *
*   - Prototype buggy parameters -                              *
*                                                               *
*   Actuator range:                                             *
*   ---------------- Max right:   700                           *
*   ---------------- Max left:    350                           *
*   Motor max speed:                                            *
*   ---------------- RPM:         100                           *
*   Direction:                                                  *
*   ---------------- Forward:       0                           *
*   ---------------- Reverse:       1                           *
*****************************************************************
'''

current_actuator_val = 350

# Main logic for turning towards path here (turns to angle calculated in path_finder)
def angle_fcb(val):
    global current_angle
    if val.data:
        current_angle = val.data #current angle will be negative for a left turn, positive for right up to 30 deg/either

    angle_diff = math.fabs(current_angle)

    if angle_diff < 5:
        actuator_publish(525)

    elif angle_diff < 12.5:
        if current_angle > 0:
            turn('r', 'slight')
        else:
            turn('l', 'slight')

    elif angle_diff < 20:
        if current_angle > 0:
            turn('r', 'moderate')
        else:
            turn('l', 'moderate')

    else:
        if current_angle > 0:
            turn('r', 'sharp')
        else:
            turn('l', 'sharp')


# function for turning. dir = r (right) l (left) and type = sharp (close to 30 deg) moderate (20ish) tiny (10)
# right = 700 max, left = 350 max
def turn(dir, type):
    global current_actuator_val

    if dir == 'l':
        if type == 'sharp':
            while current_actuator_val > 353:
                actuator_publish(350)
            actuator_publish(525)
        elif type == 'moderate':
            while current_actuator_val > 353:
                actuator_publish(350)
            actuator_publish(525)
        elif type == 'tiny':
            while current_actuator_val > 353:
                actuator_publish(350)
            actuator_publish(525)

    elif dir == 'r':
        if type == 'sharp':
            while current_actuator_val < 696:
                actuator_publish(700)
            actuator_publish(525)
        elif type == 'moderate':
            while current_actuator_val < 353:
                actuator_publish(350)
            actuator_publish(525)
        elif type == 'tiny':
            while current_actuator_val < 353:
                actuator_publish(350)
            actuator_publish(525)


def length_fcb(val):
    global length
    length = val

    i = 0


def actuator_fcb(val):
    global current_actuator_val
    current_actuator_val = val

    #print("actuator callback")
    #motor_publish(100)


    '''
    global cond
    global starttime
    global act_callback_num

    if val.data < 698 and cond == 1:
        actuator_publish(700)
        print("PUBLISHING 700")
        if act_callback_num == 0:
            starttime = int(round(time.time()*1000))
    elif val.data > 528:
        actuator_publish(525)
        if cond == 1:
            print("Final time elapsed: ",  int(round(time.time()*1000)) - starttime)
        cond = 0
    else:
        motor_publish(0)

    act_callback_num += 1 '''


def motor_fcb(val):
    global motor_rpm
    motor_rpm = val.data

    #motor_publish(0)
    #dir_publish(0)
    #print("motor callback")


def dir_publish(direction):
    pub_motor_dir = rospy.Publisher('dir', Int16, queue_size=1)
    # Publish to topic
    #rospy.loginfo(direction)
    pub_motor_dir.publish(direction)


def motor_publish(rpm):
    pub_motor_rpm = rospy.Publisher('rpm', Int16, queue_size=1)
    # Publish to topic
    #rospy.loginfo(rpm)
    pub_motor_rpm.publish(rpm)


def actuator_publish(pos):
    pub_actuator = rospy.Publisher('pos', Int16, queue_size=1)
    # Publish to topic
    #rospy.loginfo(pos)
    pub_actuator.publish(pos)


def buggy():
    rospy.init_node('buggy', anonymous=True)  # test

    # Initialize Node
    rospy.Subscriber('projected_angle', Float64, angle_fcb)
    rospy.Subscriber('projected_length', Float64, length_fcb)

    print("Subscribing to actuator")

    rospy.Subscriber('actuator_val', Int16, actuator_fcb)
    rospy.Subscriber('motor_val', Int16, actuator_fcb)
    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        rate.sleep()
       

if __name__ == '__main__':
    try:
        buggy()
    except rospy.ROSInterruptException:
        pass
