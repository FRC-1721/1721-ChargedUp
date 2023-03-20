# Import the camera server
from cscore import CameraServer

# Import OpenCV and NumPy
import cv2
import numpy as np
import commands2


class globDetect(commands2.CommandBase):
    def __init__(self) -> None:
        self.cone_lower = np.array([25, 52, 72], np.uint8)
        self.cone_upper = np.array([102, 255, 255], np.uint8)
        super().__init__()

    def camSetup(self):
        cs = CameraServer.getInstance()
        cs.enableLogging()

        # Capture from the first USB Camera on the system
        camera = cs.startAutomaticCapture()
        camera.setResolution(320, 240)

        # Get a CvSink. This will capture images from the camera
        cvSink = cs.getVideo()

        # (optional) Setup a CvSource. This will send images back to the Dashboard
        outputStream = cs.putVideo("globDetect", 320, 240)

        # Allocating new images is very expensive, always try to preallocate
        img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

        while True:
            # Tell the CvSink to grab a frame from the camera and put it
            # in the source image.  If there is an error notify the output.
            time, img = cvSink.grabFrame(img)
            if time == 0:
                # Send the output the error.
                outputStream.notifyError(cvSink.getError())
                # skip the rest of the current iteration
                continue
            hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            cone_mask = cv2.inRange(hsvFrame, self.cone_lower, self.green_upper)

            contours, hierarchy = cv2.findContours(
                cone_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 300:
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(
                        imageFrame, (x, y), (x + w, y + h), (255, 165, 0), 2
                    )

                    cv2.putText(
                        imageFrame,
                        "Cone",
                        (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 0, 0),
                    )
