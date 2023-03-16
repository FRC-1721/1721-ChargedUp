from commands.turntoangle import TurnToAngle

from ntcore import NetworkTableInstance

from subsystems.drivesubsystem import DriveSubsystem

from wpilib import RobotBase

import commands2
import json


class limeLightCommands(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem, TagID=None) -> None:
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.ll = self.nt.getTable("limelight-gabriel")
        self.botPos = 0
        self.drivesys = drive
        self.targetID = TagID
        # Load map
        mapPath = "deploy/maps/frc2023.fmap"
        if RobotBase.isReal():
            mapPath = "/home/lvuser/py/deploy/maps/frc2023.fmap"

        # self.map = json.load(open(mapPath, "r"))  # Load fmap file

    def execute(self) -> None:
        aprilTag = (
            self.getTag()
        )  # uses nt tables to try to retreive info about an apriltag
        if (
            type(aprilTag) is list and len(aprilTag) >= 6
        ):  # checks tif the apriltag is a list and has the correct amount of values
            print(aprilTag, "asdfasdfasdf")
            distX = aprilTag[0]  # x linear offset of apriltag and robot
            distY = aprilTag[1]  # y linear offset of apriltag and robot
            rotZ = aprilTag[5]  # z rotational offset of apriltag and robot

            # due to the camera not being able to capture the tag in a
            # stable manner as well as how it handles rotation, this
            # checks whether the z rot offset is negative or positive
            # and converts it into a better value
            if rotZ > 0:
                rotZ -= 180
            else:
                rotZ += 180

            # sets a default speed and rotational speed value
            movespeed = 0
            rotSpeed = 0

            print("Z: " + str(rotZ))
            print("Y: " + str(distY))

            # checks the angle offset of the robot and decides whether it should go straight forward or start turning
            if -5 < rotZ < 5:
                # checks how far away from the apriltag the robot is and sets speed accordingly
                if distX >= -4:
                    movespeed = 0.8  # needs to be adjusted
                elif distX >= -5:
                    movespeed = 0.6
                elif distX >= -6:
                    movespeed = 0.4

            elif -20 < rotZ < 20:
                if rotZ > 0:
                    rotSpeed = 0.25
                elif rotZ < 0:
                    rotSpeed = -0.25
            print("movespeed: " + str(movespeed))
            # drive the robot based on values
            self.drivesys.arcadeDrive(movespeed, rotSpeed)
        else:
            if aprilTag <= 0:
                print("no apriltag found!")
            elif aprilTag == 1:
                print("error while getting position of aprilTag")

    def getTag(self):
        """
        Tries to get any apriltag in view of limelight. returns 0 if no apriltag is found.
        If A Number is passed into ID, The limelight will only look for apriltags of that ID
        """
        # gets the tagID from ntables
        tagID = self.ll.getEntry("tid").getDouble(0)

        # checks if targetID has been set and if it has, checks to make sure that it has the right ID
        if self.targetID == None ^ tagID == self.targetID:
            print(tagID, "a")
            if 0 < tagID <= 8:
                tagPos = self.ll.getEntry("botpose").getDoubleArray(1)
                return tagPos
            # self.map["fiducials"][tagID - 1]["transform"] = tagPos
            return tagID
