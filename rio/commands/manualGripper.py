import commands2
import typing

from subsystems.clawsubsystem import ClawSubsystem


class ManualGripper(commands2.CommandBase):
    def __init__(
        self,
        clawSubsystem: ClawSubsystem,
        grabForce: typing.Callable[
            [],
            float,
        ],
        currentLimit: int = 3,
    ) -> None:
        """Manually operates the claw."""
        super().__init__()

        # Local instance of this subsystem
        self.clawSusystem = clawSubsystem
        # Requested grab force (-1 to 1)
        self.grabForce = grabForce

        # Require exclusive control of the claw
        self.addRequirements([self.clawSusystem])

        # Set the appropriate current limit
        self.clawSusystem.setCurrentlimit(currentLimit)

    def initialize(self) -> None:
        # Set the force
        self.clawSusystem.grab(self.grabForce())

    def end(self, interrupted: bool) -> None:
        # Stop setting the force
        self.clawSusystem.grab(0)
        return True
