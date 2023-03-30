import cv2
import numpy as np

# Initialize camera
camera = cv2.VideoCapture(1)


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
        actual_diameter = 10  # actual diameter of the red circle in mm
        pixel_diameter = max_radius*2  # diameter of the red circle in pixels
        print(pixel_diameter)
        distance = (actual_diameter * focal_length) / pixel_diameter

        # Print the distance
        print(f"Distance: {distance:.2f} mm")
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break