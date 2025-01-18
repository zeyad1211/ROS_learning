#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

front_range = None
angle_min = None
angle_max = None
angle_increment = None

def scan_callback(scan_data):
    global front_range, right_range, left_range, angle_increment, angle_max, angle_min
    angle_min = scan_data.angle_min
    angle_increment = scan_data.angle_increment
    laserdata = scan_data.ranges
    front = data_from_angles(345, 15, laserdata)
    front_range = minimum_range(front)
    left = data_from_angles(15, 45, laserdata)
    left_range = minimum_range(left)
    right = data_from_angles(315, 345, laserdata)
    right_range = minimum_range(right)
    rospy.loginfo('___________FRONT__________')
    rospy.loginfo(front_range)
    rospy.loginfo('___________RIGHT__________')
    rospy.loginfo(right_range)
    rospy.loginfo('___________LEFT__________')
    rospy.loginfo(left_range)    

    # rospy.loginfo(laserdata)

def data_from_angles(angle1, angle2, arr_name):
    global angle_min, angle_increment
    # Angle range you want to extract (in radians)
    # Convert angles to indices
    start_index = angle_to_index(angle1, angle_min, angle_increment)
    end_index = angle_to_index(angle2, angle_min, angle_increment)
    rospy.loginfo(f"Start Index: {start_index}, End Index: {end_index}")
    
    # Handling circular list split
    if start_index < end_index:
        # Normal case, no wraparound
        laserdata = arr_name[start_index:end_index+1]
    else:
        # Wraparound case
        laserdata = arr_name[start_index:] + arr_name[:end_index+1]
    
    # rospy.loginfo(f"Filtered Laser Data: {laserdata}")
    return laserdata


def angle_to_index(angle, angle_min, angle_increment):

    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Calculate the index
    index = int((angle_rad - angle_min) / angle_increment)

    return index


def minimum_range(data):
    numeric_data = [x for x in data if isinstance(x, (int, float)) and math.isfinite(x)]
    if not numeric_data:
        return 0  # Handle empty or invalid data
    return sum(numeric_data)/len(numeric_data)


def move():
    global front_range, right_range, left_range
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity_msg = Twist()
    rate = rospy.Rate(10)
    Kp = 0.3
    Ka = 0.6
    while not rospy.is_shutdown():
        if front_range is None:
            rospy.logwarn("Waiting for LaserScan left_rangedata...")
            rate.sleep()
            continue
        else:
            velocity_msg.linear.x = Kp * front_range
            if velocity_msg.linear.x > 2:
                velocity_msg.linear.x = 2
            if left_range < 0.6 or right_range < 0.6 or front_range < 0.8:
                velocity_msg.angular.z = Ka * (left_range - right_range)
                if front_range < 0.6 and abs(left_range-right_range) < 0.2:
                    velocity_msg.angular.z = 1.2 
            else:
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
# SSS