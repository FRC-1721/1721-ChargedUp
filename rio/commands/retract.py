import commands2
import typing

from subsystems.armsubsystem import ArmSubsystem


class Retract(commands2.CommandBase):
    def __init__(self, armSubsystem: ArmSubsystem, power=-1) -> None:
        super().__init__()
        """This pulls the spool in"""

        self.armSusystem = armSubsystem
        self.power = power

        # this gives us full control of the arm
        self.addRequirements([self.armSusystem])

        # TODO Change me
        self.armSusystem.setCurrentlimit(8)

    def execute(self) -> None:
        self.armSusystem.extension(self.power)

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(0)
        return True
