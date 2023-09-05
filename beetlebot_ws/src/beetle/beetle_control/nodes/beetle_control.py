#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
import sys, select, os
import math
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

stepmove = 0.0005

smove = 0.0
emove = 0.0
wmove = 0.0
rmove = 0.0

xcord = 0.05
ycord = 0.05
zcord = 0.0

arm1 = 0.09
arm2 = 0.09

goalpath = 0.0


def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def change_joint_state():

    global smove
    global emove
    global wmove
    global rmove
    
    global xcord
    global ycord
    global zcord

    global arm1
    global arm2
    
    global goalpath
    
    rospy.init_node('joint_state_changer')
    pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
    rate = rospy.Rate(10)  # Publish at a rate of 10 Hz
    
    while not rospy.is_shutdown():
    
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['revolute_joint', 'shoulder_joint', 'elbow_joint', 'wrist_joint'] 
        
        key = getKey()
        
        if key == 'u' :
        
            xcord += stepmove
            
        elif key == 'j' :
        
            xcord -= stepmove
            
        elif key == 'i' :
        
            ycord += stepmove
            
        elif key == 'k' :
        
            ycord -= stepmove

        elif key == 'y' :
        
            zcord += stepmove
            
        elif key == 'h' :
        
            zcord -= stepmove            
        else:
            if (key == '\x03'):
                break
        
        goalpath = math.sqrt(xcord ** 2 + ycord ** 2 + zcord ** 2)
        
        print ('goalpath: ' + str(goalpath))
        print ('xcord: ' + str(xcord))
        print ('ycord: ' + str(ycord))
        print ('zcord: ' + str(zcord))
                
        if ycord == 0.0 :
            rmove = 0.0
        else:
            rmove = math.atan(xcord / ycord)
            
        smove = math.pi/2-(math.asin(zcord / goalpath) + math.acos((goalpath ** 2 + arm1 ** 2 - arm2 ** 2) / (2 * goalpath * arm1)))
        emove = math.pi-math.acos((arm1 ** 2 + arm2 ** 2 - goalpath ** 2) / (2 * arm1 * arm2))
        
        print ('smove: ' + str(smove))
        print ('emove: ' + str(emove))
        print ('rmove: ' + str(rmove))
        
        joint_state.position = [rmove, smove, emove, wmove]

        pub.publish(joint_state)
        rate.sleep()

if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
        
    try:
        change_joint_state()
    except rospy.ROSInterruptException:
        pass
    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

