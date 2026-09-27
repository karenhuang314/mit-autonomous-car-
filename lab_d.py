"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-outreach-labs

File Name: lab_d.py

Title: Lab D - Driving in Shapes

Author: Karen Huang 

Purpose: Create a script to enable semi-autonomous driving for the RACECAR. Button presses
enable a series of instructions sent to the RACECAR, which enable it to drive in various shapes.
Complete the lines of code under the #TODO indicators to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the "A" button is pressed, drive in a Zigzag
- When the "B" button is pressed, drive in a Spiral
- When the "X" button is pressed, drive in a Hallway 
- When the "Y" button is pressed, drive in a Maze 
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# A queue of driving steps to execute
# Each entry is a list containing (time remaining, speed, angle)
queue = []
speed = 0
angle = 0

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    # Begin at a full stop
    rc.drive.stop()

    # Begin with an empty queue
    queue.clear()

    # Print start message
    # TODO Part 1: Add a line explaining what the Y button does
#    print(
#        ">> Lab 1 - Driving in Shapes\n"
#        "\n"
#        "Controls:\n"
#        "   Right trigger = accelerate forward\n"
#        "   Left trigger = accelerate backward\n"
#        "   Left joystick = turn front wheels\n"
#        "   A button = drive in a circle\n"
#        "   B button = drive in a square\n"
#        "   X button = drive in a figure eight\n"
#        "   Y button = drive in a <shape of your choice>\n"
#    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue
    global speed
    global angle

    # When the A button is pressed, add instructions to drive in a zigzag
    if rc.controller.was_pressed(rc.controller.Button.A):
        drive_zigzag()

    # When the B button is pressed, add instructions to drive in a spiral
    if rc.controller.was_pressed(rc.controller.Button.B):
        drive_spiral()

    # When the X button is pressed, add instructions to drive in a hallway 
    if rc.controller.was_pressed(rc.controller.Button.X):
        drive_hallway()

    # When the Y button is pressed, add instructions to drive in a maze 
    if rc.controller.was_pressed(rc.controller.Button.Y):
        drive_maze()

    # TODO Analyze the following code segment that executes instructions from the queue.
    # Determine how the script processes the instructions and then sends the correct speed
    # and angle commands to the RACECAR.

    # If the queue is not empty, follow the current drive instruction
    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        queue[0][0] -= rc.get_delta_time()
        if queue[0][0] <= 0:
            queue.pop(0)
    else:
        speed = 0
        angle = 0

    # Send speed and angle commands to the RACECAR
    print(queue)
    rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in a "Zigzag"
def drive_zigzag():
    global queue

    queue.clear()

    queue.append([3.6, 0.5, 0])
    queue.append([1.8, 0.5, 1])  # turn right
    queue.append([1.6, 0.5, 0.5])  # turn right
    queue.append([1.8, 0.5, -1]) # turn left
    queue.append([2, 0.5, -0.5]) # turn left
    queue.append([1.0, 0.5, 0])

# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in a "Spiral"
def drive_spiral():
    global queue

    queue.clear()

    queue.append([3.0, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([3.3, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([2.7, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([1.8, 1, 0])
    queue.append([1.4, 1, 1])
    queue.append([0.5, 1, 0])
    

# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in a "Hallway" 
def drive_hallway():
    global queue

    # TODO Part 5: Create constants that represent the RACECAR driving through
    # different parts of the figure 8, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([1, 0.5, 0])
    queue.append([1.8, 0.5, 0.3])
    queue.append([2.8, 0.5, -0.5])
    queue.append([2, 0.5, 1])
    queue.append([1.4, 0.5, -0.4])
    queue.append([1.0, 0.5, -1])
    queue.append([0.8, 0.5, 0])
    queue.append([0.6, 0.5, 0.2])
    queue.append([1.5, 0.5, 1])
    queue.append([1.0, 0.5, -0.4])
    queue.append([1.4, 0.5, -1])
    queue.append([0.8, 0.5, 1])
    queue.append([2.1, 0.5, 0])


# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in a "Maze" 
def drive_maze():
    global queue

    # TODO Part 6: Create constants that represent the RACECAR driving through
    # different parts of the shape, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([5.1, 1, 0])
    queue.append([1.2, 1, -1]) 
    queue.append([2.6, 1, 0]) 

    queue.append([3.0, 0.2, -1]) 
    queue.append([2.0, -0.5, 1]) 
    queue.append([1.8, 1, -1]) 

    queue.append([2.2, 1, 0]) 

    queue.append([3.0, 0.2, 1]) 
    queue.append([2.0, -0.5, -1]) 
    queue.append([1.8, 1, 1]) 

    queue.append([1.0, 1, 0]) 

    queue.append([1.3, 1, -1]) 

    queue.append([0.6, 1, 0]) 

    queue.append([3.0, 0.2, 1]) 
    queue.append([2.0, -0.5, -1]) 
    queue.append([2.0, 1, 1]) 

    queue.append([1.0, 1, 0]) 

    queue.append([4.0, 0.2, -1]) 
    queue.append([2.0, -0.5, 1]) 
    queue.append([1.6, 1, -1]) 

    queue.append([3.3, 1, 0]) 

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
