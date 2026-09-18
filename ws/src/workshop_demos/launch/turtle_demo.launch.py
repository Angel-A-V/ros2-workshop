"""Open turtlesim and make the turtle drive in circles."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='workshop_demos', executable='draw_circle', output='screen'),
    ])
