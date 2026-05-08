apt update

apt install -q -y ros-${ROS_DISTRO}-rviz2

git submodule add -b ${ROS_DISTRO} https://github.com/ros-navigation/navigation2.git src/navigation2

source /opt/ros/${ROS_DISTRO}/setup.bash

rosdep install -y \
  --from-paths ./src \
  --ignore-src

colcon build \
  --symlink-install

grep -qF 'GZ_SIM_RESOURCE_PATH' ~/.bashrc || cat >> ~/.bashrc << EOF

# Gazebo Sim environment variables (added by install_nav2_deps.sh)
export GZ_SIM_RESOURCE_PATH=/opt/ros/${ROS_DISTRO}/share/nav2_minimal_tb3_sim/models:/opt/ros/${ROS_DISTRO}/share:/root/nav2-jazzy/src/nav2_custom_worlds/models/bookstore_world/models:/root/nav2-jazzy/src/nav2_custom_worlds/models/racetrack_world/models:/root/nav2-jazzy/src/nav2_custom_worlds/models/small_warehouse_world/models
export GZ_IP=127.0.0.1
EOF

rm -rf /var/lib/apt/lists/*
