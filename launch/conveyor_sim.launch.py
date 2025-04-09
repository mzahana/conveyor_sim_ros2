#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, EnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    pkg_conveyor_sim = get_package_share_directory('conveyor_sim_ros2')

    # Paths
    world_file = os.path.join(pkg_conveyor_sim, 'worlds', 'conveyor.world')
    model_path = os.path.join(pkg_conveyor_sim, 'models')
    
    # Check if model path exists and print it
    if os.path.exists(model_path):
        print(f"Model path exists: {model_path}")
        # List directories in model path to verify models are there
        for item in os.listdir(model_path):
            full_path = os.path.join(model_path, item)
            if os.path.isdir(full_path):
                print(f"  - Found model directory: {item}")
                # Check for model.sdf and model.config
                if os.path.exists(os.path.join(full_path, 'model.sdf')):
                    print(f"    - model.sdf found")
                if os.path.exists(os.path.join(full_path, 'model.config')):
                    print(f"    - model.config found")
    else:
        print(f"WARNING: Model path does not exist: {model_path}")

    bridge_config_file = os.path.join(pkg_conveyor_sim, 'config', 'conveyor_bridge.yaml')

    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Append to GZ_SIM_RESOURCE_PATH rather than replacing it
    existing_resource_path = EnvironmentVariable('GZ_SIM_RESOURCE_PATH', default_value='')
    if existing_resource_path == '':
        new_resource_path = model_path
    else:
        new_resource_path = f"{existing_resource_path}:{model_path}"
        
    set_model_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=new_resource_path
    )
    
    # Debug: Print environment variables
    print_env = ExecuteProcess(
        cmd=['printenv', 'GZ_SIM_RESOURCE_PATH'],
        output='screen'
    )

    # Launch Gazebo Harmonic with the specified world
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )

    # Launch ROS <-> Gazebo bridge
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
            description='Use simulation clock if true'
        ),
        set_model_path,
        print_env,
        gazebo,
        gz_ros_bridge
    ])