#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time
import math

x_pos = 0
y_pos = 0
theta_pos = 0


def callback_func(data):
    global x_pos, y_pos, theta_pos
    
    x_pos = data.x
    y_pos = data.y
    theta_pos = data.theta


def rotate90_clockwise():
    global x_pos, theta_pos
    velocity_message = Twist()
    velocity_message.angular.z = -2
    loop_rate = rospy.Rate(10000)
    command = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    angle_desired = 90
    initialAngle = (theta_pos) * (180/math.pi)
    while not rospy.is_shutdown():
        angle_rotated = abs(((theta_pos) * (180/math.pi)) - initialAngle)
        rospy.loginfo(angle_rotated)

        if angle_rotated >= abs(angle_desired):
            rospy.loginfo("target angle reached...")
            break

        command.publish(velocity_message)
        loop_rate.sleep()
    
    velocity_message.angular.z = 0
    command.publish(velocity_message)

def move_forward(distance):
    global x_pos, y_pos, theta_pos
    velocity_message = Twist()
    velocity_message.linear.x = 2
    loop_rate = rospy.Rate(10)
    command = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    current_pos = x_pos
    # Calculate the initial position
    start_x = x_pos
    start_y = y_pos
    while not rospy.is_shutdown():
        # Compute the distance moved
        distance_moved = ((x_pos - start_x) ** 2 + (y_pos - start_y) ** 2) ** 0.5
        # rospy.loginfo(distance_moved)
        # Stop when the turtle has moved the required distance
        if distance_moved >= distance: 
            rospy.loginfo("Target distance reached. Stopping turtle.")
            break

        # Publish the velocity message
        command.publish(velocity_message)
        loop_rate.sleep()

    # Stop the turtle
    velocity_message.linear.x = 0.0
    command.publish(velocity_message)

if __name__ == '__main__':
    try:
        rospy.init_node('rectange_robot_pub', anonymous=True)
        rospy.Subscriber('/turtle1/pose', Pose, callback_func)
        time.sleep(1.0)

        move_forward(4)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(2)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(4)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(2)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)      

    
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")


# velocity_angle = 'geometry_msgs/Twist'
# # command = rospy.Publisher(velocity_angle, Twist, queue_size=10)
# position = 'turtlesim/Pose'
# pos = rospy.Subscriber(position, Pose, callback_func)
# rospy.spin()