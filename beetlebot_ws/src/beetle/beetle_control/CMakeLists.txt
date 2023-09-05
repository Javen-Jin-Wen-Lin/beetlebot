cmake_minimum_required(VERSION 2.8.3)
project(beetle_control)
find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package(
CATKIN_DEPENDS rospy
)
include_directories()

catkin_install_python(PROGRAMS
  nodes/beetle_control.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
