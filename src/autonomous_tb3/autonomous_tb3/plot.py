#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String , Header
import matplotlib.pyplot as plt
import numpy as np
from dwb_msgs.msg import LocalPlanEvaluation
from dwb_msgs.msg import CriticScore
from dwb_msgs.msg import TrajectoryScore
from nav_msgs.msg import Path, Odometry
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

class Plot(Node):
    def __init__(self):
        super().__init__('plot')
        # self.score = None
        # self.eval = self.create_subscription(LocalPlanEvaluation, "/evaluation", self.eval_callback, 10)
        self.path = self.create_subscription(Path,"/plan", self.callback,10) 
        self.path_length = 0
        self.flag = False
        

    # def eval_callback(self, msg : LocalPlanEvaluation):
    #     temp = msg.twists[:2]
    #     self.score = temp
    #     self.get_logger().info(str(self.score))
    
    def callback(self,path_msg):
        # navigator = BasicNavigator()
        # result = navigator.getResult()
        if self.flag == False:
            print(len(path_msg.poses) )
            for i in range(len(path_msg.poses) - 1):
                position_a_x = path_msg.poses[i].pose.position.x
                position_b_x = path_msg.poses[i+1].pose.position.x
                position_a_y = path_msg.poses[i].pose.position.y
                position_b_y = path_msg.poses[i+1].pose.position.y

                self.path_length += np.sqrt(np.power((position_b_x - position_a_x), 2) + np.power((position_b_y- position_a_y), 2))
                # result = navigator.getResult()
                # if result == TaskResult.SUCCEEDED:
                #    print('Goal succeeded!')
                #    break
            self.get_logger().info(str(self.path_length))
            self.flag = True
        # self.path_length = 0
        # navigator.lifecycleShutdown()


def main(args=None):
    rclpy.init(args=args)
    node = Plot()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == '__main__':
    main()