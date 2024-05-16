#!/usr/bin/env python3
"""
Carl-Dominic Aubin
Projet 2 - robot first
Script pour controler le robot
"""
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
import pygame
from threading import Thread
from random import randint
import math
import nav_msgs.msg
from tqdm import tqdm 
from time import sleep


DISTANCE_MUR = 0.3
VITESSE_LINEAIRE = 1.0
VITESSE_ANGULAIRE = 0.5
ZERO = 0

class mouvement:
    def __init__(self):
        
        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        
        # Robot state attributes
        self.murDevant_0 = False
        self.murDevant_1 = False
        self.balls_1 = False
        self.balls_1 = False
        
        # ROS publishers and subscribers
        self.move_robot_0 = rospy.Publisher('robot_0/cmd_vel', Twist, queue_size=1)
        self.move_robot_1 = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=1)
        
        rospy.Subscriber("robot_1/base_pose_ground_truth", nav_msgs.msg.Odometry, self.redPosition_1)
        rospy.Subscriber("robot_0/base_pose_ground_truth", nav_msgs.msg.Odometry, self.bluePosition_0)

        #self.requete_ballon_0 = rospy.Subscriber("robot_0/base_ballon", bool, self.lanceBallon_0)
        #self.requete_ballon_1 = rospy.Subscriber("robot_1/base_ballon", bool, self.lanceBallon_1)

        #rospy.Subscriber("robot_0/base_escalader", bool, queue_size=1)
        #rospy.Subscriber("robot_1/base_escalader", bool, queue_size=1)

        self.requete_ballon_0 = rospy.Publisher('robot_0/requete_ballon', Bool, queue_size=1)
        self.requete_ballon_1 = rospy.Publisher('robot_1/requete_ballon', Bool, queue_size=1)

        rospy.Subscriber('robot_0/base_scan', LaserScan, self.rangeDataB_0)
        rospy.Subscriber('robot_1/base_scan', LaserScan, self.rangeDataR_1)
    
    def rangeDataB_0(self, data):

        distance = data.ranges[20:160]

        if min(distance) < DISTANCE_MUR:
            self.murDevant_0 = True
                
        else:
            self.murDevant_0 = False     
                
    def rangeDataR_1(self, data):
        
        distance = data.ranges[20:160]

        if min(distance) < DISTANCE_MUR:
            self.murDevant_1 = True
                
        else:
            self.murDevant_1 = False     
                    
    def redPosition_1(self, pose):
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
                self.balls_1 = True
            else:
                self.balls_1 = False

        if yRed <= 0:
            if xRed > 5 and yRed < -1.20:
                self.climbRzone = True
            else: 
                self.climbRzone = False
    
    def bluePosition_0(self, pose):
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
                self.balls_1 = True
            else:
                self.balls_1 = False
            
    def chargeBallon_0(self):
        if (self.balls_1 == True):
            mouvement.unsuscribeMove_0(self)
            self.bloqueRobot_0 = True
            rate = rospy.Rate(10)    
            self.requete_ballon_0.publish(self.bloqueRobot_0)
            rate.sleep()
            print("Demande de ballon en cours")
        else:
            print("Vous n'êtes pas dans votre zone respective pour cette commande")
            
    def chargeBallon_1(self):
        if (self.balls_1 == True):
            mouvement.unsuscribeMove_1(self)
            self.bloqueRobot_1 = True
            rate = rospy.Rate(10)   
            self.requete_ballon_1.publish(self.balls_1)
            rate.sleep()
            print("Demande de ballon en cours")
        else:
            print("Vous n'êtes pas dans votre zone respective pour cette commande")
        
    def unsuscribeMove_0(self):
        
        try:
            self.move_robot_0.unregister()

        except Exception as e:
            print(e)
            
    def unsuscribeMove_1(self):
        
        try:
            self.move_robot_1.unregister()

        except Exception as e:
            print(e)
        
    def publishMove(line,angu,twis,robo):
        
        twis.linear.x = line
        twis.angular.z = angu
        robo.publish(twis)
        
    def mouvement_robot_0_1(self):
        
        twist_0 = Twist()
        twist_1 = Twist()
        
        try:
            
            while not rospy.is_shutdown():
                
                try:
                
                    keys = pygame.event.get()
                    keys = pygame.key.get_pressed()  
                                    
                    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_z] or keys[pygame.K_x] or keys[pygame.K_c]:
                        
                        if keys[pygame.K_w]:
                            if(self.murDevant_0 == True):
                                mouvement.publishMove(ZERO,ZERO,twist_0,self.move_robot_0)
                            else:
                                mouvement.publishMove(VITESSE_ANGULAIRE,ZERO,twist_0,self.move_robot_0)
                            
                        if keys[pygame.K_s]:
                            mouvement.publishMove(-VITESSE_ANGULAIRE,ZERO,twist_0,self.move_robot_0)
                        
                        if keys[pygame.K_a]:
                            mouvement.publishMove(ZERO,VITESSE_ANGULAIRE,twist_0,self.move_robot_0)
                        
                        if keys[pygame.K_d]:
                            mouvement.publishMove(ZERO,-VITESSE_ANGULAIRE,twist_0,self.move_robot_0)

                        if keys[pygame.K_z]:
                            mouvement.chargeBallon_0(self)
                                    
                    else:
                        mouvement.publishMove(ZERO,ZERO,twist_0,self.move_robot_0)

                        
                    if keys[pygame.K_i] or keys[pygame.K_k] or keys[pygame.K_j] or keys[pygame.K_l] or keys[pygame.K_b] or keys[pygame.K_n] or keys[pygame.K_m]:

                        if keys[pygame.K_i]:
                            if(self.murDevant_1 == True):
                                mouvement.publishMove(ZERO,ZERO,twist_1,self.move_robot_1)
                            else:
                                mouvement.publishMove(VITESSE_LINEAIRE,ZERO,twist_1,self.move_robot_1)

                        if keys[pygame.K_k]:
                            mouvement.publishMove(-VITESSE_LINEAIRE,ZERO,twist_1,self.move_robot_1)

                        if keys[pygame.K_j]:
                            mouvement.publishMove(ZERO,VITESSE_ANGULAIRE,twist_1,self.move_robot_1)

                        if keys[pygame.K_l]:
                            mouvement.publishMove(ZERO,-VITESSE_ANGULAIRE,twist_1,self.move_robot_1)
                        
                        if keys[pygame.K_b] and self.bloqueRobot_1: #Charger un ballon
                            mouvement.chargeBallon_1(self)
                            
                        if keys[pygame.K_x]: #Lancer un ballon
                            None
                        
                    else:
                        mouvement.publishMove(ZERO,ZERO,twist_1,self.move_robot_1)
                
                except Exception as e:
                        print(e)
                
        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    
    try:
        
        rospy.init_node('Robot')
        
        move = mouvement()
        move.mouvement_robot_0_1()
        
    except rospy.ROSInterruptException:
        pass