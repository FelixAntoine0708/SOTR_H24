#! /usr/bin/env python3

# library
import tty
import sys
import select
import termios
import rospy
from geometry_msgs.msg import Twist
import sensor_msgs.msg
import std_msgs.msg
from time import sleep as s
from random import randint as rand
import threading as th

speedMax = 0.5
turnSpeedMax = 0.25
laserData = [0]
lasSub = 0
bumpSub = 0
roomb = False
statue = False
contr = False
kami = False
safe = True
caution = False

# KBhit 
def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

# Laser
def laserCallback(data):
    global laserData
    laserData = data.ranges

def laserSub():
    global lasSub
    lasSub = rospy.Subscriber("/base_scan", sensor_msgs.msg.LaserScan,laserCallback)

def laserUnsub():
    global lasSub
    lasSub.unregister()

# Roomba command
def forwardRoomba():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = 2.0
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep()

def backwardRoomba():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = -2.0
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    while now + rospy.Duration.from_sec(2) >  rospy.Time.now():
        pub.publish(movecmd)
        rate.sleep()  

def leftRoomba():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.angular.z = 2.0
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    while now + rospy.Duration.from_sec(0.5) >  rospy.Time.now():
        pub.publish(movecmd)
        rate.sleep()

def rightRoomba():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.angular.z = -2.0
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    while now + rospy.Duration.from_sec(0.5) >  rospy.Time.now():
        pub.publish(movecmd)
        rate.sleep()

def bumperPub():
    global laserData

    bumpPub = rospy.Publisher('bumper',std_msgs.msg.Bool,queue_size=1)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if min(laserData) >= 0.4:
            msg = True
            bumpPub.publish(msg)
            rate.sleep()
        
        elif min(laserData) < 0.4:
            msg = False
            bumpPub.publish(msg)
            rate.sleep()

        s(0.2)

def bumperCallback(msg):
    if msg.data:
        if min(laserData) >= 0.4:
            forwardRoomba()

    else:
        if min(laserData) < 0.4:
            r = rand(1,2)
            backwardRoomba()
            if r == 1:
                leftRoomba()
            else:
                rightRoomba()

def bumperSub():
    global bumpSub
    bumpSub = rospy.Subscriber("/bumper", std_msgs.msg.Bool, bumperCallback)    

def bumperUnsub():
    global bumpSub
    bumpSub.unregister()

# Commande de base
"""
"""
def stop():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = 0
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep() 

"""
avance avec la touche 'w'
"""
def forward(speed):
    pub = rospy.Publisher("cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = speed
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep()

"""
recule avec la touche 's'
"""
def backward(speed):
    pub = rospy.Publisher("cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = -speed
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep()

"""
Tourne a gaucheavec la touche 'a'
"""
def left():
    pub = rospy.Publisher("cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = turnSpeedMax
    movecmd.angular.z = turnSpeedMax
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep()

"""
Tourne a droite avec la touche 'd'
"""
def right():
    pub = rospy.Publisher("cmd_vel", Twist, queue_size= 1)
    movecmd = Twist()
    movecmd.linear.x = turnSpeedMax
    movecmd.angular.z = -turnSpeedMax
    now = rospy.Time.now()
    rate = rospy.Rate(10)
    pub.publish(movecmd)
    rate.sleep()

"""
Les controles manuel. il rentre dans aucun murs 
"""
def control():
    global laserData
    global speedMax
    global safe
    global caution 
    slowmo = 0.01

    settings = termios.tcgetattr(sys.stdin)
    key = getKey(settings)
    
    if safe:
        if min(laserData) >= 1.5:
            speedMax = 0.5
            if key == 'w':
                forward(speedMax)
                        
            elif key == 'a':
                left()
                        
            elif key == 's':
                backward(speedMax)
                        
            elif key == 'd':
                right()

        elif min(laserData) < 0.4:
            if key == 's':
                speedMax += slowmo
                backward(speedMax) 
            else:
                stop()

        elif min(laserData) >= 0.4: 
            if min(laserData) <= 1.5:
                if speedMax > 0:
                    if key == 'w':
                        speedMax -= slowmo
                        forward(speedMax)
                            
                    elif key == 'a':
                        left()
                                    
                    elif key == 's':
                        speedMax += slowmo
                        backward(speedMax)
                                    
                    elif key == 'd':
                        right() 

    if caution:
        if min(laserData) >= 1:
            speedMax = 0.5
            if key == 'w':
                forward(speedMax)
                        
            elif key == 'a':
                left()
                        
            elif key == 's':
                backward(speedMax)
                        
            elif key == 'd':
                right()

        elif min(laserData) < 0.4:
            if key == 's':
                speedMax += slowmo
                backward(speedMax) 
            else:
                stop()

        elif min(laserData) >= 0.4: 
            if min(laserData) <= 1:
                if speedMax > 0:
                    if key == 'w':
                        speedMax -= slowmo
                        forward(speedMax)
                            
                    elif key == 'a':
                        left()
                                    
                    elif key == 's':
                        speedMax += slowmo
                        backward(speedMax)
                                    
                    elif key == 'd':
                        right()

    s(0.02)

"""
Les controles de mon Kamikaze. Il rentre dans les murs 
"""
def controlKami():
    speedMax = 0.5
    settings = termios.tcgetattr(sys.stdin)
    key = getKey(settings)
    if key == 'w':
        forward(speedMax)

    elif key == 'a':
        left()

    elif key == 's':
        backward(speedMax)

    elif key == 'd':
        right()

# lecteur des touches 
"""
Lis les touches pour savoir quel modes il doit faire
"""
def listenter():
    global roomb
    global statue
    global contr
    global kami
    global safe
    global caution

    settings = termios.tcgetattr(sys.stdin)
    key = getKey(settings)

    if key == '1':
        statue = True
        roomb = False
        contr = False
        kami = False
        laserUnsub()
        bumperUnsub()
                
    elif key == '2':
        roomb = True
        statue = False
        contr = False
        kami = False
        laserSub()
        bumperSub()
                
    elif key == '3':
        contr = True
        statue = False
        roomb = False
        kami = False
        laserSub()
        bumperUnsub()

    elif key == '4':
        kami = True
        statue = False
        roomb = False
        contr = False
        laserUnsub()
        bumperUnsub()

    elif key == '7':
        safe = True
        caution = False

    elif key == '8':
        caution = True
        safe = False

    if statue:
        stop()

    if contr: 
        control()

    if kami:
        controlKami()

    s(0.1)


# MAIN
if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin) # init du key 
    rospy.init_node('custom_teleopkeyLabo4', anonymous=True)    # init du noed ROS

    t1 = th.Thread(target=bumperPub, args=())   #init le thread du publisher du bumper
    t1.start()  # debut du thread

    laserSub()  # subscribe sur le laser
    bumperSub() # subscribe sur le bumper
    try:
        while not rospy.is_shutdown():  
            listenter() # lis les touche et effectue les tache
                
    except rospy.ROSInterruptException:
        pass