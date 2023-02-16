import commands2
import typing

from subsystems.armsubsystem import ArmSubsystem


class Extend(commands2.CommandBase):
    def __init__(
        self, armSubsystem: ArmSubsystem, extendSpeed: typing.Callable[[], float]
    ) -> None:
        super().__init__()

        self.armSusystem = armSubsystem
        self.extendSpeed = extendSpeed

        # this gives us full control of the arm
        self.addRequirements([self.armSusystem])

        # TODO Change me
        self.armSusystem.setCurrentlimit(1)

    def initialize(self) -> None:
        self.armSusystem.extension(self.extendSpeed)

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(self.extendSpeed)
        return True
