#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys


class ConveyorController(Node):
    def __init__(self):
        super().__init__('conveyor_controller')
        
        # Create publisher for conveyor control
        self.conveyor_pub = self.create_publisher(
            Float64, 
            '/conveyor/cmd_vel', 
            10)
        
        self.get_logger().info('Conveyor controller initialized. Use: ros2 run conveyor_sim_ros2 conveyor_control <speed>')
        
    def set_speed(self, speed):
        msg = Float64()
        msg.data = float(speed)
        self.conveyor_pub.publish(msg)
        self.get_logger().info(f'Setting conveyor speed to: {speed}')


def main(args=None):
    rclpy.init(args=args)
    
    controller = ConveyorController()
    
    # Get speed from command line argument, default to 0.1
    speed = 0.1
    if len(sys.argv) > 1:
        speed = float(sys.argv[1])
    
    controller.set_speed(speed)
    
    try:
        rclpy.spin_once(controller, timeout_sec=2.0)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()