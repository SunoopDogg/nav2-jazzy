import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

_SRC_WORLDS_DIR = os.path.join('/root/nav2-jazzy', 'src', 'nav2_custom_worlds', 'models')

_MODELS_DIRS = ':'.join([
    os.path.join(_SRC_WORLDS_DIR, 'bookstore_world', 'models'),
    os.path.join(_SRC_WORLDS_DIR, 'racetrack_world', 'models'),
    os.path.join(_SRC_WORLDS_DIR, 'small_warehouse_world', 'models'),
])


def generate_launch_description():
    pkg_share = get_package_share_directory('nav2_custom_worlds')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    headless = LaunchConfiguration('headless')
    slam = LaunchConfiguration('slam')
    use_rviz = LaunchConfiguration('use_rviz')

    urdf_path = os.path.join(pkg_share, 'urdf', 'go2.urdf')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    # Gazebo server: bookstore.sdf is plain SDF (no xacro needed)
    # headless = don't start the GUI client (server always runs)
    gz_server = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s',
             os.path.join(pkg_share, 'worlds', 'bookstore.sdf')],
        output='screen',
    )

    gz_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'),
                         'launch', 'gz_sim.launch.py')
        ),
        condition=IfCondition(PythonExpression(['not ', headless])),
        launch_arguments={'gz_args': '-v4 -g'}.items(),
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_share, 'config', 'go2_bridge.yaml'),
            'expand_gz_topic_names': False,
            'use_sim_time': True,
        }],
        output='screen',
    )

    spawn_go2 = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name', 'go2',
            '-file', os.path.join(pkg_share, 'models', 'go2', 'model.sdf'),
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.01',
        ],
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description,
        }],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'go2_nav2.rviz')],
        parameters=[{'use_sim_time': True}],
        condition=UnlessCondition(headless),
        output='screen',
    )

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'slam': slam,
            'map': os.path.join(pkg_share, 'maps', 'bookstore.yaml'),
            'params_file': os.path.join(pkg_share, 'config', 'nav2_params_go2.yaml'),
            'use_sim_time': 'true',
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='False',
                              description='Skip gz GUI client and RViz (server still runs)'),
        DeclareLaunchArgument('slam', default_value='False',
                              description='Run slam_toolbox instead of loading a map'),
        DeclareLaunchArgument('use_rviz', default_value='True',
                              description='Launch RViz2'),
        SetEnvironmentVariable('GZ_IP', '127.0.0.1'),
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', _MODELS_DIRS),
        gz_server,
        gz_client,
        bridge,
        spawn_go2,
        rsp,
        rviz,
        nav2_bringup,
    ])
