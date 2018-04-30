#!/usr/bin/env python
import rospy, sys, select, time, datetime, math, random

from std_msgs.msg import Header, Bool
from geometry_msgs.msg import Pose, PoseStamped, Point
from hector_uav_msgs.srv import EnableMotors
from nav_msgs.msg import Odometry

CPS_DIR = "/home/saeed/cps_ws/src/cps_quadrotor/"

msg = """
Publishing commands to /cps/path_planner!
---------------------------
Listening to /cps/command_reached for acknowledgements

CTRL-C to quit
"""

# CONFIGURATIONS

# CONSTANTS
CMD_PUB = rospy.Publisher('/cps/path_planner', Point, queue_size = 1)

# GLOBAL VARIABLES
global ack

def ackCb(data):
    global ack
    print data
    if data:
        ack = True

if __name__=="__main__":
    global ack

    rospy.init_node('sim_planner')

    print msg

    ack = False

    rospy.Subscriber('/cps/command_reached', Bool, ackCb)

    print 'Path Planning started...'

    # Publish movement
    # @TODO write proper code here
    time.sleep(1)
    cmd = Point()
    cmd.x = 2.0
    cmd.y = 1.0
    cmd.z = 1.0
    CMD_PUB.publish(cmd)

    while not ack and not rospy.is_shutdown():
        time.sleep(1)

    print ''
    print 'Done!'
