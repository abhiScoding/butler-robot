#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

vel = Twist()

def callback(odom):
    global x, y, theta
    x = odom.pose.pose.position.x
    y = odom.pose.pose.position.y
    theta = odom.pose.pose.orientation.z
    # print(round(x, 2), round(y, 2))
    return 0


def robot():
    rospy.init_node('robot')
    rospy.Subscriber('/odom', Odometry, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy. sleep(1)
    rate = rospy.Rate(10)
    goalx, goaly = 3, -3
    robotAngle = math.asin(theta)
    angleDiff = math.atan((goaly - y) / (goalx- x)) - 2*robotAngle
    linear = 0.5*math.sqrt((goalx - x)**2 + (goaly - y)**2)
    while not rospy.is_shutdown():

        while abs(angleDiff) > 0.03:
            robotAngle = math.asin(theta)
            angleDiff = math.atan((goaly - y) / (goalx- x)) - 2*robotAngle
            vel.angular.z = 1.5*angleDiff
            pub.publish(vel)
        vel.angular.z = 0

        while abs(linear) > 0.05:

            linear = 0.5*math.sqrt((goalx - x)**2 + (goaly - y)**2)
            vel.linear.x = linear
            pub.publish(vel)
        vel.linear.x = 0
        print(vel.linear.x, vel.angular.z)
        pub.publish(vel)
        rate.sleep()


if __name__ == '__main__':

    try:
        robot()
    except rospy.ROSInterruptException:
        pass