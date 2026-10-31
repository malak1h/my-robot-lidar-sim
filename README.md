# my-robot-lidar-sim

A differential-drive robot in ROS 2 Humble and Gazebo Classic with a simulated 360° LiDAR, plus a node that stops the robot before it hits an obstacle.

> Simulation only. Built as part of a student autonomous vehicles activity.

## What's inside

- `urdf/robot.urdf.xacro`: robot model (chassis, two wheels, diff-drive plugin, LiDAR sensor)
- `launch/simulation.launch.py`: starts Gazebo and spawns the robot
- `scripts/stop_node.py`: reads `/scan` and publishes to `/cmd_vel`, stopping when an obstacle is closer than 1 m

## LiDAR settings

| Setting | Value |
|---|---|
| Beams | 360 (1° resolution) |
| Range | 0.12 m to 10 m |
| Update rate | 10 Hz |
| Topic | `/scan` (`sensor_msgs/LaserScan`) |
| Frame | `lidar_link` |

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- `ros-humble-gazebo-ros-pkgs`, `ros-humble-rviz2`

## Build and run

```bash
mkdir -p ~/gazebo_ws/src
cd ~/gazebo_ws/src
git clone https://github.com/malak1h/my-robot-lidar-sim.git my_robot_description
cd ~/gazebo_ws
colcon build --packages-select my_robot_description
source install/setup.bash
ros2 launch my_robot_description simulation.launch.py
```

Add a few boxes in front of the robot in Gazebo, then in a new terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/gazebo_ws/install/setup.bash
python3 ~/gazebo_ws/src/my_robot_description/scripts/stop_node.py
```

Options: `--ros-args -p stop_distance:=0.6 -p speed:=0.3 -p cone_deg:=20.0`

## View the scan in RViz

```bash
rviz2 --ros-args -p use_sim_time:=true
```

Set Fixed Frame to `odom`, add a LaserScan display on `/scan`, and set Reliability to Best Effort.

## Lessons learned

- Missing scan in RViz is usually TF, QoS (Best Effort vs Reliable), or `use_sim_time`.
- In an empty world every beam reads `inf`, so RViz shows nothing.

## Next steps

- Obstacle avoidance (turning, not only stopping)
- SLAM and Nav2
