import apriltag
import cv2 as cv
import commands2

# is this where this file should go?
class detectTag(commands2.CommandBase):
    def __init__(self) -> None:
        super().__init__()
        # stuff will go here

    def getCapture(self):
        cam = cv.VideoCapture(0)
        capture = cam.read()
        return capture

    def tagInfo(self):
        image = self.getCapture()
        img = cv.imread(
            image, cv.IMREAD_GRAYSCALE  # NEEDS TO BE GRAYSCALED VIA THIS COMMAND
        )  # image is your import, I'm not sure how to get the video on the robot, but i'm guessing a snapshot should be taken at set intervals and fed into image
        detector = apriltag.Detector()  # this is the object that detetcts the tag
        result = detector.detect(img)  # this is the method that does the detection
        return result
