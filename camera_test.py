#!/usr/bin/env python
"""
Script to experiment with OpenCV object detection using images from iphone camera
"""
from imutils import paths
import numpy as np
import imutils
import cv2


def main():
    """
    <Main Description>
    """
    # initialize the known distance from the camera to the object, which
    # in this case is 24 inches
    KNOWN_DISTANCE = 21.650
    # initialize the known object width, which in this case, the piece of
    # paper is 12 inches wide
    KNOWN_WIDTH = 11
    # load the furst image that contains an object that is KNOWN TO BE 2 feet
    # from our camera, then find the paper marker in the image, and initialize
    # the focal length
    image = cv2.imread("./images/img2.jpg")
    marker = find_marker(image)
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
    print(marker)
    # loop over the images
    for imagePath in sorted(paths.list_images("images")):
        # load the image, find the marker in the image, then compute the
        # distance to the marker from the camera
        image = cv2.imread(imagePath)
        marker = find_marker(image)
        circles = find_circle(image)
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        # draw a bounding box around the image and display it
        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.intp(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fft" % (inches / 12),
            (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
        cv2.imshow("image", image)
        cv2.waitKey(0)


def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray=cv2.medianBlur(gray,5)
    edged = cv2.Canny(gray, 25, 80)
    cv2.imshow("edged", edged)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c)

def find_circle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray=cv2.medianBlur(gray,5)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("gray", gray)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=20, maxRadius=80)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(image, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(image, center, radius, (255, 0, 255), 3)
    #check_colour(image, center[0], center[1])
    cv2.imshow("detected circles", image)
    cv2.waitKey(0)
def check_colour(image, x, y):
     print(image[x, y])

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth


if __name__ == '__main__':
    main()


