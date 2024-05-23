#!/usr/bin/env python3
"""
Carl-Dominic Aubin
Projet 2 - robot first
Script pour controler le robot
"""
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from std_msgs.msg import Int8
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
        self.ballZone_0 = False
        self.ballZone_1 = False
        self.ballget_0 = 0
        self.ballget_1 = 0
        self.stade_0 = 0
        self.stade_1 = 0
        self.requeteLancer_0 = False
        self.requeteLancer_1 = False
        self.requeteBallon_1 = False
        self.requeteBallon_0 = False

        # ROS publishers and subscribers
        self.move_robot_0 = rospy.Publisher('robot_0/cmd_vel', Twist, queue_size=1)
        self.move_robot_1 = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=1)

        self.requete_ballon_0 = rospy.Publisher('robot_0/requete_ballon', Bool, queue_size=1)
        self.requete_ballon_1 = rospy.Publisher('robot_1/requete_ballon', Bool, queue_size=1)
        
        self.requete_grimper_0 = rospy.Publisher('robot_0/requete_climb', Bool, queue_size=1)
        self.requete_grimper_1 = rospy.Publisher('robot_1/requete_climb', Bool, queue_size=1)
        
        self.requete_lancer_0 = rospy.Publisher('robot_0/requete_shoot', Bool, queue_size=1)
        self.requete_lancer_1 = rospy.Publisher('robot_1/requete_shoot', Bool, queue_size=1)
        
        rospy.Subscriber('robot_0/base_scan', LaserScan, self.rangeDataB_0)
        rospy.Subscriber('robot_1/base_scan', LaserScan, self.rangeDataR_1)
        
        rospy.Subscriber('robot_0/ballon_recu', Bool, self.ballRecu_0)
        rospy.Subscriber('robot_1/ballon_recu', Bool, self.ballRecu_1)
        
        rospy.Subscriber('robot_0/climb_recu', Bool, self.climbRecu_0)
        rospy.Subscriber('robot_1/climb_recu', Bool, self.climbRecu_1)
        
        rospy.Subscriber('robot_0/shoot_recu', Bool, self.tireRecu_0)
        rospy.Subscriber('robot_1/shoot_recu', Bool, self.tireRecu_1)
        
        rospy.Subscriber("robot_1/base_pose_ground_truth", nav_msgs.msg.Odometry, self.redPosition_1)
        rospy.Subscriber("robot_0/base_pose_ground_truth", nav_msgs.msg.Odometry, self.bluePosition_0)

        
    def tireRecu_0(self,tire_0):
        self.reponseTire_0 = tire_0.data
        if(self.reponseTire_0 == True): #2points vrai
            self.requeteLancer_0 = False
            self.reponseTire_0 = False
            print("compte !!!")
        else:
            self.requeteLancer_0 = False
            print("manque completement !!!")
    
    def tireRecu_1(self,tire_1):
        self.reponseTire_1 = tire_1.data
        if(self.reponseTire_1 == True): #2points vrai
            self.requeteLancer_1 = False
            self.reponseTire_1 = False
            print("compte !!!")
        else:
            self.requeteLancer_1 = False
            print("manque completement !!!")
      
    def ballRecu_0(self, ball_0):
        self.reponseBall_0 = ball_0.data
        if self.reponseBall_0 == True:
            self.requeteBallon_0 = False
            self.reponseBall_0 = False
            print("Ballon obtenu blue")
            self.ballget_0+=1
            mouvement.suscribeMove_0(self)
        
    def ballRecu_1(self, ball_1):
        self.reponseBall_1 = ball_1.data
        if self.reponseBall_1 == True:
            self.requeteBallon_1 = False
            self.reponseBall_1 = False
            print("Ballon obtenu blue")
            self.ballget_1+=1
            mouvement.suscribeMove_0(self)
    
    def climbRecu_0(self, climb_0):
        self.reponseClimb_0 = climb_0.data
        if self.reponseClimb_0:
            self.requeteGrimper_0 = False
            self.reponseClimb_0 = 0
            self.stade_0 += 1
            print("Vous prenez de la hauteur")

        else:
            self.requeteGrimper_0 = False
            self.reponseClimb_0 = 0
            print("Vous ne montez pas")
    
    def climbRecu_1(self, climb_1):
        self.reponseClimb_1 = climb_1.data
        if self.reponseClimb_1:
            self.requeteGrimper_1 = False
            self.reponseClimb_1 = 0
            self.stade_1 += 1
            print("Vous prenez de la hauteur")

        else:
            self.requeteGrimper_1 = False
            self.reponseClimb_1 = 0
            print("Vous ne montez pas")
    
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
            if distance <= 2.5:
                self.shootR2pts = True

            else: 
                self.shootR2pts = False
        
        if yRed > 0:
            if xRed > 6 and yRed > 2:
                self.ballZone_1 = True
            else:
                self.ballZone_1 = False

        if yRed <= 0:
            if xRed > 5 and yRed < -1.20:
                self.climbRzone_1 = True
            else: 
                self.climbRzone_1 = False
    
    def bluePosition_0(self, pose):
        xBlue = pose.pose.pose.position.x
        yBlue = pose.pose.pose.position.y

        # calcul de side
        ypente = -2.5*xBlue
        is_blue_side = yBlue <= ypente

        #calcul de cercle
        distance = math.sqrt(math.pow(xBlue, 2) + math.pow(yBlue, 2))

        if is_blue_side:
            if distance <= 2.5:
                self.shootB2pts = True
            
            else:
                self.shootB2pts = False

        if yBlue > 0:
            if xBlue < -4.60 and yBlue > 1.20:
                self.climbBzone_0 = True
            else:
                self.climbBzone_0 = False

        if yBlue <= 0:
            if xBlue <  -6 and yBlue < -2:
                self.ballZone_0 = True
            else:
                self.ballZone_0 = False
            
    def chargeBallon_0(self):
        if (self.ballZone_0 == True) and (self.requeteBallon_0 == False):
            mouvement.unsuscribeMove_0(self)
            rate = rospy.Rate(10)    
            self.requeteBallon_0 = True
            self.requete_ballon_0.publish(self.requeteBallon_0)
            rate.sleep()
            print("Demande de ballon en cours")

    def chargeBallon_1(self):
        if (self.ballZone_1 == True) and (self.requeteBallon_1 == False):
            mouvement.unsuscribeMove_1(self)
            rate = rospy.Rate(10)   
            self.requeteBallon_1 = True
            self.requete_ballon_1.publish(self.requeteBallon_1)
            rate.sleep()
            print("Demande de ballon en cours")
            
    def grimperRobot_1(self):
        if(self.climbRzone_1 == True) and (self.requeteGrimper_1 == False):
            mouvement.unsuscribeMove_1(self)
            rate = rospy.Rate(10)   
            self.requeteGrimper_1 = True
            self.requete_grimper_1.publish(self.requeteGrimper_1)
            rate.sleep()
            if self.stade_0< 3:
                print("Demande pour grimper en cours")
            
    def grimperRobot_0(self):
        if(self.climbBzone_0 == True) and (self.requeteGrimper_0 == False):
            mouvement.unsuscribeMove_0(self)
            rate = rospy.Rate(10)   
            self.requeteGrimper_0 = True
            self.requete_grimper_0.publish(self.requeteGrimper_0)
            rate.sleep()
            if self.stade_0< 3:
                print("Demande pour grimper en cours")
        
    def lancerBallon_0(self):
        if self.shootB2pts and self.requeteLancer_0 == False:
            rate = rospy.Rate(10)   
            self.requeteLancer_0 = True
            self.requete_lancer_0.publish(self.requeteLancer_0)
            rate.sleep()
            print("Il lance et ...")
                
    def lancerBallon_1(self):
        if self.shootR2pts and self.requeteLancer_1 == False:  
            rate = rospy.Rate(10)   
            self.requeteLancer_1 = True
            self.requete_lancer_1.publish(self.requeteLancer_1)
            rate.sleep()
            print("Il lance et ...")
        
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
            
    def suscribeMove_0(self):
        self.move_robot_0 = rospy.Publisher('robot_0/cmd_vel', Twist, queue_size=1)
        
    def suscribeMove_1(self):
        self.move_robot_1 = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=1)

    def publishMove(line,angu,twis,robo):
        twis.linear.x = line
        twis.angular.z = angu
        robo.publish(twis)
        
    def mouvement_robot_0_1(self):
        twist_0 = Twist()
        twist_1 = Twist()
        
        self.requeteBallon_0 = False
        self.requeteBallon_1 = False
        
        self.requeteGrimper_0 = False
        self.requeteGrimper_1 = False
        
        self.reponseBall_0 = False
        self.reponseBall_1 = False
        
        self.reponseClimb_0 = 0
        self.reponseClimb_1 = 0
        
        self.reponseTire_0 = False
        self.reponseTire_1 = False

        ball_1 = 0

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
                            if(self.ballget_0 == 2):
                                None
                            else:
                                mouvement.chargeBallon_0(self)
                        
                        if keys[pygame.K_x] and self.ballget_0 > 0: #Lancer un ballon
                            mouvement.lancerBallon_0(self)
                        
                        if keys[pygame.K_c]:
                            mouvement.grimperRobot_0(self)
                            
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
                        
                        if keys[pygame.K_b]: #Charger un ballon
                            if(ball_1 == 2):
                                None
                            else:
                                mouvement.chargeBallon_1(self)
                                                            
                        if keys[pygame.K_n] and self.ballget_1 > 0: #Lancer un ballon
                            mouvement.lancerBallon_1(self)
                        
                        if keys[pygame.K_m]: #Grimper  
                            mouvement.grimperRobot_1(self)
                          
                    else:   
                        if(self.requeteBallon_1 == False) and (self.requeteGrimper_1 == False):
                            mouvement.publishMove(ZERO,ZERO,twist_1,self.move_robot_1)
                        else:
       
                            if(self.reponseTire_1 == True): #2points vrai
                                self.requeteLancer_1 == False
                                self.reponseTire_1 == False
                                print("Il compte !!!")

                            else:
                                None
                        
                except Exception as e:
                        None
                
        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    
    try:
        
        rospy.init_node('Robot')
        
        move = mouvement()
        move.mouvement_robot_0_1()
        
    except rospy.ROSInterruptException:
        pass