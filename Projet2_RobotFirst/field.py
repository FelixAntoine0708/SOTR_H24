#!/usr/bin/python3

####### Import #######
import rospy
import geometry_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
from tqdm import tqdm 
from time import sleep as s
from os import system
import tty, sys, termios, select
from threading import Thread
from random import randint
import math


class field:
    def __init__(self):
        self.bluePoint = rospy.Publisher("/bluePoint", std_msgs.msg.Int64, queue_size=1)
        self.redPoint = rospy.Publisher("/redPoint", std_msgs.msg.Int64, queue_size=1)
        rospy.Subscriber("/robot_0/base_pose_ground_truth", nav_msgs.msg.Odometry, self.bluePosition)
        rospy.Subscriber("/robot_0/base_scan",sensor_msgs.msg.LaserScan, self.Bluelaser)
        rospy.Subscriber("/robot_1/base_pose_ground_truth", nav_msgs.msg.Odometry, self.redPosition)
        rospy.Subscriber("/robot_1/base_scan",sensor_msgs.msg.LaserScan, self.Redlaser)
        self.blueTeam = {
            "ballzone": False,
            "ball":0,
            "climbzone": False,
            "climbing": True,
            "stage":0,
            "shoot1ptszone":False, 
            "shoot2ptszone":False, 
            "laser":[0]
        }
        self.redTeam = {
            "ballzone": False,
            "ball":0,
            "climbzone": False,
            "climbing": True,
            "stage":0,
            "shoot1ptszone":False,
            "shoot2ptszone":False,
            "laser":[0]
        }

        
    def kbhit(self, settings):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    
    def progressbar(self, key):
        if key == 'z':
            for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.blueTeam['ball']}"):
                s(0.1)
        
        if key == 'b':
            for x in tqdm(range(10), colour="RED", desc= f"Red Teams balls {self.redTeam['ball']}"):
                s(0.1)

        if key == 'x':
            self.blueTeam['climbing'] = False
            for x in tqdm(range(35), colour="BLUE", desc= f"Blue Teams climbing"):
                s(0.1)
            climbingBresult = randint(1, 100)
            if climbingBresult > 1 and climbingBresult <=60:
                print("\n\rclimb succes for Blue team")
                rate = rospy.Rate(10)
                msg = 5
                self.bluePoint.publish(msg)
                rate.sleep()
                self.blueTeam['stage'] +=1

            else:
                print("\n\rclimb fail for Blue team")
            self.blueTeam['climbing'] = True
        
        if key == 'n':
            self.redTeam['climbing'] = False
            for x in tqdm(range(35), colour="RED", desc= f"Red Teams climbing"):
                s(0.1)
            climbingBresult = randint(1, 100)
            if climbingBresult > 1 and climbingBresult <=60:
                print("\n\rclimb succes for Red team")
                rate = rospy.Rate(10)
                msg = 5
                self.redPoint.publish(msg)
                rate.sleep()
                self.redTeam['stage'] +=1

            else:
                print("\n\rclimb fail for Red team")
            self.redTeam['climbing'] = True

        if key == 'c':
            if self.blueTeam['shoot1ptszone']:
                self.blueTeam['shoot1ptszone'] = False
                self.blueTeam['shoot2ptszone'] = False
                for x in tqdm(range(25), colour="BLUE", desc= f"Blue Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=90:
                    print("\n\rshoot succes for Blue team 1pts")
                    rate = rospy.Rate(10)
                    msg = 1
                    self.bluePoint.publish(msg)
                    rate.sleep()
                else:
                    print("\n\rshoot fail for Blue team")
                self.blueTeam['shoot1ptszone'] = True
                self.blueTeam['shoot2ptszone'] = True
            
            elif self.blueTeam['shoot2ptszone']:
                self.blueTeam['shoot1ptszone'] = False
                self.blueTeam['shoot2ptszone'] = False
                for x in tqdm(range(25), colour="BLUE", desc= f"Blue Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=80:
                    print("\n\rshoot succes for Blue team 2pts")
                    rate = rospy.Rate(10)
                    msg = 2
                    self.bluePoint.publish(msg)
                    rate.sleep()
                else:
                    print("\n\rshoot fail for Blue team")
                self.blueTeam['shoot1ptszone'] = True
                self.blueTeam['shoot2ptszone'] = True
            
        if key == 'm':
            if self.redTeam['shoot1ptszone']:
                self.redTeam['shoot1ptszone'] = False
                self.redTeam['shoot2ptszone'] = False
                for x in tqdm(range(25), colour="RED", desc= f"Red Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=90:
                    print("\n\rshoot succes for Red team 1pts")
                    rate = rospy.Rate(10)
                    msg = 1
                    self.redPoint.publish(msg)
                    rate.sleep()
                else:
                    print("\n\rshoot fail for Red team")
                self.redTeam['shoot1ptszone'] = True
                self.redTeam['shoot2ptszone'] = True
            
            elif self.redTeam['shoot2ptszone']:
                self.redTeam['shoot1ptszone'] = False
                self.redTeam['shoot2ptszone'] = False
                for x in tqdm(range(25), colour="RED", desc= f"Red Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=80:
                    print("\n\rshoot succes for Red team 2pts")
                    rate = rospy.Rate(10)
                    msg = 2
                    self.redPoint.publish(msg)
                    rate.sleep()
                else:
                    print("\n\rshoot fail for Red team")
                self.redTeam['shoot1ptszone'] = True
                self.redTeam['shoot2ptszone'] = True

    def Bluelaser(self, laser):
        self.blueTeam['laser'] = laser.ranges[80:100]

    def Redlaser(self, laser):
        self.redTeam['laser']= laser.ranges[80:100]

    def redPosition(self, pose):
        xRed = pose.pose.pose.position.x
        yRed = pose.pose.pose.position.y

        # calcul de side
        ypente = -2.5*xRed
        is_red_side = yRed >= ypente

        #calcul de cercle
        distance = math.sqrt(math.pow(xRed, 2) + math.pow(yRed, 2))

        if is_red_side:
            if distance <= 1.5:
                self.redTeam['shoot1ptszone'] = True
                self.redTeam['shoot2ptszone'] = False

            elif distance <= 2.5:
                self.redTeam['shoot1ptszone'] = False
                self.redTeam['shoot2ptszone'] = True

            else: 
                self.redTeam['shoot1ptszone'] = False
                self.redTeam['shoot2ptszone'] = False
        
        if yRed > 0:
            if xRed > 6 and yRed > 2:
                self.redTeam['ballzone'] = True
            else:
                self.redTeam['ballzone'] = False

        if yRed <= 0:
            if xRed > 5 and yRed < -1.20:
                self.redTeam['climbzone'] = True
            else: 
                self.redTeam['climbzone'] = False
    
    def bluePosition(self, pose):
        xBlue = pose.pose.pose.position.x
        yBlue = pose.pose.pose.position.y

        # calcul de side
        ypente = -2.5*xBlue
        is_blue_side = yBlue <= ypente

        #calcul de cercle
        distance = math.sqrt(math.pow(xBlue, 2) + math.pow(yBlue, 2))

        if is_blue_side:
            if distance <= 1.5:
                self.blueTeam['shoot1ptszone'] = True
                self.blueTeam['shoot2ptszone'] = False

            elif distance <= 2.5:
                self.blueTeam['shoot1ptszone'] = False
                self.blueTeam['shoot2ptszone'] = True
            
            else:
                self.blueTeam['shoot1ptszone'] = False
                self.blueTeam['shoot2ptszone'] = False


        if yBlue > 0:
            if xBlue < -4.60 and yBlue > 1.20:
                self.blueTeam['climbzone'] = True
            else:
                self.blueTeam['climbzone'] = False

        if yBlue <= 0:
            if xBlue <  -6 and yBlue < -2:
                self.blueTeam['ballzone'] = True
            else:
                self.blueTeam['ballzone'] = False

    def listener(self):
        while True:
            settings = termios.tcgetattr(sys.stdin)
            key = self.kbhit(settings) 

            if key == 'z' and self.blueTeam['ballzone']: 
                self.blueTeam['ball'] +=1
                if self.blueTeam['ball'] <= 2:
                    blueBallT= Thread(target=self.progressbar, args=(key, ))
                    blueBallT.start()
                else:
                    print("Blue are full")
                    self.blueTeam['ball'] = 2
            
            if key == 'b' and self.redTeam['ballzone']:
                self.redTeam['ball'] +=1
                if self.redTeam['ball'] <= 2:
                    redBallT = Thread(target=self.progressbar , args=(key, ))
                    redBallT.start()
                else:
                    print("Red are full")
                    self.redTeam['ball'] = 2

            if key == 'x' and self.blueTeam['climbzone']:
                if self.blueTeam['climbing'] and self.blueTeam['stage'] < 3:
                    blueClimbT = Thread(target=self.progressbar , args=(key, ))
                    blueClimbT.start()

            if key == 'n' and self.redTeam['climbzone']:
                if self.redTeam['climbing'] and self.redTeam['stage'] < 3:
                    redClimbT = Thread(target=self.progressbar , args=(key, ))
                    redClimbT.start()

            if key == 'c' and self.blueTeam['shoot1ptszone'] or key == 'c' and self.blueTeam['shoot2ptszone']:
                if self.blueTeam['ball'] >=1 and min(self.blueTeam['laser']) <=1.5:
                    self.blueTeam['ball'] -=1
                    blueShotT = Thread(target=self.progressbar, args=(key, ))
                    blueShotT.start()
                else: 
                    print("\n\rBlue Can't shoot")

            if key == 'm' and self.redTeam['shoot1ptszone'] or key == 'm' and self.redTeam['shoot2ptszone']:
                if self.redTeam['ball'] >=1 and min(self.redTeam['laser']) <=1.5:
                    self.redTeam['ball'] -=1
                    redshotT = Thread(target=self.progressbar, args=(key, ))
                    redshotT.start()
                else: 
                    print("\n\rRed Can't shoot")
                    

if __name__ == "__main__" : 
    cField = field()
    t1 = Thread(target=cField.listener)
    t1.start()
    rospy.init_node('first_field', anonymous=True)    # init du noed ROS
    try:
        while not rospy.is_shutdown():  
            s(2)
                
    except rospy.ROSInterruptException:
        pass
