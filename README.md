# Conveyor Simulation ROS 2 Package

This ROS 2 package provides a simulation of a conveyor belt in Gazebo Harmonic with ROS 2 interface for control.

![custom conveyor](resource/conveyor.png)
## Prerequisites

- ROS 2 (Humble or later recommended)
- Gazebo Harmonic (does not work with earlier versions of Gazebo)
- ros_gz_bridge package

## Building the Package

1. Create a ROS 2 workspace (if you don't have one already):
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

2. Clone this package into your workspace:
```bash
# Assuming you're packaging this code in a git repository
git clone https://github.com/mzahana/conveyor_sim_ros2.git
```

3. Build the package:
```bash
cd ~/ros2_ws
colcon build --packages-select conveyor_sim_ros2
source install/setup.bash
```

## Running the Simulation

1. Launch the Gazebo simulation with the conveyor belt:
```bash
ros2 launch conveyor_sim_ros2 conveyor_sim.launch.py
```

2. Control the conveyor belt speed:
```bash
# Set the conveyor speed to 0.5 (default is 0.1)
ros2 run conveyor_sim_ros2 conveyor_control 0.5

# Or manually publish to the topic
ros2 topic pub --once /conveyor/cmd_vel std_msgs/msg/Float64 "data: 0.5"
```

## Keyboard Control in Gazebo

The conveyor model in Gazebo includes keyboard controls:
- Press 'W' to move the conveyor forward
- Press 'X' to move the conveyor backward
- Press 'S' to stop the conveyor

## Topics

- `/conveyor/cmd_vel` (std_msgs/msg/Float64): Control the speed of the conveyor belt
- Original Gazebo topic: `/model/conveyor/link/base_link/track_cmd_vel`

## Conveyor Bridge Configuration

The package includes a YAML configuration for the ROS-Gazebo bridge located at `config/conveyor_bridge.yaml`. This configuration defines:

1. ROS to Gazebo bridge:
   - ROS topic: `/conveyor/cmd_vel` (std_msgs/msg/Float64)
   - Gazebo topic: `/model/conveyor/link/base_link/track_cmd_vel` (gz.msgs.Double)

You can modify this YAML file to add more bridges or change the topic mappings to suit your needs.

## Conveyor Generation Script
There is a convenience python script ([conveyor_generator.py](scripts/conveyor_generator.py)) which generates SDF model of a custom size (and optionaly with custom texture) conveyor. The details can be found the [conveyor_generator.md](conveyor_generator.md)