"""Start a simulated robot arm with a laser scanner, and open RViz to see it.

Uses the ROS 2 'dummy_robot' demo (already installed in the desktop image):
  - robot_state_publisher  -> publishes the robot model and TF frames
  - dummy_joint_states     -> makes the joints move
  - dummy_laser            -> publishes fake laser scans on /scan
  - dummy_map_server       -> publishes a small map on /map
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    dummy_launch = os.path.join(
        get_package_share_directory('dummy_robot_bringup'),
        'launch', 'dummy_robot_bringup.launch.py')
    rviz_config = os.path.join(
        get_package_share_directory('workshop_demos'), 'rviz', 'robot_demo.rviz')

    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(dummy_launch)),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_config]),
    ])
