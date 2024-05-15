import rospy
import std_msgs.msg
from time import sleep as s
from os import system

class game:
    def __init__(self):
        rospy.Subscriber("/bluePoint", std_msgs.msg.Int64, self.bluePoints)
        rospy.Subscriber("/redPoint", std_msgs.msg.Int64, self.redPoints)
        self.blueTeam = {
            "shoot":0,
            "climb":0
        }
        self.redTeam = {
            "shoot":0,
            "climb":0
        }

    def bluePoints(self, point):
        if point.data == 2 or point.data == 1:
            self.blueTeam["shoot"] += point.data

        if  point.data == 5:
            self.blueTeam["climb"] += point.data

    def redPoints(self, point):
        if point.data == 2 or point.data == 1:
            self.redTeam["shoot"] += point.data

        if  point.data == 5:
            self.redTeam["climb"] += point.data
            
    def pointsTotal(self):
        print(f"\n\rBlue Teams: Climbing Points: {self.blueTeam['climb']} / Shoot Points: {self.blueTeam['shoot']}")
        print(f"\n\rRed Teams: Climbing Points: {self.redTeam['climb']} / Shoot Points: {self.redTeam['shoot']}")

if __name__ == "__main__":
    point = game()
    while True:
        rospy.init_node('game', anonymous=True)    # init du noed ROS
        try:
            while not rospy.is_shutdown():  
                system('clear')
                point.pointsTotal()
                s(0.1)
                    
        except rospy.ROSInterruptException:
            pass