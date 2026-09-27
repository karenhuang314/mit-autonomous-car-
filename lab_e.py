"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-outreach-labs

File Name: lab_e.py

Title: Lab E - Stoplight Challenge

Author: Karen Huang 

Purpose: Write a script to enable autonomous behavior from the RACECAR. When
the RACECAR sees a stoplight object (colored cube in the simulator), respond accordingly
by going straight, turning right, turning left, or stopping. Append instructions to the
queue depending on whether the position of the RACECAR relative to the stoplight reaches
a certain threshold, and be able to respond to traffic lights at consecutive intersections. 

Expected Outcome: When the user runs the script, the RACECAR should control itself using
the following constraints:
- When the RACECAR sees a BLUE traffic light, make a right turn at the intersection
- When the RACECAR sees an ORANGE traffic light, make a left turn at the intersection
- When the RACECAR sees a GREEN traffic light, go straight
- When the RACECAR sees a RED traffic light, stop moving,
- When the RACECAR sees any other traffic light colors, stop moving.

Considerations: Since the user is not controlling the RACECAR, be sure to consider the
following scenarios:
- What should the RACECAR do if it sees two traffic lights, one at the current intersection
and the other at the intersection behind it?
- What should be the constraint for adding the instructions to the queue? Traffic light position,
traffic light area, or both?
- How often should the instruction-adding function calls be? Once, twice, or 60 times a second?

Environment: Test your code using the level "Neo Labs > Lab 3: Stoplight Challenge".
By default, the traffic lights should direct you in a counterclockwise circle around the course.
For testing purposes, you may change the color of the traffic light by first left-clicking to 
select and then right clicking on the light to scroll through available colors.
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour (Adjust threshold!)
MIN_CONTOUR_AREA = 300

# TODO Part 1: Determine the HSV color threshold pairs for ORANGE, GREEN, RED, YELLOW, and PURPLE
# Colors, stored as a pair (hsv_min, hsv_max)
BLUE = ((100, 150, 150), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((30, 50, 50), (80, 255, 255))  # The HSV range for the color green
RED = [((0, 50, 50), (10, 255, 255)), ((170, 100, 100), (179, 255, 255))]  # The HSV range for the color red
ORANGE = ((10, 50, 50), (20, 255, 255))  # The HSV range for the color orange
YELLOW = ((20, 50, 50), (30, 255, 255))  # The HSV range for the color yellow
PURPLE = ((125, 50, 50), (165, 255, 255))  # The HSV range for the color purple

# >> Variables
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

queue = [] # The queue of instructions
is_queue_empty = ""  # The queue of instructions
stoplight_color = "" # The current color of the stoplight
speed = 0
angle = 0

########################################################################################
# Functions
########################################################################################
# [FUNCTION] Get contours for a specific color range
def get_contour_for_color(image, lower_bound, upper_bound):

    # Change color space from BGR to HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # Create a binary mask for the specific color image 
    mask = cv.inRange(hsv, lower_bound, upper_bound)

    # Find valid contours on the mask
    contours,_ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    return contours


# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global stoplight_color

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0

    # Get contours for each color
    red_contours  = get_contour_for_color(image, RED[0][0], RED[0][1])
    red_contours  += get_contour_for_color(image, RED[1][0], RED[1][1])
    blue_contours = get_contour_for_color(image, BLUE[0], BLUE[1])
    green_contours = get_contour_for_color(image, GREEN[0], GREEN[1])
    orange_contours = get_contour_for_color(image, ORANGE[0], ORANGE[1])
 
    # Apply priority rules to select the correct contour:RED>BLUE>GREEN>ORANGE
    if red_contours:
        largest_red_contour = rc_utils.get_largest_contour(red_contours, MIN_CONTOUR_AREA)

        if largest_red_contour is not None:
            contour_center = rc_utils.get_contour_center(largest_red_contour)
            contour_area = rc_utils.get_contour_area(largest_red_contour)

            stoplight_color = "Red"
            print(f"stoplight_color = {stoplight_color}") 

    elif blue_contours:
        largest_blue_contour = rc_utils.get_largest_contour(blue_contours, MIN_CONTOUR_AREA)

        if largest_blue_contour is not None:
            contour_center = rc_utils.get_contour_center(largest_blue_contour)
            contour_area = rc_utils.get_contour_area(largest_blue_contour)

            stoplight_color = "Blue"
            print(f"stoplight_color = {stoplight_color}") 

    elif orange_contours:
        largest_orange_contour = rc_utils.get_largest_contour(orange_contours, MIN_CONTOUR_AREA)

        if largest_orange_contour is not None:
            contour_center = rc_utils.get_contour_center(largest_orange_contour)
            contour_area = rc_utils.get_contour_area(largest_orange_contour)

            stoplight_color = "Orange"
            print(f"stoplight_color = {stoplight_color}") 

    elif green_contours:
        largest_green_contour = rc_utils.get_largest_contour(green_contours, MIN_CONTOUR_AREA)

        if largest_green_contour is not None:
            contour_center = rc_utils.get_contour_center(largest_green_contour)
            contour_area = rc_utils.get_contour_area(largest_green_contour)

            stoplight_color = "Green"
            print(f"stoplight_color = {stoplight_color}") 

#    elif orange_contours:
#        largest_orange_contour = rc_utils.get_largest_contour(orange_contours, MIN_CONTOUR_AREA)
#
#        if largest_orange_contour is not None:
#            contour_center = rc_utils.get_contour_center(largest_orange_contour)
#            contour_area = rc_utils.get_contour_area(largest_orange_contour)
#
#            stoplight_color = "Orange"
#            print(f"stoplight_color = {stoplight_color}") 

    else:
        stoplight_color = "Red"

        # Display the image to the screen
        rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global queue
    global speed
    global angle
    global is_queue_empty
    global stoplight_color

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message (You may edit this to be more informative!)
    print(
        ">> Lab 3 - Stoplight Challenge\n"
        "\n"
        "Controls:\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue
    global speed
    global angle
    global stoplight_color
    global is_queue_empty

    update_contour()

    # TODO Part 2: Complete the conditional tree with the given constraints.
    if is_queue_empty == "YES":
        
        if stoplight_color == "Red":
            stopNow()
        elif stoplight_color == "Blue":
            turnRight()
        elif stoplight_color == "Green":
            goStraight()
        elif stoplight_color == "Orange":
            turnLeft()
        else:
            stopNow()

    # TODO Part 3: Implement a way to execute instructions from the queue once they have been placed
    # by the traffic light detector logic (Hint: Lab 2)

    # Per lab_d(lab2), if the queue is not empty, follow the current drive instruction
    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        queue[0][0] -= rc.get_delta_time()
        if queue[0][0] <= 0:
            queue.pop(0)

        is_queue_empty = "NO"
    else:
        speed = 0
        angle = 0
        is_queue_empty = "YES" 

    print(queue)
    print(f"is_queue_empty = {is_queue_empty}")

    # Send speed and angle commands to the RACECAR
    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)

# [FUNCTION] Appends the correct instructions to make a 90 degree right turn to the queue
def turnRight():
    global queue

    # TODO Part 4: Complete the rest of this function with the instructions to make a right turn
 
    queue.clear()

    queue.append([6.0, 0.25, 0])
    queue.append([5.5, 0.25, 1])
    queue.append([3.0, 0.25, 0])

# [FUNCTION] Appends the correct instructions to make a 90 degree left turn to the queue
def turnLeft():
    global queue

    # TODO Part 5: Complete the rest of this function with the instructions to make a left turn

    queue.clear()

    queue.append([6.0, 0.25, 0])
    queue.append([5.5, 0.25, -1])
    queue.append([3.0, 0.25, 0])

# [FUNCTION] Appends the correct instructions to go straight through the intersectionto the queue
def goStraight():
    global queue

    # TODO Part 6: Complete the rest of this function with the instructions to make a left turn

    queue.clear()

    queue.append([15.0, 0.25, 0])

# [FUNCTION] Clears the queue to stop all actions
def stopNow():
    global queue
    queue.clear()

def update_slow():
    pass
########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
