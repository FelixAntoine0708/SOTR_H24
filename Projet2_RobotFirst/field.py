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
import Robot
 
 
class field:
    def __init__(self):
        self.bluePoint = rospy.Publisher("/robot_0/Point", std_msgs.msg.Int64, queue_size=1)
        self.blueBallGive = rospy.Publisher("/robot_0/ballon_recu", std_msgs.msg.Bool, queue_size=1)
        self.blueclimb = rospy.Publisher("/robot_0/climb_recu", std_msgs.msg.Int8, queue_size=1)
        self.blueshot = rospy.Publisher("/robot_0/shoot_recu", std_msgs.msg.Bool, queue_size=1)
 
        self.redPoint = rospy.Publisher("/robot_1/Point", std_msgs.msg.Int64, queue_size=1)
        self.redBallGive = rospy.Publisher("/robot_1/ballon_recu", std_msgs.msg.Bool, queue_size=1)
        self.redclimb = rospy.Publisher("/robot_1/climb_recu", std_msgs.msg.Int8, queue_size=1)
        self.redshot = rospy.Publisher("/robot_1/shoot_recu", std_msgs.msg.Bool, queue_size=1)
        
        rospy.Subscriber("/robot_0/base_pose_ground_truth", nav_msgs.msg.Odometry, self.bluePosition)
        rospy.Subscriber("/robot_0/base_scan",sensor_msgs.msg.LaserScan, self.Bluelaser)
        rospy.Subscriber("/robot_0/requete_ballon", std_msgs.msg.Bool, self.requestAnswerBlueBall)
        rospy.Subscriber("/robot_0/requete_climb", std_msgs.msg.Bool, self.requestBlueClimb)
        rospy.Subscriber("/robot_0/requete_shoot", std_msgs.msg.String, self.requestBlueShoot)
        
 
        rospy.Subscriber("/robot_1/base_pose_ground_truth", nav_msgs.msg.Odometry, self.redPosition)
        rospy.Subscriber("/robot_1/base_scan",sensor_msgs.msg.LaserScan, self.Redlaser)
        rospy.Subscriber("/robot_1/requete_ballon", std_msgs.msg.Bool, self.requestAnswerRedBall)
        rospy.Subscriber("/robot_1/requete_climb", std_msgs.msg.Bool, self.requestRedClimb)
        rospy.Subscriber("/robot_1/requete_shoot", std_msgs.msg.String, self.requestRedShoot)
 
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
 
    def requestAnswerBlueBall(self, ballrobot_0):
        self.blueTeam['ballzone'] = ballrobot_0.data
        if self.blueTeam['ballzone']:
            if self.blueTeam['ball'] < 2:
                self.blueTeam['ballzone'] = False
                self.blueTeam['ball']+=1
                for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.blueTeam['ball']}"):
                    s(0.1)
                self.blueTeam['ballzone'] = True
                msg = True
                rate = rospy.Rate(10)    
                self.blueBallGive.publish(msg)
                rate.sleep()
 
    def requestAnswerRedBall(self, ballrobot_1):
        self.redTeam['ballzone'] = ballrobot_1.data
        if self.redTeam['ballzone']:
            if self.redTeam['ball'] < 2:
                self.redTeam['ballzone'] = False
                self.redTeam['ball']+=1
                for x in tqdm(range(10), colour="BLUE", desc= f"Red Teams balls {self.redTeam['ball']}"):
                    s(0.1)
                self.redTeam['ballzone'] = True
                msg = True
                rate = rospy.Rate(10)    
                self.redBallGive.publish(msg)
                rate.sleep()
 
    def requestBlueClimb(self, climbrobot_0):
        if climbrobot_0.data:
                if self.blueTeam['climbing'] and self.blueTeam['stage'] < 3:
                    for x in tqdm(range(35), colour="BLUE", desc= f"Blue Teams balls {self.blueTeam['ball']}"):
                        s(0.1)
                    
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Blue")
                        msg = 1
                        rate = rospy.Rate(10)    
                        self.blueclimb.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Blue")
                        msg = 2
                        rate = rospy.Rate(10)    
                        self.blueclimb.publish(msg)
                        rate.sleep()
 
    def requestRedClimb(self, climbrobot_1):
        if climbrobot_1 and self.redTeam['climbzone']:
                if self.redTeam['climbing'] and self.redTeam['stage'] < 3:
                    for x in tqdm(range(35), colour="BLUE", desc= f"Blue Teams balls {self.redTeam['ball']}"):
                        s(0.1)
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Red")
                        msg = 1
                        rate = rospy.Rate(10)    
                        self.redclimb.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Red")
                        msg = 2
                        rate = rospy.Rate(10)    
                        self.redclimb.publish(msg)
                        rate.sleep()
                    
    def requestBlueShoot(self, shootrobot_0):
        if shootrobot_0 == 1:
                if self.blueTeam['ball'] >=1 and min(self.blueTeam['laser']) <=1.5:
                    self.blueTeam['ball'] -=1
                    for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.blueTeam['ball']}"):
                        s(0.1)
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Blue")
                        msg = True
                        rate = rospy.Rate(10)    
                        self.blueshot.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Blue")
                        msg = False
                        rate = rospy.Rate(10)    
                        self.blueshot.publish(msg)
                        rate.sleep()
 
        if shootrobot_0 == 2:
                if self.blueTeam['ball'] >=1 and min(self.blueTeam['laser']) <=1.5:
                    self.blueTeam['ball'] -=1
                    for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.blueTeam['ball']}"):
                        s(0.1)
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Blue")
                        msg = True
                        rate = rospy.Rate(10)    
                        self.blueshot.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Blue")
                        msg = False
                        rate = rospy.Rate(10)    
                        self.blueshot.publish(msg)
                        rate.sleep()
                    
    def requestRedShoot(self, shootrobot_1):
        if shootrobot_1 == 1:
                if self.redTeam['ball'] >=1 and min(self.redTeam['laser']) <=1.5:
                    self.redTeam['ball'] -=1
                    for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.redTeam['ball']}"):
                        s(0.1)
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Blue")
                        msg = True
                        rate = rospy.Rate(10)    
                        self.redshot.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Blue")
                        msg = False
                        rate = rospy.Rate(10)    
                        self.redshot.publish(msg)
                        rate.sleep()
 
        if shootrobot_1 == 2:
                if self.redTeam['ball'] >=1 and min(self.redTeam['laser']) <=1.5:
                    self.redTeam['ball'] -=1
                    for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.redTeam['ball']}"):
                        s(0.1)
                    climb = randint(1, 100)
                    if climb <=60:
                        print("Success climb Blue")
                        msg = True
                        rate = rospy.Rate(10)    
                        self.redshot.publish(msg)
                        rate.sleep()
                    else:
                        print("Failed climb Blue")
                        msg = False
                        rate = rospy.Rate(10)    
                        self.redshot.publish(msg)
                        rate.sleep()
 
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
 
                    
if __name__ == "__main__" :
    cfield = field()
    rospy.init_node('field', anonymous=True)    # init du noed ROS
    try:
        while not rospy.is_shutdown():  
            s(2)
                
    except rospy.ROSInterruptException:
        pass