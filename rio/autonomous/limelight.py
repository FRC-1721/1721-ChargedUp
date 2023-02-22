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
        self.ll = self.nt.getTable("limelight")
        self.botPos = 0
        self.drivesys = drive
        # Load map
        mapPath = "deploy/maps/frc2023.fmap"
        if RobotBase.isReal():
            mapPath = "/home/lvuser/py/deploy/maps/frc2023.fmap"

        # self.map = json.load(open(mapPath, "r"))  # Load fmap file

    def execute(self) -> None:
        aprilTag = self.getTag()
        if aprilTag != None:
            distX = aprilTag[0]
            DistY = aprilTag[1]
            rotZ = aprilTag[5]
            if distX > 10:
                self.drivesys.arcadeDrive(10, 0)  # needs to be adjusted
            if DistY > 0:
                self.drivesys.arcadeDrive(10, 20)  # needs to be adjusted
            elif DistY < 0:
                self.drivesys.arcadeDrive(10, -20)  # needs to be adjusted
            elif rotZ != 0:
                TurnToAngle(rotZ, self.drivesys)  # prbably doesn't work
        else:
            print("no apriltag found!")

    def getTag(self):
        """
        Tries to get any apriltag in view of limelight. returns 0 if no apriltag is found.
        If A Number is passed into ID, The limelight will only look for apriltags of that ID
        """

        tagID = self.ll.getEntry("tid").getDouble(0)
        tagPos = self.ll.getEntry("targetpose_robotspace").getDoubleArray(0)
        # self.map["fiducials"][tagID - 1]["transform"] = tagPos
        return tagPos

    def getBotPos(self):
        pos = self.ll.getEntry("botpose_targetspace").getType()
        return pos

    def autoBotDrive(self):
        self.botPos = self.getBotPos()
        if self.botPos != 0:
            TurnToAngle(6, self.drivesys)
