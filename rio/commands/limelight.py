from networktables import NetworkTables as NT
import wpilib
import commands2
import json


class limeLight(commands2.Command):
    def __init__(self) -> None:
        self.table = NT.getTable("limelight")  # info we recieve from the limelight
        self.map = json.load(open("/frc2023.fmap", "r"))  # fmap file

    def getTag(self):
        """Tries to get any apriltag in view of limelight. returns 0 if no apriltag is found."""
        tagID = self.table.getEntry("tid").getDouble(0)
        tagPos = self.table.getEntry("targetpose_robotspace").getDoubleArray(0)
        self.map["fiducials"][tagID - 1]["transform"] = tagPos
        return tagPos

    def getBotPos(self):
        pos = self.table.getEntry("botpose_targetspace").getDoubleArray(0)
        return pos
