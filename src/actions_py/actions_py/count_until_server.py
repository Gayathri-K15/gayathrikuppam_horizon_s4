#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil


class CountUntilServerNode(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.count_until_server_ = ActionServer(
            self,
            CountUntil,
            "count_until",
            execute_callback=self.execute_callback)
        self.get_logger().info("Action Server has been started.")

    def execute_callback(self, goal_handle: ServerGoalHandle):
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period

        self.get_logger().info("executing the goal")
        counter = 0
        for i in range (target_number):
            counter += 1
            self.get_logger().info(str(counter))
            time.sleep(period)

        goal_handle.succeed()
        
        result = CountUntil.Result()
        result.reached_number = counter
        return result 
def main(args=None):
            rclpy.init(args=args)
            node = CountUntilServerNode()
            rclpy.spin(node)
            rclpy.shutdown()



    