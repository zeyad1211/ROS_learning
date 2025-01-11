#!/usr/bin/env python
import rospy
from learning_motion.msg import parameters
import sys

pub = rospy.Publisher('width_hieght', parameters, queue_size=10)
rospy.init_node('paramerPublisher', anonymous=True)

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    parameter = parameters()
    parameter.Length = float(input("Length: "))
    parameter.Width = float(input("Width: "))
    rospy.loginfo('publishing...' + 'length: ' + str(parameter.Length) + 'width: ' + str(parameter.Width) )
    pub.publish(parameter)
    rate.sleep()

