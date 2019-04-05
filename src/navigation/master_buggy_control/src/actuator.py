#!/usr/bin/env python

import rospy
from smbus2 import SMBus, i2c_msg
from std_msgs.msg import Int16

la_address = 11
bus = SMBus(0)


def write_array(value):
    print("Current writing to linact:", value)
    bus.write_i2c_block_data(la_address, 0, value)
    return -1


def read_array():
    tmpvar = bus.read_i2c_block_data(la_address, 0, 2)
    print("reading i2c la_address, 0 , 2")

    position = tmpvar[0]
    position = (position << 8) | tmpvar[1]

    print("Current Actuator val: ", position)
    pos_16 = Int16(data=position)
    return pos_16


def pos(data):
    rospy.loginfo(rospy.get_caller_id() + ' POS = %d', data.data)

    array = list()
    array.append((data.data >> 8) & 0xFF)
    array.append(data.data & 0xFF)
    write_array(array)


def actuator():
    # The anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('actuator', anonymous=True)

    rospy.Subscriber('pos', Int16, pos)
    actuator_val_pub = rospy.Publisher('actuator_val', Int16, queue_size=1)

    rate = rospy.Rate(2)  # 10hz

    while not rospy.is_shutdown():
        actuator_val_pub.publish(read_array())
        rate.sleep()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    actuator()
