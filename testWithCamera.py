#!/usr/bin/env python
import cv2
import numpy as np
from rich.traceback import install
from meca_coordinates import Meca

install()
# Initialize camera

def main():
    camera = cv2.VideoCapture(0)
    meca = Meca()

    while True:
        # Capture frame from camera
        ret, frame = camera.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply threshold to isolate red color
        low_red = np.array([0, 0, 180])
        high_red = np.array([100, 100, 255])
        mask = cv2.inRange(frame, low_red, high_red)

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
            cv2.circle(frame, max_center, int(max_radius), (0, 255, 0), 2)

        # Find the centroid of the largest contour
        if max_contour is not None:
            moments = cv2.moments(max_contour)
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
        # Draw a green circle around the red circle area
            # Draw a circle at the centroid
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Calculate distance from camera
            focal_length = 500  # iPhone X focal length in mm
            actual_diameter = 15  # actual diameter of the red circle in mm
            pixel_diameter = max_radius*2  # diameter of the red circle in pixels
            print(pixel_diameter)
            distance = (actual_diameter * focal_length) / pixel_diameter
            d_cx = (25/62)*((1980/2)-cx)
            d_cy = (25/62)*((1080/2)-cy)
            print(f'[bold red] x: in p{cx} {d_cx} y:{cy} {d_cy}')


            # Print the distance
            print(f"Distance: {distance:.2f} mm")
            cv2.imshow('frame', frame)
            cv2.imwrite('frame.jpg', frame)
            mx, my, mz, _ = meca.meca_coordinates(d_cx, d_cy, distance)
            meca.robot.MovePose(mx, my, mz, 0, 90, 0)
            #meca.get_joints()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()


