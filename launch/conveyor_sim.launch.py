#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_conveyor_sim = get_package_share_directory('conveyor_sim_ros2')
    
    # Path to the world file
    world_file = os.path.join(pkg_conveyor_sim, 'worlds', 'conveyor.sdf')
    
    # Path to the bridge config file
    bridge_config_file = os.path.join(pkg_conveyor_sim, 'config', 'conveyor_bridge.yaml')
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Gazebo Harmonic launch
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )
    
    # ROS GZ Bridge using YAML configuration
    gz_ros_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='conveyor_bridge',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'config_file': bridge_config_file
        }]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock if true'),
        
        # Launch Gazebo
        gazebo,
        
        # Launch ROS GZ Bridge
        gz_ros_bridge,
    ])