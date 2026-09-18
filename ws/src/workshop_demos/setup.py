from glob import glob

from setuptools import setup

package_name = 'workshop_demos'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robotics Society at UC Merced',
    maintainer_email='robotics@todo.todo',
    description='Workshop demos (turtlesim and RViz). No robot hardware needed.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'draw_circle = workshop_demos.draw_circle:main',
        ],
    },
)
