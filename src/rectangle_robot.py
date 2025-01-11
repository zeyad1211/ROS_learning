#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time

# x_pos = 0
# y_pos = 0
# theta_pos = 0


# def callback_func():
#     global x_pos, y_pos, theta_pos
    
#     x_pos = Pose.x
#     y_pos = Pose.y
#     theta_pos = Pose.theta


def rotate90_clockwise():
    velocity_message = Twist()
    velocity_message.angular.z = -2
    loop_rate = rospy.Rate(10)
    command = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    t0 = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - t0 < 0.7854:
        rospy.loginfo('turtle turning clockwise 90')
        command.publish(velocity_message)
        loop_rate.sleep()
    
    velocity_message.angular.z = 0
    command.publish(velocity_message)

def move_forward(time):
    velocity_message = Twist()
    velocity_message.linear.x = 2
    loop_rate = rospy.Rate(10)
    command = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    t0 = rospy.Time.now().to_sec()

    while rospy.Time.now().to_sec() - t0 < time:
        rospy.loginfo("turtle moving forward")
        command.publish(velocity_message)
        loop_rate.sleep()

    velocity_message.linear.x = 0
    command.publish(velocity_message)

if __name__ == '__main__':
    try:
        rospy.init_node('rectange_robot_pub', anonymous=True)
        # rospy.Subscriber('/turtle1/pose', Pose, callback_func)
        move_forward(2)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(1)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(2)
        time.sleep(1.0)
        rotate90_clockwise()
        time.sleep(1.0)

        move_forward(1)
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