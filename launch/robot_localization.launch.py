from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_local',
            output='screen',
            parameters=['/path/to/ekf_local.yaml'],
            remappings=[
                ('/odometry/filtered', '/odometry/filtered_local'),
                ('/accel/filtered', '/accel/filtered_local')
            ]
        ),
        
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            output='screen',
            parameters=['/path/to/navsat_transform.yaml'],
            remappings=[
                ('/imu', '/olive/imu/id001/filtered_ahrs'),
                ('/gps/fix', '/gps/fix'), 
                ('/odometry/filtered', '/odometry/filtered_local')
            ]
        ),
        
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_global',
            output='screen',
            parameters=['/path/to/ekf_global.yaml'],
            remappings=[
                ('/odometry/filtered', '/odometry/filtered_global')
            ]
        )
    ])