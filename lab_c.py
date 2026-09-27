"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-outreach-labs

File Name: lab_c.py

Title: Lab C - RACECAR Controller

Author: Karen Huang

Purpose: Using a Python script and the data polled from the controller module,
write code to replicate a manual control scheme for the RACECAR. Gain a mastery
in using conditional statements, controller functions and an understanding in the
rc.drive.set_speed_angle() function. Complete the lines of code under the #TODO indicators 
to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the right trigger is pressed, the RACECAR drives forward
- When the left trigger is pressed, the RACECAR drives backward
- When the left joystick's x-axis has a value of greater than 0, the RACECAR's wheels turns to the right
- When the left joystick's x-axis has a value of less than 0, the RACECAR's wheels turns to the left
- When the "A" button is pressed, increase the speed and print the current speed to the terminal window
- When the "B" button is pressed, reduce the speed and print the current speed to the terminal window
- When the "X" button is pressed, increase the turning angle and print the current turning angle to the terminal window
- When the "Y" button is pressed, reduce the turning angle and print the current turning angle to the terminal window
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

# Declare any global variables here
global speed
global angle
global speed_offset
global angle_offset

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle
    global speed_offset
    global angle_offset

    global speed1
    global angle1

    speed1 = 0.5
    angle1 = 0.5

    speed = 0.0 # The initial speed is at 1.0
    angle = 0.0 # The initial turning angle away from the center is at 0.0
    speed_offset = 0.5 # The initial speed offset is 0.5
    angle_offset = 1.0 # The inital angle offset is 1.0

    # This tells the car to begin at a standstill
    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed
    global angle
    global speed_offset
    global angle_offset
    
    global speed1
    global angle1

    # TODO Part 1: Modify the following conditional statement such that when the
    # right trigger is pressed, the RACECAR moves forward at the designated speed.
    # when the left trigger is pressed, the RACECAR moves backward at the designated speed.
    if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) > 0.5:
        speed = speed1
    elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) > 0.5:
        speed = -speed1
    else:
        speed = 0
      
    # TODO Part 2: Modify the following conditional statement such that when the
    # value of the left joystick's x-axis is greater than 0, the RACECAR's wheels turn right.
    # When the value of the left joystick's x-axis is less than 0, the RACECAR's wheels turn left.
    (x, y) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    if x > 0.5:
        angle = angle1
    elif x < -0.5:
        angle = -angle1
    else:
        angle = 0
    #print(f"Angle1 after Joystick = {angle1}")

    # TODO Part 3: Write a conditional statement such that when the
    # "A" button is pressed, increase the speed of the RACECAR. When the "B" button is pressed,
    # decrease the speed of the RACECAR. Print the current speed of the RACECAR to the
    # terminal window.
    if rc.controller.was_released(rc.controller.Button.A):
        speed1 += 0.1
        if speed1 >= 1.0:
            speed1 = 1.0
    elif rc.controller.was_released(rc.controller.Button.B):
        speed1 -= 0.1
        if speed1 <= -1.0:
            speed1 = -1.0

    print(f"Speed = {speed}, Angle = {angle}")

    # TODO Part 4: Write a conditional statement such that when the
    # "X" button is pressed, increase the turning angle of the RACECAR. When the "Y" button 
    # is pressed, decrease the turning angle of the RACECAR. Print the current turning angle 
    # of the RACECAR to the terminal window.
    #if rc.controller.was_pressed(rc.controller.Button.X):
    if rc.controller.is_down(rc.controller.Button.X):

        print(f"Angle1 at Button X = {angle1}")
        angle1 += 0.1
        if angle1 >= 1.0:
            angle1 = 1.0
        angle = angle1
        print(f"Speed = {speed}, Angle = {angle}")

    #elif rc.controller.was_pressed(rc.controller.Button.Y):
    elif rc.controller.is_down(rc.controller.Button.Y):

        print(f"Angle1 at Button Y = {angle1}")
        angle1 -= 0.1
        if angle1 <= -1.0:
            angle1 = -1.0
        angle = angle1
        print(f"Speed = {speed}, Angle = {angle}")


    #print(f"Speed = {speed}, Angle = {angle}")
    # Send the speed and angle values to the RACECAR
    rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
