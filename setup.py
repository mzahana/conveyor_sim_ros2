from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'conveyor_sim_ros2'

def package_files(directory):
    """Recursively collect all files in a directory for data_files."""
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(path, filename)
            install_path = os.path.join('share', package_name, path)
            paths.append((install_path, [file_path]))
    return paths

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
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        # Include config files
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ] + package_files('models'),  # Include model files recursively
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
