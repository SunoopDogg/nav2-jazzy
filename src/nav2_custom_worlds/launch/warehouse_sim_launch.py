import os
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

_LAUNCH_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
_PKG_DIR = os.path.dirname(_LAUNCH_DIR)

_MODELS_DIRS = ':'.join([
    os.path.join(_PKG_DIR, 'models', 'bookstore_world', 'models'),
    os.path.join(_PKG_DIR, 'models', 'racetrack_world', 'models'),
    os.path.join(_PKG_DIR, 'models', 'small_warehouse_world', 'models'),
])


def generate_launch_description():
    pkg_share = get_package_share_directory('nav2_custom_worlds')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='False',
                              description='Disable Gazebo GUI'),
        DeclareLaunchArgument('slam', default_value='False',
                              description='Run slam_toolbox instead of loading a map'),
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', _MODELS_DIRS),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'tb3_simulation_launch.py')
            ),
            launch_arguments={
                'world': os.path.join(pkg_share, 'worlds', 'small_warehouse.sdf'),
                'map': os.path.join(pkg_share, 'maps', 'small_warehouse.yaml'),
                'params_file': os.path.join(pkg_share, 'config', 'nav2_params.yaml'),
                'slam': LaunchConfiguration('slam'),
                'headless': LaunchConfiguration('headless'),
                'x_pose': '0.0',
                'y_pose': '0.0',
            }.items()
        ),
    ])
