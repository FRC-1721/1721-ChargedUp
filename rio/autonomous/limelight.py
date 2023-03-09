from commands.turntoangle import TurnToAngle

from ntcore import NetworkTableInstance

from subsystems.drivesubsystem import DriveSubsystem

from wpilib import RobotBase

import commands2
import json


class limeLightCommands(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.ll = self.nt.getTable("limelight-gabriel")
        self.botPos = 0
        self.drivesys = drive
        # Load map
        mapPath = "deploy/maps/frc2023.fmap"
        if RobotBase.isReal():
            mapPath = "/home/lvuser/py/deploy/maps/frc2023.fmap"

        # self.map = json.load(open(mapPath, "r"))  # Load fmap file

    def execute(self) -> None:
        aprilTag = self.getTag()
        if type(aprilTag) is list and len(aprilTag) >= 6:
            print(aprilTag, "asdfasdfasdf")
            distX = aprilTag[0]
            distY = aprilTag[1] - 180
            rotZ = aprilTag[5]
            if -2.5 < rotZ < 2.5:
                if distX >= -4:
                    self.drivesys.arcadeDrive(0.5, 0)  # needs to be adjusted
                elif distX >= -5:
                    self.drivesys.arcadeDrive(0.35, 0)  # needs to be adjusted
                elif distX >= -6:
                    self.drivesys.arcadeDrive(0.2, 0)  # needs to be adjusted

                    # if distY > 0:
                    # self.drivesys.arcadeDrive(10, 20)  # needs to be adjusted
                    # elif distY < 0:
                    # self.drivesys.arcadeDrive(10, -20)  # needs to be adjusted
            else:
                TurnToAngle(rotZ - 180, self.drivesys)  # prbably doesn't work
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

        tagID = self.ll.getEntry("tid").getDouble(0)
        print(tagID, "a")
        if 0 < tagID <= 8:
            tagPos = self.ll.getEntry("botpose").getDoubleArray(1)
            return tagPos
        # self.map["fiducials"][tagID - 1]["transform"] = tagPos
        return tagID

    def getBotPos(self):
        pos = self.ll.getEntry("botpose_targetspace").getType()
        return pos

    def autoBotDrive(self):
        self.botPos = self.getBotPos()
        if self.botPos != 0:
            TurnToAngle(6, self.drivesys)
