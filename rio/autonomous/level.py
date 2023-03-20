import commands2
import wpilib

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.armsubsystem import ArmSubsystem

from commands.presetArm import PresetArm
from autonomous.flywithwire import FlyWithWires


class Level(commands2.CommandBase):
    def __init__(
        self, drive: DriveSubsystem, arm=ArmSubsystem, fwd=0, rot=0, time=-1
    ) -> None:
        super().__init__()

        self.drive = drive
        self.arm = arm

        # time and derection vars
        self.time = time
        self.fwd = fwd
        self.rot = rot

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        PresetArm(self.arm, lambda: 0, lambda: 0, 82, 163),
        if self.drive.getPitch() != 89:
            FlyWithWires(self.drive, self.fwd, self.rot, self.time)

        elif self.drive.getPitch() != 91:
            FlyWithWires(self.drive, self.fwd * -1, self.rot, self.time)

        else:
            FlyWithWires(self.drive, 0, 0, 0)

    def end(self, interrupted: bool) -> None:
        self.drive.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return True
