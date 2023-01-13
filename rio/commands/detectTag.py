import apriltag
import cv2 as cv
import numpy as np

cam = cv.VideoCapture(0)


def getCapture():

    ret, cap = cam.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
    else:
        cv.imwrite("snap.png", cap)


def tagInfo():
    # Just adding this real quick so people don't get confused by the return values.
    # tag_family: represents a bunch of stupid stuff we don't really need to know. the apriltags this season will be 16h5
    # tag_id: each tag family has a different number of unique ID's. unlike tag family, this is REALLY important.
    # homography: 3x3 2d array of something? Hopefully someone understands homography but I think we can work around it for now
    # center: the x & y values of the center point of the tag. don't know what it's being measured in though
    # corners: 2x4 2d array, the x & y values of each of the 4 corners of the tag

    # Max detection distance in meters = t /(2 * tan( (b* f * p) / (2 * r ) ) )
    # t = size of your tag in meters - Optitag calls this Edge Length or size
    # b = the number of bits that span the width of the tag (excluding the white border for Apriltag 2). ex: 36h11 = 8, 25h9 = 6, standard41h12 = 9
    # f = horizontal FOV of your camera
    # r = horizontal resolution of you camera
    # p = the number of pixels required to detect a bit. This is an adjustable constant. We recommend 5. Lowest number we recommend is 2 which is the Nyquist Frequency. We recommend 5 to avoid some of the detection pitfalls mentioned above.

    # more info here https://optitag.io/blogs/news/designing-your-perfect-apriltag
    getCapture()
    img = cv.imread(
        "snap.png", cv.IMREAD_GRAYSCALE  # NEEDS TO BE GRAYSCALED VIA THIS COMMAND
    )  # image is your import, I'm not sure how to get the video on the robot, but i'm guessing a snapshot should be taken at set intervals and fed into image
    options = apriltag.DetectorOptions(
        families="tag16h5",
    )
    detector = apriltag.Detector()  # this is the object that detetcts the tag
    result = detector.detect(img)  # this is the method that does the detection
    return result


while True:
    info = tagInfo()
    if info:
        print(info)
