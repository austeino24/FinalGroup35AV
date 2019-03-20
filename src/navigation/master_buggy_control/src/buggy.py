#!/usr/bin/env python

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
import random
import _random
from std_msgs.msg import Int16
from std_msgs.msg import Byte
from std_msgs.msg import ByteMultiArray

def stop_buggy(r,d):
    r *=-1
    d = not d
    return (r, d)

def sens_array(val):
    # Create motor topics
    pub_motor_rpm = rospy.Publisher('rpm', Int16, queue_size=1)
    pub_motor_dir = rospy.Publisher('dir', Int16, queue_size=1)
    # Create Linear Actuator topic
    pub_actuator = rospy.Publisher('pos', Int16, queue_size=1)

    # rpm = 100
    dir = 1
    # pos = 500
    #
    #
    # # Publish motor topics
    # rospy.loginfo(dir)
    # pub_motor_dir.publish(dir)
    # rospy.loginfo(rpm)
    # pub_motor_rpm.publish(rpm)
    #
    # # Publish Linear Actuator topics
    # rospy.loginfo(pos)
    # pub_actuator.publish(pos)
    # rate.sleep()
    
    front_read = []
    rear_read = []
    left_read = []
    right_read = []

    arr = list()
    arr = val.data

    #  8ft. => 96in.
    front_read.append(arr[1])
    front_read.append(arr[2])

    # The below line reads all 4 sensors for forward motion
    #if arr[0] < 48 or arr[1] < 48 or arr[2] < 48 or arr[3] < 48:

    if arr[1] < 10 or arr[2] < 10:
        print("\nObjects too close........ Stopping buggy\n")

        # dir = random.randrange(0, 2)  # Brake
        # rospy.loginfo(dir)
        # pub_motor_dir.publish(dir) # Reverse dir polarity
        rpm = 0
        rospy.loginfo(rpm)
        pub_motor_rpm.publish(rpm)

        pos = random.randrange(0, 1001)  # linear actuator position 0 ~ 1000
        rospy.loginfo(pos)
        pub_actuator.publish(pos)  # Reverse dir polarity
    else:
        rpm = 100

        # Publish motor topics
        #rospy.loginfo(dir)
        #pub_motor_dir.publish(dir)
        rospy.loginfo(rpm)
        pub_motor_rpm.publish(rpm)


    # dir = int(not dir)
    # rospy.loginfo(dir)
    # pub_motor_dir.publish(dir)
    # rospy.loginfo(rpm)
    # pub_motor_rpm.publish(rpm)

    # rear_read.append(arr[4])
    # rear_read.append(arr[5])
    #
    # left_read.append(arr[0])
    # left_read.append(arr[1])
    #
    # right_read.append(arr[2])
    # right_read.append(arr[3])

    print("arr is " + str(arr))
    print("front_sensors" + str(front_read))
    # print("rear_sensors " + str(rear_read))
    # print("left_sensors " + str(left_read))
    # print("right_sensors" + str(right_read))


def buggy():
    rospy.init_node('buggy', anonymous=True)  # test

    # Initialize Node
    rospy.Subscriber('sens', ByteMultiArray, sens_array)
    
    rate = rospy.Rate(1) # 10hz
    x = 0

    while not rospy.is_shutdown():
        rate.sleep()
       

if __name__ == '__main__':
    try:
        buggy()
    except rospy.ROSInterruptException:
        pass
