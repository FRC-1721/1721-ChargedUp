import commands2

from commands.flybywire import FlyByWire

from subsystems.drivesubsystem import DriverStation


class Crawl(commands2.CommandBase):
    """
    Manually drives the arm subsystem to zero
    """

    def __init__(self, driveSubsystem, rot) -> None:
        super().__init__()

        self.driveSubsystem = driveSubsystem
        self.rot = rot

    def execute(self) -> None:
        FlyByWire(self.driveSubsystem, forward=0.3, rotation=self.rot)

    def end(self, interrupted: bool) -> None:
        pass
