# CMake generated Testfile for 
# Source directory: /home/nvidia/AV/src/darknet_ros-master/darknet_ros
# Build directory: /home/nvidia/AV/build/darknet_ros
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_darknet_ros_rostest_test_object_detection.test "/home/nvidia/AV/build/darknet_ros/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/nvidia/AV/build/darknet_ros/test_results/darknet_ros/rostest-test_object_detection.xml" "--return-code" "/opt/ros/kinetic/share/rostest/cmake/../../../bin/rostest --pkgdir=/home/nvidia/AV/src/darknet_ros-master/darknet_ros --package=darknet_ros --results-filename test_object_detection.xml --results-base-dir \"/home/nvidia/AV/build/darknet_ros/test_results\" /home/nvidia/AV/src/darknet_ros-master/darknet_ros/test/object_detection.test ")
subdirs(gtest)
