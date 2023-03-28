#!/usr/bin/env python
"""
Testing chatgpt script for red circle recognition
"""
import cv2
import numpy as np
import math

# Load the image
img = cv2.imread('images/red3.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply threshold to isolate red color
low_red = np.array([0, 0, 180])
high_red = np.array([100, 100, 255])
mask = cv2.inRange(img, low_red, high_red)

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Find the contour with the largest area
max_area = 0
max_contour = None
max_radius = 0
max_center = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        max_contour = contour
    (x, y), radius = cv2.minEnclosingCircle(contour)
    if radius > max_radius:
        max_radius = radius
        max_center = (int(x), int(y))

# Draw a green circle around the red circle area
if max_center is not None:
    cv2.circle(img, max_center, int(max_radius), (0, 255, 0), 2)

# Find the centroid of the largest contour
if max_contour is not None:
    moments = cv2.moments(max_contour)
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])
# Draw a green circle around the red circle area
    # Draw a circle at the centroid
    cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)

    # Calculate distance from camera
    focal_length = 3.99  # iPhone X focal length in mm
    actual_diameter = 30  # actual diameter of the red circle in mm
    pixel_diameter = 50  # diameter of the red circle in pixels
    distance = (actual_diameter * focal_length) / pixel_diameter

    # Print the distance
    print(f"Distance: {distance:.2f} mm")

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

