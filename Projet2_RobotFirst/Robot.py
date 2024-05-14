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

        # ROS publishers and subscribers
        self.move_robot_0 = rospy.Publisher('robot_0/cmd_vel', Twist, queue_size=1)
        self.move_robot_1 = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=1)
        
        rospy.Subscriber('robot_0/base_scan', LaserScan, self.rangeData0)
        rospy.Subscriber('robot_1/base_scan', LaserScan, self.rangeData1)
    
    def rangeData0(self, data):

        distance = data.ranges[20:160]

        if min(distance) < DISTANCE_MUR:
            self.murDevant_0 = True
                
        else:
            self.murDevant_0 = False     
                
    def rangeData1(self, data):
        
        distance = data.ranges[20:160]

        if min(distance) < DISTANCE_MUR:
            self.murDevant_1 = True
                
        else:
            self.murDevant_1 = False     
                
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
        
    def commande_robot_0_1(self):
        
        twist_0 = Twist()
        twist_1 = Twist()
        
        try:
            
            while not rospy.is_shutdown():
                
                    keys = pygame.event.get()
                    keys = pygame.key.get_pressed()  
                                    
                    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
                        
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

                    else:
                        mouvement.publishMove(ZERO,ZERO,twist_0,self.move_robot_0)

                        
                    if keys[pygame.K_i] or keys[pygame.K_k] or keys[pygame.K_j] or keys[pygame.K_l]:
                        
                        if keys[pygame.K_i]:
                            if(self.murDevant_1 == True):
                                mouvement.publishMove(ZERO,ZERO,twist_1,self.move_robot_1)
                            else:
                                mouvement.publishMove(VITESSE_LINEAIRE,ZERO,twist_1,self.move_robot_1)

                        elif keys[pygame.K_k]:
                            mouvement.publishMove(-VITESSE_LINEAIRE,ZERO,twist_1,self.move_robot_1)

                        elif keys[pygame.K_j]:
                            mouvement.publishMove(ZERO,VITESSE_ANGULAIRE,twist_1,self.move_robot_1)

                        elif keys[pygame.K_l]:
                            mouvement.publishMove(ZERO,-VITESSE_ANGULAIRE,twist_1,self.move_robot_1)

                    else:
                        mouvement.publishMove(ZERO,ZERO,twist_1,self.move_robot_1)

        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    
    try:
        
        rospy.init_node('Robot')
        
        move = mouvement()
        move.commande_robot_0_1()
        
    except rospy.ROSInterruptException:
        pass