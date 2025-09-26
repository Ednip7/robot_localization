from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import launch_ros.actions
import os
import yaml
from launch.substitutions import EnvironmentVariable
import pathlib
import launch.actions
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        # 1. TF static transforms
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_gps',
            output='screen',
            arguments=['-0.475', '0', '0', '0', '0', '0', 'base_link', 'gps_link'],
        ),
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_imu',
            output='screen',
            arguments=['-0.145', '0', '0', '0', '0', '0', 'base_link', 'id001_imu_link'],
        ),

        # 2. EKF local
        launch_ros.actions.Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[os.path.join(get_package_share_directory("robot_localization"), 'params', 'ekf_local.yaml')],
        ),

        # 3. Navsat transform
        launch_ros.actions.Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            output='screen',
            parameters=[os.path.join(get_package_share_directory("robot_localization"), 'params', 'navsat_transform_custom.yaml')],
        ),

        # 4. EKF global
        launch_ros.actions.Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[os.path.join(get_package_share_directory("robot_localization"), 'params', 'ekf_global.yaml')],
            remappings=[
                ('/odometry/filtered', '/odometry/global')
            ],
        ),
    ])
