import commands2
import typing

from subsystems.clawsubsystem import ClawSubsystem


class Clamp(commands2.CommandBase):
    def __init__(
        self, clawSubsystem: ClawSubsystem, grabSpeed: typing.Callable[[], float]
    ) -> None:
        super().__init__()

        self.clawSusystem = clawSubsystem
        self.grabSpeed = grabSpeed

        # this gives us full control of the claw
        self.addRequirements([self.clawSusystem])

        # TODO Change me
        self.clawSusystem.setCurrentlimit(3)

    def initialize(self) -> None:
        self.clawSusystem.grab(self.grabSpeed)

    def end(self, interrupted: bool) -> None:
        self.clawSusystem.grab(self.grabSpeed)
        return True
