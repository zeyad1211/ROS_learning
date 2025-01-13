#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

minimumRange = None

def scan_callback(scan_data):
    global laserdata
    global minimumRange

    laserdata = list(scan_data.ranges[0:6]) + list(scan_data.ranges[355:361])
    minimumRange = minimum_range(laserdata)
    rospy.loginfo(minimumRange)
    # rospy.loginfo(laserdata)


def minimum_range(data):
    numeric_data = [x for x in data if isinstance(x, (int, float)) and math.isfinite(x)]
    if not numeric_data:
        return 0  # Handle empty or invalid data
    return min(numeric_data)


def move():
    global minimumRange
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity_msg = Twist()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if minimumRange is None:
            rospy.logwarn("Waiting for LaserScan data...")
            rate.sleep()
            continue
        if minimumRange == 0:
            rospy.loginfo("perfect...")
            velocity_msg.linear.x = 0.3
            velocity_msg.angular.z = 0
            pub.publish(velocity_msg)
            
        elif minimumRange < 0.6:  # Example threshold for obstacle avoidance
            rospy.loginfo("Obstacle detected! Stopping.")
            velocity_msg.linear.x = 0
            velocity_msg.angular.z = 0.2
            pub.publish(velocity_msg)
            while minimumRange !=0 and minimumRange < 3:
                rospy.loginfo("Turning...")
                rate.sleep()
        else:
            rospy.loginfo("Path is clear. Moving forward.")
            velocity_msg.linear.x = 0.3  # Move forward
            velocity_msg.angular.z = 0
            pub.publish(velocity_msg)

        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('autonomous_turtlebot', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, scan_callback)
        move()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")

# difficulties.....
# trying to make the laserscanner only see -5, +5 degrees instead of only using -5,+5 degrees for data
# filtering the data by removing non numeric values
# not knowing how to concatenate two tuples
# 