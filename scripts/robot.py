#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import math

vel = Twist()
message = ""
at_kitchen = False
at_table1 = False
at_table2 = False

def callback1(odom):
    global x, y, theta
    x = odom.pose.pose.position.x
    y = odom.pose.pose.position.y
    theta = odom.pose.pose.orientation.z
    # print(round(x, 2), round(y, 2))
    return 0

def callback2(data):
    global message
    message = data.data.lower()
    # print(message)
    return 0

def go_to(goalx, goaly):
    global at_kitchen, at_table1, at_table2
    robotAngle = math.asin(theta)
    dy,dx = (goaly - y), (goalx- x)
    slop = dy/dx

    if dx<0 and dy>0:
        goalAngle = math.pi + math.atan(slop)
    elif dx<0 and dy<0:
        goalAngle = math.atan(slop) - math.pi
    else:
        goalAngle = math.atan(slop)

    angleDiff = goalAngle - 2*robotAngle
    # angleDiff = math.atan((goaly - y) / (goalx- x)) - 2*robotAngle
    linear = math.sqrt((goalx - x)**2 + (goaly - y)**2)
    if abs(angleDiff) > 0.01:
        angular_vel = 1.5*angleDiff
        linear_vel = 0
    else:
        angular_vel = 0

        if abs(linear) > 0.05:
            linear_vel = 0.5*linear
        else:
            linear_vel = 0
            if (goalx, goaly) == (0.09, -3.00):
                at_kitchen = True
            if (goalx, goaly) == (3, 3):
                at_table1 = True
                # at_kitchen = False
            if (goalx, goaly) == (5.1, 0.48):
                at_table2 = True
    return linear_vel, angular_vel


def robot():
    rospy.init_node('robot')
    rospy.Subscriber('/odom', Odometry, callback1)
    rospy.Subscriber('chatter', String, callback2)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy. sleep(1)
    rate = rospy.Rate(10)
    # goalx, goaly = 3, -3
 
    print("Waiting for the orders!")
    while not rospy.is_shutdown():
        if 'order' in message and not at_kitchen:
            linear_vel, angular_vel = go_to(0.09, -3.00)
            vel.linear.x = linear_vel
            vel.angular.z = angular_vel
        if 't1' in message and at_kitchen:
            linear_vel, angular_vel = go_to(3, 3)
            vel.linear.x = linear_vel
            vel.angular.z = angular_vel
        if 't2' in message and (('t1' in message and at_table1) or ('t1' not in message and at_kitchen)):
            linear_vel, angular_vel = go_to(5.1, 0.48)
            vel.linear.x = linear_vel
            vel.angular.z = angular_vel
        # if message.lower() == 't3':
        #     linear_vel, angular_vel = go_to(4.95, -5.66)
        #     vel.linear.x = linear_vel
        #     vel.angular.z = angular_vel
        if 'home' in message and (('t1' in message and 't2' not in message and at_table1) or ('t2' in message and 't1' not in message and at_table2) or (('t1' in message and 't2' in message and at_table2))):
            linear_vel, angular_vel = go_to(0.5, -5.85)
            vel.linear.x = linear_vel
            vel.angular.z = angular_vel

        # print(round(vel.linear.x, 2), round(vel.angular.z, 2))
        pub.publish(vel)
        rate.sleep()


if __name__ == '__main__':

    try:
        robot()
    except rospy.ROSInterruptException:
        pass