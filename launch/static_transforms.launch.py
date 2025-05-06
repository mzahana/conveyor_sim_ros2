from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import math

def generate_launch_description():
    """
    Launch file to publish static transforms for cameras and lidar
    relative to the textured conveyor belt in the Gazebo Harmonic warehouse simulation.
    
    TF tree hierarchy:
    conveyor_link → bracket → dual_bar → left_camera_base/right_camera_base
                           → lidar
    camera_base → camera_optical_frame
    
    static_transform_publisher arguments: x y z yaw pitch roll
    """
    # Launch arguments
    conveyor_frame_arg = DeclareLaunchArgument(
        'conveyor_frame', 
        default_value='textured_conveyor/link',
        description='The frame ID of the conveyor belt'
    )
    
    conveyor_frame = LaunchConfiguration('conveyor_frame')
    
    # Constants for transform calculations
    deg_to_rad = math.pi / 180.0
    
    return LaunchDescription([
        # Include launch arguments
        conveyor_frame_arg,
        
        # 1. Conveyor to bracket
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='conveyor_to_bracket_tf_publisher',
            arguments=[
                '0', '0', '2.0',                    # x, y, z (bracket at same x,y as conveyor, 2m up)
                str(math.pi/2), '0', '0',           # yaw, pitch, roll (90° rotation around Z)
                conveyor_frame,                      # Parent frame
                'bracket/horizontal_bar'             # Child frame
            ],
            output='screen'
        ),
        
        # 2. Bracket to dual bar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='bracket_to_dual_bar_tf_publisher',
            arguments=[
                '0', '0', '0',                      # x, y, z (centered on bracket)
                str(-math.pi/2), '0', '0',          # yaw, pitch, roll (-90° around Z)
                'bracket/horizontal_bar',            # Parent frame
                'dual_camera_bar/horizontal_bar'     # Child frame
            ],
            output='screen'
        ),
        
        # 3. Dual bar to left camera base
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='dual_bar_to_left_camera_tf_publisher',
            arguments=[
                '-0.5', '0', '-0.05',               # x, y, z (-0.5m from center, small z offset)
                '0', str(45 * deg_to_rad), '0',     # yaw, pitch, roll (45° pitch)
                'dual_camera_bar/horizontal_bar',    # Parent frame
                'left_camera/link/realsense_d435'    # Child frame
            ],
            output='screen'
        ),
        
        # 4. Left camera base to optical frame
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='left_camera_to_optical_tf_publisher',
            arguments=[
                '0', '0', '0',                      # No translation
                str(-math.pi/2), '0', str(-math.pi/2),  # yaw, pitch, roll
                'left_camera/link/realsense_d435',         # Parent frame
                'left_camera/link/realsense_d435_optical'  # Child frame
            ],
            output='screen'
        ),
        
        # 5. Dual bar to right camera base
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='dual_bar_to_right_camera_tf_publisher',
            arguments=[
                '0.5', '0', '-0.05',                # x, y, z (0.5m from center, small z offset)
                str(math.pi), str(45 * deg_to_rad), '0',  # yaw, pitch, roll (180° yaw, 45° pitch)
                'dual_camera_bar/horizontal_bar',    # Parent frame
                'right_camera/link/realsense_d435'   # Child frame
            ],
            output='screen'
        ),
        
        # 6. Right camera base to optical frame
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='right_camera_to_optical_tf_publisher',
            arguments=[
                '0', '0', '0',                      # No translation
                str(-math.pi/2), '0', str(-math.pi/2),  # yaw, pitch, roll
                'right_camera/link/realsense_d435',        # Parent frame
                'right_camera/link/realsense_d435_optical' # Child frame
            ],
            output='screen'
        ),
        
        # 7. Bracket to 3D lidar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='bracket_to_lidar_tf_publisher',
            arguments=[
                '0.1', '0.1', '0',                 # x, y, z (small offset on bracket)
                '0', '0', str(math.pi/2),          # yaw, pitch, roll (90° roll)
                'bracket/horizontal_bar',           # Parent frame
                'lidar_3d/link/gpu_lidar'           # Child frame
            ],
            output='screen'
        ),
    ])