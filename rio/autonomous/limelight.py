from ntcore import NetworkTableInstance

from wpilib import RobotBase

import commands2
import json


class limeLightCommands(commands2.CommandBase):
    def __init__(self) -> None:
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.ll = self.nt.getTable("limelight")

        # Load map
        mapPath = "deploy/maps/frc2023.fmap"
        if RobotBase.isReal():
            mapPath = "/home/lvuser/py/deploy/maps/frc2023.fmap"

        self.map = json.load(open(mapPath, "r"))  # Load fmap file

    def getTag(self):
        """Tries to get any apriltag in view of limelight. returns 0 if no apriltag is found."""
        tagID = self.table.getEntry("tid").getDouble(0)
        tagPos = self.table.getEntry("targetpose_robotspace").getDoubleArray(0)
        self.map["fiducials"][tagID - 1]["transform"] = tagPos
        return tagPos

    def getBotPos(self):
        pos = self.table.getEntry("botpose_targetspace").getDoubleArray(0)
        return pos
