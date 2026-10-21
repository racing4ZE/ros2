from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Locate the vehicle Xacro and RViz configuration.
    package_dir = get_package_share_directory('fourze_vehicle_description')
    xacro_file = os.path.join(package_dir, 'urdf', '4ze_vehicle.urdf.xacro')
    rviz_config = os.path.join(package_dir, 'rviz', 'mockup.rviz')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        additional_env={'LIBGL_ALWAYS_SOFTWARE': '1'},
        output='screen'
    )

    pedal_signal_node = Node(
        package='4ze_vehicle_control',
        executable='pedal_signal_node',
        output='screen'
    )

    can_udp_bridge = Node(
        package='4ze_vehicle_can',
        executable='can_udp_bridge',
        parameters=[{
            'windows_host': 'host.docker.internal',
            'udp_port': 5005
        }],
        output='screen'
    )

    return LaunchDescription([
        joint_state_publisher_gui,
        robot_state_publisher,
        rviz,
        pedal_signal_node,
        can_udp_bridge
    ])
