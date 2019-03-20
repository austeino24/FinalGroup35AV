#!/usr/bin/env python

import rospy
import roslib
import math
import cv2 as cv

from std_msgs.msg import Int32, Int64, Int8, String, Float64, Float64MultiArray
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes


path = None
curNumObjectsDetected = None
curImage = None

foc_len = 2.1               # focal length in mm (see 'predict' below)
fov = 140                   # field of view in degrees (below)
bottle_avg_height = 330.2   # average real life height (13 in, 330.2mm)
camera_height = 430         # camera height (17in)

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def midpoint(p1, p2):
    return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

def avg(a, b):
    return


class PathFinder:

    def __init__(self, bb):
        self.curBB = bb
        self.projectedAngle = None
        self.projectedLength = None

        if curImage:
            self.imgHeight = curImage.height
            self.imgWidth = curImage.width
            self.imgEncoding = curImage.encoding

            predict()

    # gets 2 nearest <bottle> bounding boxes, finds the midpoints of each and angle away via
    # the field of view & focal length. mynt eye is 140 degrees FOV (both cameras) and focal
    # length of 2.1mm. logitek webcame 60 degrees FOV and focal length of 4mm
    def predict(self):
        lowestDist = float("inf")
        nextLowestDist = float("inf")

        lowestMid = Point(float("inf"), float("inf"))
        nextLowestMid = Point(float("inf"), float("inf"))

        lowestAngle = float("inf")
        nextLowestAngle = float("inf")

        for e in self.curBB:
            curMiddle = Point(((e.xmax-e.xmin) / 2) + e.xmin, ((e.ymax-e.ymin) / 2) + e.ymin)
            if curMiddle.x > (imgWidth / 2):
                curAngle = (fov/2) + (fov/2) * ((curMiddle.x - (imgWidth / 2)) / (imgWidth / 2))
            else:
                curAngle = (fov/2) - (fov/2) * (((imgWidth / 2) - curMiddle.x) / (imgWidth / 2))

            objHeight = e.ymax-e.ymin

            curDistance = foc_len * bottle_avg_height * imgHeight / (objHeight * camera_height)

            if curDistance < lowestDist:
                nextLowestDist = lowestDist
                nextLowestMid = lowestMid
                nextLowestAngle = lowestAngle

                lowestDist = curDistance
                lowestMid = curMiddle
                lowestAngle = curAngle

            elif curDistance < nextLowest:
                nextLowestDist = curDistance
                nextLowestMid = curMiddle
                nextLowestAngle = curAngle

        xLow = math.sin(lowestAngle) * lowestDist
        yLow = math.cos(lowestAngle) * lowestDist

        xHigh = math.sin(nextLowestAngle) * nextLowestDist
        yHigh = math.cos(nextLowestAngle) * nextLowestDist

        if lowestAngle < 90:
            xLow = -xLow

        if nextLowestAngle < 90:
            xHigh = -xHigh

        low = Point(xLow, yLow)
        high = Point(xHigh, yHigh)

        goal = midpoint(low, high)

        self.projectedLength = distance(goal, Point(0, 0))
        self.projectedAngle = math.atan(goal.x / goal.y)


def num_objects_fcb(msg):
    global curNumObjectsDetected
    curNumObjectsDetected = msg.data
    print("num objects = ", msg.data)


def detection_image_fcb(msg):
    global curImage
    curImage = msg.data


def bounding_boxes_fcb(msg):
    global path

                                # each bounding box has attributes: string Class, float64 probability,
    cur_bounding_boxes = []     #                                   int64 xmin, ymin, xmax, ymax

    if curNumObjectsDetected > 1:

        print("Current bounding box data: ", msg.data)

        for e in msg.data:
            if e.Class == 'bottle' or e.Class == 'Bottle' and e.probability >= 0.5:
                cur_bounding_boxes.append(e)

    path = PathFinder(cur_bounding_boxes)


if __name__ == '__main__':
    rospy.init_node('path_finder')

    numObjectsSub = rospy.Subscriber('/darknet_ros/found_object', Int8, num_objects_fcb)
    imageSub = rospy.Subscriber('/darknet_ros/detection_image', Image, detection_image_fcb)
    boundingBoxesSub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, bounding_boxes_fcb)

    angle_pub = rospy.Publisher('projected_angle', Float64, queue_size=1)
    distance_pub = rospy.Publisher('projected_distance', Float64, queue_size=1)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if path:
            angle_pub.publish(path.projectedAngle)
            distance_pub.publish(path.projectedLength)

            print(path.projectedAngle)
            print(path.projectedLength)

        rate.sleep()
