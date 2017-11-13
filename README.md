# Lab 7 - Final Project Planning
**Anthony Keydel, Jarrett Philips, Max Schwarz**

## Abstract
We propose to have a quadcopter identify, locate, approach, and land on a moving platform of unknown periodic trajectory.  This project aims to incorporate multiple robotic and learning concepts; including OpenCV, Machine Learning, and 3-Dimensional robotics, to achieve a practical and useful objective. The drone will have to first find the objective landing location, and monitor its motion in order to learn its path and be able to intercept it in the future. The landing pad will be attached to Sparki, and Sparki will decide on a randomized path during setup. A correct interpretation of Sparki’s path and a soft landing are the key challenges and important measurements of success of our project.  

## Equipment
- Drone
- Computer
- Landing Pad
- Sparki

## Implementation Plan
Code can be separated into two programs: Sparki, and drone paired with a computer.

Sparki code will run independently.
Follows a smooth, continuous, predetermined (but not straight) path on a flat plane. Sparki will have a square landing pad mounted on top of it

Drone will work closely with the computer, using the better hardware to handle the larger processing needs of OpenCV.
Drone will take off, look down, and find the landing pad using OpenCV. It will analyze the path of the landing pad (as dictated by Sparki), and predict its next location. The drone will then navigate to that predicted location and land on the pad. 

## Plan For Next Month (11/1 - 12/13)
[ ] Create Sparki Pad - Lead: Jarrett | Deadline: November 8th
 [ ] Create Sparki path program (Random State Machine)
  [ ] Variable Linear Path
  [ ] Variable Circular Path
  [ ] Variable Sin Path 
 [ ] Build physical pad to mount to Sparki
  [ ] Pad will be colored bright green
  [ ] Pad will have a center circle target colored bright red
 [ ] Make sure Sparki can carry the weight of the pad

[ ] Create Vision System - Lead: Anthony | Deadline: November 15th
 [ ] Install OpenCV Python Package & Verify it works with drone camera
 [ ] Write color threshold algorithm to locate pad

[ ] Drone Basic Systems - Lead: Max | Deadline: November 29th (Spans Fall Break)
 [ ] Be able to take off
 [ ] Be able to land
 [ ] Be able to travel in air
  [ ] Subsystems
  [ ] Odometry
  [ ] Accelerometer
  [ ] IK
  [ ] Rotor Control
  [ ] Altitude Control

[ ] Land Drone on Static Pad - Lead: Jarrett | Deadline: December 6th 
 [ ] Combine CV and Drone Basic Systems

[ ] Land Drone on Dynamic Pad - Lead: Anthony | Deadline: December 13th
 [ ] Be able to predict pad’s location
 [ ] Be able to adjust landing destination constantly

## Graceful Failure
Things we can remove:
1. Machine learning (Sparki moves pad in a straight line)
2. OpenCV (Sparki can relay odometry to drone)
3. Sparki (Pad simply is put on the ground)
4. Pad (Drone lands at a set of given coordinates)

## Demo
Simple video demonstration.  Provide examples of each of Sparki’s possible paths. Demonstrate as the drone takes off, scans area, and lands on the pad. 

