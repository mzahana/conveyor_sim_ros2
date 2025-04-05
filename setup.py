from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'conveyor_sim_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # Include world files
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        # Include config files
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Package for simulating a conveyor belt in Gazebo Harmonic',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'conveyor_control = conveyor_sim_ros2.conveyor_control:main',
        ],
    },
)