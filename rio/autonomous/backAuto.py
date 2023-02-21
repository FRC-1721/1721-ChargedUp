# commands2
import commands2

from commands2 import WaitCommand
from subsystems.drivesubsystem import DriveSubsystem


class BackAuto(commands2.SequentialCommandGroup):
    def __init__(self, driveSubsystem: DriveSubsystem, speedLeft, speedRight) -> None:
        """
        A manual drive backwards command
        """

        super().__init__(
            driveSubsystem.autoMovement(speedLeft, speedRight),
            WaitCommand(1),
        )
