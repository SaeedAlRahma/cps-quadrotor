#!/usr/bin/env python
import rospy, sys

from std_msgs.msg import Header
from geometry_msgs.msg import Pose, PoseStamped, Point
from hector_uav_msgs.srv import EnableMotors
from nav_msgs.msg import Odometry

import sys, select, time, datetime, math, random

CPS_DIR = "/home/saeed/cps_ws/src/cps_quadrotor/"

msg = """
Publishing to Pose!
---------------------------
Moving around:
  w:	 +y
  s:	 -y
  d:	 +x
  a:	 -x
  e:	 +z
  c:	 -z

anything else : go to origin

CTRL-C to quit
"""

# CONFIGURATIONS
WRITE_PERIOD = 5 # write 1 message every WRITE_PERIOD
DIST_THRESHOLD = 0.01 # threshold for distance from target
VEL_THRESHOLD = 0.001 # threshold for target velocity
NUM_MOVEMENTS = 10

# CONSTANTS
MOVE_BINDINGS = {
            		'w':(0,1,0,0),
            		's':(0,-1,0,0),
            		'd':(1,0,0,0),
            		'a':(-1,0,0,0),
            		'e':(0,0,1,0),
            		'c':(0,0,-1,0),
        	     }
WORLD_FRAME = rospy.get_param('world_frame', '/world')
POSE_PUB = rospy.Publisher('/command/pose', PoseStamped, queue_size = 1)
DIST_TRAVEL = 1

# GLOBAL VARIABLES
global position
global cmdPosition
global count_period
global dataFile
global isMoving
global count_pos


def dist(p1, p2):
    d =  math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
    return d

def speed(v):
    s = math.sqrt((v.x)**2 + (v.y)**2 + (v.z)**2)
    return s

def isTargetReached(pos, target, vel):
    if dist(pos,target) < DIST_THRESHOLD:
        if speed(vel) < VEL_THRESHOLD:
            return True
    return False

def stateCb(odo):
    global position
    global cmdPosition
    global count_period
    global dataFile
    global isMoving
    global count_pos

    position = odo.pose.pose.position

    if isMoving and not dataFile.closed:
        count_period += 1
        if not count_period%WRITE_PERIOD:
            twist = odo.twist.twist
            twistLinear = twist.linear
            odoTime = (odo.header.stamp.secs*1.0) + (odo.header.stamp.nsecs/1000000000.0)
            dataFile.write('%.2f %.2f %.2f %.2f %.2f %.2f %.2f\n'
                            % (odoTime,
                            position.x, position.y, position.z,
                            twistLinear.x, twistLinear.y, twistLinear.z))
            if isTargetReached(position, cmdPosition, twistLinear):
                dataFile.write('\n')
                print 'Reached target %d' % count_pos
                if count_pos < NUM_MOVEMENTS:
                    rad = 2*math.pi*random.random()
                    cmdPosition.x = position.x + (DIST_TRAVEL*math.cos(rad))
                    cmdPosition.y = position.y + (DIST_TRAVEL*math.sin(rad))
                    cmdPosition.z = position.z
                    publishPoseCommand()
                else:
                    isMoving = False
                count_pos += 1
                count_period = 0


def disableMotors():
    SERVICE_ENABLE_MOTORS = 'enable_motors'
    try:
        enable_motors = rospy.ServiceProxy(SERVICE_ENABLE_MOTORS, EnableMotors)
        res = enable_motors(False)
        if res:
            print "Motors disabled!"
        else:
            print "Failed to disable motors..."
    except rospy.ServiceException, e:
        print "Disable service", SERVICE_ENABLE_MOTORS, "call failed: %s"%e

def enableMotors():
    SERVICE_ENABLE_MOTORS = 'enable_motors'
    print "Waiting for service", SERVICE_ENABLE_MOTORS
    rospy.wait_for_service(SERVICE_ENABLE_MOTORS)
    try:
        enable_motors = rospy.ServiceProxy(SERVICE_ENABLE_MOTORS, EnableMotors)
        res = enable_motors(True)
        if res:
            print "Motors enabled!"
        else:
            print "Failed to enable motors..."
    except rospy.ServiceException, e:
        print "Enable service", SERVICE_ENABLE_MOTORS, "call failed: %s"%e

def vels(dist_travel):
	return "DIST_TRAVEL is %s" % (DIST_TRAVEL)

def publishPoseCommand(write=True):
    global position
    global cmdPosition
    global dataFile

    poseStamped = PoseStamped()
    poseStamped.pose = Pose()
    poseStamped.pose.position.x = cmdPosition.x
    poseStamped.pose.position.y = cmdPosition.y
    poseStamped.pose.position.z = cmdPosition.z
    poseStamped.pose.orientation.w = 1
    poseStamped.header = Header()
    poseStamped.header.frame_id = WORLD_FRAME
    now = rospy.Time.now()
    poseStamped.header.stamp = now

    POSE_PUB.publish(poseStamped)

    if write:
        # dataFile.write('xxxxx CURRENT POSITION xxxxx\n')
        dataFile.write('%d.%d\t%.2f\t%.2f\t%.2f\n'
                        % (now.secs,
                        now.nsecs/10000000,
                        position.x, position.y, position.z))
        # dataFile.write('----- POSITION COMMAND -----\n')
        dataFile.write('%d.%d\t%.2f\t%.2f\t%.2f\n'
                        % (now.secs,
                        now.nsecs/10000000,
                        cmdPosition.x, cmdPosition.y, cmdPosition.z))
    return poseStamped

if __name__=="__main__":
    global isMoving
    global count_period
    global count_pos
    global cmdPosition

    enableMotors()

    rospy.init_node('test_overshoot_random')

    isMoving = False
    count_period = 0
    count_pos = 1
    cmdPosition = Point()
    if len(sys.argv) > 1:
        DIST_TRAVEL = int(sys.argv[1])

    print msg
    print vels(DIST_TRAVEL)

    now = datetime.datetime.now()
    filename = "test_files/random%d_%d-%d-%d-%d-%d-%d.txt" %(DIST_TRAVEL, now.year, now.month, now.day, now.hour, now.minute, now.second)
    dataFile = open(CPS_DIR + filename,"w+")

    rospy.Subscriber('/ground_truth/state', Odometry, stateCb)

    # Start movement (Hover)
    time.sleep(1)
    cmdPosition.x = 0.0
    cmdPosition.y = 0.0
    cmdPosition.z = 1.0
    print "Launching..."
    publishPoseCommand(False)
    time.sleep(5) # wait for quadrotor to hover
    print 'Simulating...'
    rad = 2*math.pi*random.random()
    cmdPosition.x = position.x + (DIST_TRAVEL*math.cos(rad))
    cmdPosition.y = position.y + (DIST_TRAVEL*math.sin(rad))
    cmdPosition.z = position.z
    publishPoseCommand()
    isMoving = True

    try:
        while isMoving:
            time.sleep(1)
    except KeyboardInterrupt:
        print 'Done!'
    finally:
        dataFile.close()
        disableMotors()
