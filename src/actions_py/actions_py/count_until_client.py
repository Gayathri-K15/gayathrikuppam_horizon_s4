import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from my_robot_interfaces.action import CountUntil


class CountUntilClientNode(Node):
    def __init__(self):
        super().__init__("count_until_client")
        self.count_until_client = ActionClient(self, CountUntil, "count_until")

    def send_goal(self, target_number, period):
        

        self.count_until_client.wait_for_server()
        goal =CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period
        self.get_logger().info("sending goal")
        self.count_until_client. \
            send_goal_async(goal). \
                add_done_callback(self.goal_response_callback)
    def goal_response_callback(self, future):
          self.goal_handle_:ClientGoalHandle= future.result()  
          if self.goal_handle_.accepted:
              self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
    def goal_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("result: "+ str(result.reached_number))
        
                 



def main(args=None):
            rclpy.init(args=args)
            node = CountUntilClientNode()
            node.send_goal(6,1.0)
            rclpy.spin(node)
            rclpy.shutdown()
        