import commands2
import wpilib

from subsystems.drivesubsystem import DriveSubsystem


class FlyWithWires(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem, fwd=0, rot=0, time=-1) -> None:
        super().__init__()

        self.drive = drive

        # time and derection vars
        self.time = time
        self.fwd = fwd
        self.rot = rot

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.backgroundTimer.reset()

    def execute(self) -> None:
        self.drive.arcadeDrive(
            self.fwd,
            self.rot,
        )

    def end(self, interrupted: bool) -> None:
        self.drive.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        if self.time != -1 and self.backgroundTimer.hasElapsed(self.time):
            return True
