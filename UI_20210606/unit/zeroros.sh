#!/bin/bash
source /home/wenhao/Test_Program/robot_factory_tool/common/ginger_ws/devel/setup.bash
export ROS_MASTER_URI=http://192.168.1.200:11311
export ROS_IP=192.168.1.100
cd ../../robot_factory_tool/zero_test
rosrun camera_test aging_action 10000
