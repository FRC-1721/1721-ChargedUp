import commands2
import typing

from subsystems.armsubsystem import ArmSubsystem


class Extend(commands2.CommandBase):
    def __init__(self, armSubsystem: ArmSubsystem) -> None:
        super().__init__()
        """Pushes the arm back out"""

        self.armSusystem = armSubsystem

        # this gives us full control of the arm
        self.addRequirements([self.armSusystem])

        # TODO Change me
        self.armSusystem.setCurrentlimit(1)

    def initialize(self) -> None:
        self.armSusystem.extension(1)  # this is required otherwise it breaks everything

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(0)
        return True
