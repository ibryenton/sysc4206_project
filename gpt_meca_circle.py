#!/usr/bin/env python
"""
Test script which interfaces with meca500 to navigate to red circle
"""

import pymeca
import cv2
import numpy as np

# Initialize robot connection
robot = pymeca.Meca500('192.168.0.100')

# Initialize camera
camera = cv2.VideoCapture(0)

# Set camera parameters
camera_focal_length = 2.8 # mm
camera_sensor_width = 5.7 # mm
camera_pixel_size = 0.0014 # mm

# Set known distance from camera to robot
robot_distance = 100 # mm

# Set target color (in BGR format)
target_color = (0, 0, 255)

while True:
    # Capture frame from camera
    ret, frame = camera.read()
    if not ret:
        break

    # Convert frame to grayscale and threshold to find red areas
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour matches the target color
    for cnt in contours:
        # Compute the center of the contour
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Check if the color at the center of the contour matches the target color
        color = frame[cy, cx]
        if tuple(color) == target_color:
            # Compute the distance to the object
            object_width_px = cv2.minEnclosingCircle(cnt)[1][0] * 2
            object_width_mm = object_width_px * camera_pixel_size
            object_distance_mm = (camera_focal_length * robot_distance) / (object_width_mm * camera_sensor_width)

            # Move the robot to the object
            robot.move([object_distance_mm, 0, 0, 0, 0, 0], 'absolute')

            # Draw a circle around the object
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

    # Show the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()




