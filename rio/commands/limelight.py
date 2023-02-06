from networktables import NetworkTables as NT
import wpilib
import commands2


class limeLight(commands2.Command):
    def __init__(self) -> None:
        self.tables = NT.getTable("limelight")  # info we recieve from the limelight
        self.map = map = open("/frc2023.fmap", "r")  # fmap file

    def getTag(self):
        Id = "No Id found"
        tagID = self.tables.getEntry("tid").getString(Id)
        return tagID

    def getBotPos(self):
        Pos = "No Id Found"
        tagID = self.tables.getEntry("botpose_targetspace").getString(Pos)
        return tagID
