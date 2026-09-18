"""Drive the turtlesim turtle in a circle.

This is the same idea as the real robot: a node publishes velocity
commands (geometry_msgs/Twist) on a topic, and something else moves.

Try changing the numbers while it runs (in another terminal):
    ros2 param set /draw_circle speed 4.0
    ros2 param set /draw_circle turn -2.0
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class DrawCircle(Node):

    def __init__(self):
        super().__init__('draw_circle')
        self.declare_parameter('speed', 2.0)   # forward speed
        self.declare_parameter('turn', 1.0)    # turning speed
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.send_command)  # 10 times per second
        self.get_logger().info('Driving turtle1 in a circle. Press Ctrl+C to stop.')

    def send_command(self):
        msg = Twist()
        msg.linear.x = float(self.get_parameter('speed').value)
        msg.angular.z = float(self.get_parameter('turn').value)
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DrawCircle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
