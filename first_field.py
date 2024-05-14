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
        rospy.Subscriber("/robot_0/base_pose_ground_truth", nav_msgs.msg.Odometry, self.bluePosition)
        rospy.Subscriber("/robot_0/base_scan",sensor_msgs.msg.LaserScan, self.Bluelaser)
        rospy.Subscriber("/robot_1/base_pose_ground_truth", nav_msgs.msg.Odometry, self.redPosition)
        rospy.Subscriber("/robot_1/base_scan",sensor_msgs.msg.LaserScan, self.Redlaser)
        self.ballsR = False
        self.ballsB = False
        self.climbRzone = False 
        self.climbBzone = False
        self.climbR = True
        self.climbB = True
        self.counterBlueBalls = 0
        self.counterRedBalls = 0
        self.bluePoints = 0
        self.redPoints = 0
        self.shootB1pts = False
        self.shootB2pts = False
        self.shootR1pts = False
        self.shootR2pts = False
        self.laserBlue = [0]
        self.laserRed = [0]
        

    def kbhit(self, settings):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    
    def progressbar(self, key):
        if key == 'z':
            for x in tqdm(range(10), colour="BLUE", desc= f"Blue Teams balls {self.counterBlueBalls}"):
                s(0.1)
        
        if key == 'b':
            for x in tqdm(range(10), colour="RED", desc= f"Red Teams balls {self.counterRedBalls}"):
                s(0.1)

        if key == 'x':
            self.climbB = False
            for x in tqdm(range(35), colour="BLUE", desc= f"Blue Teams climbing"):
                s(0.1)
            climbingBresult = randint(1, 100)
            if climbingBresult > 1 and climbingBresult <=60:
                print("\n\rclimb succes for Blue team")
                self.bluePoints +=5

            else:
                print("\n\rclimb fail for Blue team")
            self.climbB = True
        
        if key == 'n':
            self.climbR = False
            for x in tqdm(range(35), colour="RED", desc= f"Red Teams climbing"):
                s(0.1)
            climbingBresult = randint(1, 100)
            if climbingBresult > 1 and climbingBresult <=60:
                print("\n\rclimb succes for Red team")
                self.redPoints +=5
            else:
                print("\n\rclimb fail for Red team")
            self.climbR = True

        if key == 'c':
            if self.shootB1pts:
                self.shootB1pts = False
                self.shootB2pts = False
                for x in tqdm(range(25), colour="BLUE", desc= f"Blue Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=90:
                    print("\n\rshoot succes for Blue team 1pts")
                    self.bluePoints +=1
                else:
                    print("\n\rshoot fail for Blue team")
                self.shootB1pts = True
                self.shootB2pts = True
            
            elif self.shootB2pts:
                self.shootB1pts = False
                self.shootB2pts = False
                for x in tqdm(range(25), colour="BLUE", desc= f"Blue Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=80:
                    print("\n\rshoot succes for Blue team 2pts")
                    self.redPoints +=2
                else:
                    print("\n\rshoot fail for Blue team")
                self.shootB1pts = True
                self.shootB2pts = True
            
        if key == 'm':
            if self.shootR1pts:
                self.shootR1pts = False
                self.shootR2pts = False
                for x in tqdm(range(25), colour="RED", desc= f"Red Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=90:
                    print("\n\rshoot succes for Red team 1pts")
                    self.redPoints +=1
                else:
                    print("\n\rshoot fail for Red team")
                self.shootR1pts = True
                self.shootR2pts = True
            
            elif self.shootR2pts:
                self.shootR1pts = False
                self.shootR2pts = False
                for x in tqdm(range(25), colour="RED", desc= f"Red Teams shoot"):
                    s(0.1)
                shootresult = randint(1, 100)
                if shootresult > 1 and shootresult <=80:
                    print("\n\rshoot succes for Red team 2pts")
                    self.redPoints +=2
                else:
                    print("\n\rshoot fail for Red team")
                self.shootR1pts = True
                self.shootR2pts = True

    def Bluelaser(self, laser):
        self.laserBlue = laser.ranges[80:100]

    def Redlaser(self, laser):
        self.laserRed = laser.ranges[80:100]


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
                self.shootR1pts = True
                self.shootR2pts = False

            elif distance <= 2.5:
                self.shootR1pts = False
                self.shootR2pts = True

            else: 
                self.shootR1pts = False
                self.shootR2pts = False
        
        if yRed > 0:
            if xRed > 6 and yRed > 2:
                self.ballsR = True
            else:
                self.ballsR = False

        if yRed <= 0:
            if xRed > 5 and yRed < -1.20:
                self.climbRzone = True
            else: 
                self.climbRzone = False
    
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
                self.shootB1pts = True
                self.shootB2pts = False

            elif distance <= 2.5:
                self.shootB1pts = False
                self.shootB2pts = True
            
            else:
                self.shootB1pts = False
                self.shootB2pts = False


        if yBlue > 0:
            if xBlue < -4.60 and yBlue > 1.20:
                self.climbBzone = True
            else:
                self.climbBzone = False

        if yBlue <= 0:
            if xBlue <  -6 and yBlue < -2:
                self.ballsB = True
            else:
                self.ballsB = False

    def listener(self):
        while True:
            settings = termios.tcgetattr(sys.stdin)
            key = self.kbhit(settings) 

            if key == 'z' and self.ballsB: 
                self.counterBlueBalls +=1
                if self.counterBlueBalls <= 2:
                    blueBallT= Thread(target=self.progressbar, args=(key, ))
                    blueBallT.start()
                else:
                    print("Blue are full")
                    self.counterBlueBalls = 2
            
            if key == 'b' and self.ballsR:
                self.counterRedBalls +=1
                if self.counterRedBalls <= 2:
                    redBallT = Thread(target=self.progressbar , args=(key, ))
                    redBallT.start()
                else:
                    print("Red are full")
                    self.counterRedBalls = 2

            if key == 'x' and self.climbBzone:
                if self.bluePoints < 15 and self.climbB:
                    blueClimbT = Thread(target=self.progressbar , args=(key, ))
                    blueClimbT.start()

            if key == 'n' and self.climbRzone:
                if self.redPoints < 15 and self.climbR:
                    redClimbT = Thread(target=self.progressbar , args=(key, ))
                    redClimbT.start()

            if key == 'c' and self.shootB1pts or key == 'c' and self.shootB2pts:
                if self.counterBlueBalls >=1 and min(self.laserBlue) <=1.5:
                    self.counterBlueBalls -=1
                    blueShotT = Thread(target=self.progressbar, args=(key, ))
                    blueShotT.start()
                else: 
                    print("\n\rBlue Can't shoot")

            if key == 'm' and self.shootR1pts or key == 'm' and self.shootR2pts:
                if self.counterRedBalls >=1 and min(self.laserRed) <=1.5:
                    self.counterRedBalls -=1
                    blueShotT = Thread(target=self.progressbar, args=(key, ))
                    blueShotT.start()
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
