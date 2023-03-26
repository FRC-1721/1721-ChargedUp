from ntcore import NetworkTableInstance

from subsystems.drivesubsystem import DriveSubsystem

from wpilib import RobotBase
from numpy import *
import commands2
import json


class limeLightDetector(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.ll = self.nt.getTable("limelight-rotom")
        self.drivesys = drive
        self.movespeed = 0
        self.rotspeed = 0
        self.xFifo = array([0] * 10)
        self.yFifo = array([0] * 10)

    def execute(self) -> None:
        posX = self.ll.getEntry("tx").getDouble(0)
        append(self.xFifo, posX)
        delete(self.xFifo, 0)

        posY = self.ll.getEntry("ty").getDouble(0)
        append(self.yFifo, posY)
        delete(self.yFifo, 0)

        meanX = mean(posX)
        meanY = mean(posY)

        if meanY > 0.5:
            self.movespeed = 0.6
        else:
            self.movespeed = 0

        if meanX > 0.5:
            self.rotspeed = 0.5

        elif meanX < -0.5:
            self.rotspeed = -0.5

        else:
            self.rotspeed = 0

        self.drivesys.arcadeDrive(self.movespeed, self.rotspeed)
