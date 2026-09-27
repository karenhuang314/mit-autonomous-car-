"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-outreach-labs

File Name: Team10_MiniGrandPrix.py

Title: Grand Prix Day!

Author: Karen Huang 

Purpose: Write a script to enable fully autonomous behavior from the RACECAR. The
RACECAR will traverse the obstacle course autonomously without human intervention.
Once the start button is pressed, the RACECAR must drive through the course until it
reaches the white cone at the end, in which it will then stop. You are disqualified if
you stop too far from the cone or hit the cone.

Note: There is no template code in this document to follow except for the RACECAR script 
structure found in template.py. You are expected to use code written from previous labs
to complete this challenge. Good luck!

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

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))

# TODO Part 1: Determine the HSV color threshold pairs for GREEN and RED
# Colors, stored as a pair (hsv_min, hsv_max) Hint: Lab E!
RED = [((0, 50, 50), (10, 255, 255)), ((170, 100, 100), (179, 255, 255))]  # The HSV range for the color red
GREEN = ((30, 1, 1), (80, 255, 255))  # The HSV range for the color green
BLUE = ((90, 50, 50), (120, 255, 255))  # The HSV range for the color blue
ORANGE = ((10, 50, 50), (20, 255, 255))  # The HSV range for the color orange
YELLOW = ((20, 50, 50), (30, 255, 255))  # The HSV range for the color yellow
PURPLE = ((125, 50, 50), (165, 255, 255))  # The HSV range for the color purple

# Color priority: Orange >> Green >> Red >> Blue >> Purple


# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour


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

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Crop the image to the floor directly in front of the car
        image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

        # Search for line colors, and update the global variables
        # contour_center and contour_area with the largest contour found

        # Get contours for each color
        red_contours  = rc_utils.find_contours(image, RED[0][0], RED[0][1])
        red_contours  += rc_utils.find_contours(image, RED[1][0], RED[1][1])
        blue_contours = rc_utils.find_contours(image, BLUE[0], BLUE[1])
        green_contours = rc_utils.find_contours(image, GREEN[0], GREEN[1])
        orange_contours = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])
        orange_contours += rc_utils.find_contours(image, YELLOW[0], YELLOW[1])
        purple_contours = rc_utils.find_contours(image, PURPLE[0], PURPLE[1])
     
        if orange_contours:
            largest_orange_contour = rc_utils.get_largest_contour(orange_contours, MIN_CONTOUR_AREA)
    
            if largest_orange_contour is not None:
                contour_center = rc_utils.get_contour_center(largest_orange_contour)
                contour_area = rc_utils.get_contour_area(largest_orange_contour)
    
                # Functions from Lab F to draw contour onto the image
                rc_utils.draw_contour(image, largest_orange_contour)
                rc_utils.draw_circle(image, contour_center)
                cv.circle(image, (contour_center[1], contour_center[0]), 6, (0, 255, 255), -1)
    
        elif green_contours:
            largest_green_contour = rc_utils.get_largest_contour(green_contours, MIN_CONTOUR_AREA)
    
            if largest_green_contour is not None:
                contour_center = rc_utils.get_contour_center(largest_green_contour)
                contour_area = rc_utils.get_contour_area(largest_green_contour)
    
                # Functions from Lab F to draw contour onto the image
                rc_utils.draw_contour(image, largest_green_contour)
                rc_utils.draw_circle(image, contour_center)
                cv.circle(image, (contour_center[1], contour_center[0]), 6, (0, 255, 255), -1)
    
        elif red_contours:
            largest_red_contour = rc_utils.get_largest_contour(red_contours, MIN_CONTOUR_AREA)
    
            if largest_red_contour is not None:
                contour_center = rc_utils.get_contour_center(largest_red_contour)
                contour_area = rc_utils.get_contour_area(largest_red_contour)
    
                # Functions from Lab F to draw contour onto the image
                rc_utils.draw_contour(image, largest_red_contour)
                rc_utils.draw_circle(image, contour_center)
                cv.circle(image, (contour_center[1], contour_center[0]), 6, (0, 255, 255), -1)
    
        elif blue_contours:
            largest_blue_contour = rc_utils.get_largest_contour(blue_contours, MIN_CONTOUR_AREA)
    
            if largest_blue_contour is not None:
                contour_center = rc_utils.get_contour_center(largest_blue_contour)
                contour_area = rc_utils.get_contour_area(largest_blue_contour)
    
                # Functions from Lab F to draw contour onto the image
                rc_utils.draw_contour(image, largest_blue_contour)
                rc_utils.draw_circle(image, contour_center)
                cv.circle(image, (contour_center[1], contour_center[0]), 6, (0, 255, 255), -1)
    
        elif purple_contours:
            largest_purple_contour = rc_utils.get_largest_contour(purple_contours, MIN_CONTOUR_AREA)
    
            if largest_purple_contour is not None:
                contour_center = rc_utils.get_contour_center(largest_purple_contour)
                contour_area = rc_utils.get_contour_area(largest_purple_contour)
    
                # Functions from Lab F to draw contour onto the image
                rc_utils.draw_contour(image, largest_purple_contour)
                rc_utils.draw_circle(image, contour_center)
                cv.circle(image, (contour_center[1], contour_center[0]), 6, (0, 255, 255), -1)
    
        else:
            contour_center = None
            contour_area = 0

        # Display the image to the screen
        rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    #pass # Remove 'pass' and write your source code for the start() function here
    global speed
    global angle

    # Initialize variables
    speed = 0.25
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)


# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    #pass # Remove 'pass' and write your source code for the update() function here

    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global contour_center

    # Search for contours in the current color image
    update_contour()

    # Choose an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    if contour_center is not None:
        setpoint = rc.camera.get_width() // 2  # x=320

        # Retrieve the current x-axis position of the line from the array
        present_value = contour_center[1]

        # Define the proportional coefficient Kp:
        #Kp = -0.003125
        #Kp = -0.003
        Kp = -0.00285

        # Calculate the error signal e(t)
        error = setpoint - present_value 

        # Calculate the control signal u(t)
        angle = Kp * error

        # Clamp angle to prevent assertion error
        angle = rc_utils.clamp(angle, -1, 1)

        speed = 0.2

        if angle > -0.2 and angle < 0.2:
            rc.drive.set_max_speed(1)
    else:
        speed = 0
        angle = 0

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

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    #pass # Remove 'pass and write your source code for the update_slow() function here
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x-position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))
########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
