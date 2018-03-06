# Final Project
**Anthony Keydel, Jarrett Philips, Max Schwarz**

## Abstract

## Demo
A video demonstration of the project can viewed on YouTube [here](https://www.youtube.com/watch?v=YfWKpK9FmZg).

## Hardware
This project used a number of physical components. These include:
- Parrot Bebop 2 Drone
- Arcbotics Sparki
- Landing Pad (custom made from cardboard, with printed design on top)

##bebop_automation
start roscore
start driver
angle camera:
rostopic pub --once bebop/camera_control geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, -89, 0]'
get video feed:
rosrun image_view image_view image:=/bebop/image_raw
