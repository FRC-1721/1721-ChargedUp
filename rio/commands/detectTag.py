import apriltag
import cv2
import commands2

# is this where this file should go?
class detectTag(commands2.CommandBase):  #
    def __init__(self) -> None:
        super().__init__()
        # stuff will go here

    def getCapture():
        pass
        # will maybe be used to get the capture s it can be used in tagInfo()

    def tagInfo(image):
        img = cv2.imread(
            image, cv2.IMREAD_GRAYSCALE
        )  # image is your import, I'm not sure how to get the video on the robot, but i'm guessing a snapshot should be taken at set intervals and fed into image
        detector = apriltag.Detector()
        result = detector.detect(img)
        return result
