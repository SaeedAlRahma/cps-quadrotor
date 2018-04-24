#!/usr/bin/env python
import rospy, sys, select, time, datetime, math, random

from std_msgs.msg import Header, Bool
from geometry_msgs.msg import Pose, PoseStamped, Point
from hector_uav_msgs.srv import EnableMotors
from nav_msgs.msg import Odometry

CPS_DIR = "/home/saeed/cps_ws/src/cps_quadrotor/"

msg = """
Publishing commands to Pose!
---------------------------
Listening to /cps/path_planner for commands
Publishing acknowledgements to /cps/command_reached

CTRL-C to quit
"""

# CONFIGURATIONS
DIST_THRESHOLD = 0.01 # threshold for distance from target
VEL_THRESHOLD = 0.001 # threshold for target velocity
WRITE_PERIOD = 5 # write 1 message every WRITE_PERIOD

# CONSTANTS
HOVER_HEIGHT = 1.0
WORLD_FRAME = rospy.get_param('world_frame', '/world')
POSE_PUB = rospy.Publisher('/command/pose', PoseStamped, queue_size = 1)
ACK_PUB = rospy.Publisher('/cps/command_reached', Bool, queue_size = 1)

# GLOBAL VARIABLES
global position
global cmdPosition
global count_period
global dataFile
global isMoving


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

    position = odo.pose.pose.position

    if isMoving and not dataFile.closed:
        count_period += 1
        if not count_period%WRITE_PERIOD:
            twist = odo.twist.twist
            twistLinear = twist.linear
            dataFile.write('%d.%d %.2f %.2f %.2f %.2f %.2f %.2f\n'
                            % (odo.header.stamp.secs, odo.header.stamp.nsecs/10000000,
                            position.x, position.y, position.z,
                            twistLinear.x, twistLinear.y, twistLinear.z))
            if isTargetReached(position, cmdPosition, twistLinear):
                dataFile.write('\n')
                print 'Reached target'
                print position
                ACK_PUB.publish(True)
                isMoving = False

def commandCb(pos):
    global cmdPosition
    global count_period
    global isMoving

    cmdPosition.x = pos.x
    cmdPosition.y = pos.y
    cmdPosition.z = pos.z
    publishPoseCommand()
    count_period = 0
    isMoving = True


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
    global cmdPosition

    enableMotors()

    rospy.init_node('sim_controller')

    isMoving = False
    count_period = 0
    cmdPosition = Point()
    prefix = ''
    if len(sys.argv) > 1:
        prefix = sys.argv[1] + '_'

    print msg

    now = datetime.datetime.now()
    filename = "sim_files/%s%d-%d-%d-%d-%d-%d.txt" %(prefix, now.year, now.month, now.day, now.hour, now.minute, now.second)
    dataFile = open(CPS_DIR + filename,"w+")

    rospy.Subscriber('/ground_truth/state', Odometry, stateCb)

    # Start movement (Hover)
    time.sleep(1)
    cmdPosition.x = 0.0
    cmdPosition.y = 0.0
    cmdPosition.z = HOVER_HEIGHT
    print "Launching..."
    publishPoseCommand(False)
    time.sleep(5) # wait for quadrotor to hover
    print 'Simulating...'
    rospy.Subscriber('/cps/path_planner', Point, commandCb)

    while not rospy.is_shutdown():
        time.sleep(1)

    print ''
    print 'Terminated!'
    dataFile.close()
    disableMotors()
