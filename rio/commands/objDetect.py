from ntcore import NetworkTableInstance

from subsystems.drivesubsystem import DriveSubsystem

from wpilib import RobotBase

import commands2
import json


class limeLightDetector(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.ll = self.nt.getTable("limelight-rotom")
        self.drivesys = drive

    def execute(self) -> None:
        posX = self.ll.getEntry("tx").getDouble(0)
        posY = self.ll.getEntry("ty").getDouble(0)
        if posX <= -4:
            movespeed = 0.8  # needs to be adjusted
        elif posX <= -3:
            movespeed = 0.6
        elif posX <= -2:
            movespeed = 0.4

        if posY > 0.5:
            rotspeed = 1

        if posY < -0.5:
            rotspeed = -1

        self.drivesys.arcadeDrive(movespeed, rotspeed)
