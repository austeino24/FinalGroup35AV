#!/usr/bin/env python

import rospy
import roslib
import math
import cv2 as cv

from std_msgs.msg import Int32, Int64, Int8, String, Float64, Float64MultiArray
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from math import sqrt


##########################################################################
# Path planner for UCF Beach Buggy Snr. Design Project                   #
#                                                                        #
# INPUTS ROS output from darknet module including bounding box info      #
#                                                                        #
# OUTPUTS Angle (negative if                                                                        #

path = None
curNumObjectsDetected = None
curImage = None

foc_len = 2.1               # focal length in mm (see 'predict' below)
fov = 140                   # field of view in degrees (below)
bottle_avg_height = 330.2   # average real life height (13 in, 330.2mm)
camera_height = 3           # height of the literal camera (3mm)

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

            # print("Cur image width/height: ", self.imgWidth, "/", self.imgHeight)

            self.predict()

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

        if self.curBB:

            for e in self.curBB:

               # print("Current bounding box info, xmax, xmin, ymax, ymin", e.xmax, e.xmin, e.ymax, e.ymin)

                curMiddle = Point(((e.xmax - e.xmin) / 2) + e.xmin, ((e.ymax - e.ymin) / 2) + e.ymin)

                halfImg = float(self.imgWidth / 2)

                if curMiddle.x > halfImg:
                    imgDiff = (curMiddle.x - halfImg)
                    proportion = (imgDiff / halfImg)
                    curAngle = ((fov/2) + (fov/2) * proportion)
                else:
                    curAngle = ((fov/2) - (fov/2) * ((halfImg - curMiddle.x) / halfImg))

                objHeight = e.ymax-e.ymin

                #print("Current middle/ angle: ", curMiddle.x, curAngle)

                curDistance = foc_len * bottle_avg_height * self.imgHeight / (objHeight * camera_height)

                if curDistance < lowestDist:
                    nextLowestDist = lowestDist
                    nextLowestMid = lowestMid
                    nextLowestAngle = lowestAngle

                    lowestDist = curDistance
                    lowestMid = curMiddle
                    lowestAngle = curAngle

                elif curDistance < nextLowestDist:
                    nextLowestDist = curDistance
                    nextLowestMid = curMiddle
                    nextLowestAngle = curAngle
        else:
            print("Not enough bottles to to plan")
            return

        #print("Nearest bottle distances/ angles: ", lowestDist, "/", lowestAngle, " & ", nextLowestDist, "/", nextLowestAngle)


        if lowestAngle < 70:
            lowestAngle = 70 - lowestAngle
            xLow = math.sin(math.radians(lowestAngle)) * lowestDist
            yLow = math.cos(math.radians(lowestAngle)) * lowestDist

            xLow = -xLow
        else:
            lowestAngle -= 70
            xLow = math.sin(math.radians(lowestAngle)) * lowestDist
            yLow = math.cos(math.radians(lowestAngle)) * lowestDist

        if nextLowestAngle < 70:
            nextLowestAngle = 70 - nextLowestAngle
            xHigh = math.sin(math.radians(nextLowestAngle)) * nextLowestDist
            yHigh = math.cos(math.radians(nextLowestAngle)) * nextLowestDist

            xHigh = -xHigh
        else:
            nextLowestAngle -= 70
            xHigh = math.sin(math.radians(nextLowestAngle)) * nextLowestDist
            yHigh = math.cos(math.radians(nextLowestAngle)) * nextLowestDist

        #print("low x/y high: ", xLow, yLow, xHigh, yHigh)

        low = Point(xLow, yLow)
        high = Point(xHigh, yHigh)

        goal = midpoint(low, high)

        self.projectedLength = distance(goal, Point(0, 0))
        self.projectedAngle =  math.degrees(math.atan(goal.x / goal.y))


def num_objects_fcb(msg):
    global curNumObjectsDetected
    curNumObjectsDetected = msg.data
    #print("num objects = ", msg.data)


def detection_image_fcb(msg):
    global curImage
    curImage = msg


def bounding_boxes_fcb(msg):
    global path

                                # each bounding box has attributes: string Class, float64 probability,
    cur_bounding_boxes = []     #                                   int64 xmin, ymin, xmax, ymax

    if curNumObjectsDetected > 1:

        #print("Current bounding box data: ", msg.bounding_boxes)

        for e in msg.bounding_boxes:
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

            print("Projected angle is: ", path.projectedAngle)
            print("Projected length is: ", path.projectedLength)

        rate.sleep()
