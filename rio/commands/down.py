import commands2
import typing

from subsystems.armsubsystem import ArmSubsystem


class Down(commands2.CommandBase):
    def __init__(
        self, armsubsystem: ArmSubsystem, extendSpeed: typing.Callable[[], float]
    ) -> None:
        super().__init__()

        self.armsubsystem = armsubsystem
        self.extendSpeed = extendSpeed

        # this gives us full control of the claw
        self.addRequirements([self.armsubsystem])

    def initialize(self) -> None:
        self.armsubsystem.ascent(self.extendSpeed)

    def end(self, interrupted: bool) -> None:
        self.armsubsystem.ascent(self.extendSpeed)
        return True
