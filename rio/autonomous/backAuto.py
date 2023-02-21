# commands2
import commands2

from commands2 import WaitCommand
from subsystems.drivesubsystem import DriveSubsystem


class BackAuto(commands2.SequentialCommandGroup):
    def __init__(self, driveSubsystem: DriveSubsystem) -> None:
        """
        A manual drive backwards command
        """

        super().__init__(
            # driveSubsystem.motorDrive(0.25, 0.25),
            WaitCommand(1),
        )
