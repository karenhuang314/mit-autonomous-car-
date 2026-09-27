# mit-autonomous-car-
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
