# MIT-Autonomous-Car

### Hardware
**Platform:** MIT RACECAR
**Sensors:** 
  * RGB Camera (Line detection & color classification)
  * LiDAR (Obstacle detection)
  * IMU (Angular velocity & acceleration)
### Software
* Python 3.12
* Operating System: Ubuntu Linux / ROS (Robot Operating System)
* RACECAR Library ('racecar_core')
* OpenCV ('opencv-python')
* NumPy ('numpy')

## Technical Design
Course Traversal: The autonomous vehicle's steering angle is calculated based on the error offset between frame center and the central point of the contour. 

Color Priority: When multiple colored lines are detected, the following hierarchy is implemented:
Red > Green > Blue

Purpose: Write a script to enable fully autonomous behavior from the RACECAR. The
RACECAR will traverse the obstacle course autonomously without human intervention.
Once the start button is pressed, the RACECAR must drive through the course until it
reaches the white cone at the end, in which it will then stop. You are disqualified if
you stop too far from the cone or hit the cone.

Expected Outcome: When the user runs the script, they must not be able to manually control
the RACECAR. The RACECAR must move forward on its own, traverse through the course, and then
stop on its own.
- The speed of the RACECAR can be controlled by a state machine or script, but not by the user
- The angle of the RACECAR should only be controlled by the center of the line contour
- The RACECAR sees the color RED as the highest priority, then GREEN, then BLUE
- The RACECAR must stop before the white cone at the end of the course. The RACECAR must stop
close enough to the cone such that it does not see the entirety of the white cone at the end
of the race. (less than 30 cm). The RACECAR must not hit the white cone.
"""

## Repository Structure

├── 00_main.py              # Primary autonomous script for final race (final version code)
├── cone_slalom             # Cone slalom navigation module
├── driving_in_shapes       # Driving in shapes
├── line_follower           # Color line tracking
├── pathfinding             # Pathfinding logic for vehicle trajectory planning
├── racecar_controller      # Vehicle motor and steering control wrapper
├── sign_detection         # Deep learning sign detection training
├── stoplight_challenge     # Visual traffic light recognition module
├── wall_follower           # LiDAR safety stop and wall-following algorithms
└── README.md               # Project documentation
