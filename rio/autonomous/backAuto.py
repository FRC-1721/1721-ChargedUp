import commands2

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.clawsubsystem import ClawSubsystem

from autonomous.flywithwire import FlyWithWires


class BackAuto(commands2.SequentialCommandGroup):
    def __init__(self, driveSubsystem: DriveSubsystem) -> None:
        """
        a 'simple' drive back command
        """

        super().__init__(
            FlyWithWires(driveSubsystem, fwd=-0.5, time=3),
        )
