# Floor-Mapper


### Project Overview

The Floor-Mapper is a project that aims to collect and process sensor data to map out surroundings of an autonomous robot. The main benefit of this project is that all sensors used are external and thus can be mounted onto any robot. Currently, the main application of this project is creating a map of one’s room by mounting sensors onto an autonomous vacuum robot, such as a Roomba. The application found in this repository contains a simulation aimed at testing different algorithms used to process sensor data by replicating the real-world nuances that a robot might experience, such as noisy sensor data. The red displays the algorithm’s estimate for where the robot/obstacles are, while the black shows the true location of everything. 


### Approach 1: Distance & Heading Sensors

This approach uses a distance sensor that measures the distance from the sensor to an obstacle/wall in the direction of the sensor. In combination with a compass that measures the heading of the robot (what angle the robot is facing), these two sensors are able to determine the position of an obstacle relative to the robot. In addition, every time the robot moves forward, the distance to an obstacle decreases. Using this information, we are also able to determine the position of the robot. 

For example, the robot starts out at (0, 0) and detects an obstacle 9 meters away with a heading of 90 degrees (exactly North). Based on this, we can record a point at (0, 9). Suppose the robot moves forward until the obstacle is 4 meters away. Using the coordinate of the obstacle, we can determine that the robot is at (0, 5). 

By repeating this process for every sensor measurement taken, we are able to retrace the path of the robot while also having a collection of “obstacle” coordinates. The downside of this approach is that the position data is determined by the obstacle data and vice versa, meaning any error becomes compounded. During simulation testing, the position of the robot remained relatively accurate, but obstacle coordinates became scattered and required extensive processing. 


### Approach 2: Triangulation

This approach involves using 3 beacons with known positions. Each beacon measures its distance to the robot, which is fitted with a transmitter. To determine the exact position of the robot, we need to find the intersection of 3 circles centered at the 3 beacons and with radius equal to the distance between the robot and each beacon. 

However, any noise could prevent a perfect intersection between 3 circles. Instead, we solve the equation for 2 circles and end up with up to 2 potential solutions, and simply pick the solution with the shortest distance to any point on the 3rd circle. 

The disadvantage of this approach is that there is no simple way to determine the positions of walls or obstacles. One solution is to create a boundary around all points the robot has been to. However, such an algorithm would be inefficient and extremely complex if the floor layout has additional obstacles. Instead, we will use a bumper that reports any collisions, similar to the one iRobot employs on Roomba. The best solution would be to combine approach 1 and 2, using the distance sensor to determine the location of obstacles. While this approach offers the highest accuracy, it is also more complex and in a real-world setting, would be more expensive (ex. needing an additional 2 sensors for every robot). As a result, this project aims to demonstrate that each approach individually is capable of achieving the desired end result. 


### Processing Obstacle Points

Both approaches leave us with a collection of coordinates, and we somehow need to convert that into a layout — a set of lines that constitute the walls and obstacles. The first challenge is to group the points so that each group forms the general shape of a line. We do this with the following algorithm:



1. Pick a point P and find its closest neighbor Q that has not been picked yet
2. Find the closest point to Q, and check if its slope is consistent with the slope of line PQ
3. If it is, add it to the group and continue finding the closest point and checking if its slope is consistent with the general slope of the group
4. If not, set that point to become the new point P and start over

As a result, points with similar slopes and close proximity are grouped together. To deal with noise, we can add an exception to step #2, where we add the closest point K to Q if and only if there are no points that extend from line QK. 

To determine a line from a group of points, we can either fit a regression or take the 2 furthest points in that group. Both approaches work, although the regression method struggles when there are few points in a group (which frequently happens if there is a large amount of noise). 
