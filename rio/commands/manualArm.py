import typing
import commands2

from subsystems.armsubsystem import ArmSubsystem


class ManualArm(commands2.CommandBase):
    """
    ManualArm controls the arm using manual human
    controls only.
    """

    def __init__(
        self,
        armSubsystem: ArmSubsystem,
        # Power to the elevator (spool)
        elevatorPower: typing.Callable[
            [],
            float,
        ],
        # Power to the ladder (angle)
        ladderPower: typing.Callable[
            [],
            float,
        ],
    ) -> None:
        super().__init__()

        # Local instance of this subsystem
        self.armSusystem = armSubsystem

        # Requested powers
        self.elevatorPower = elevatorPower
        self.ladderPower = elevatorPower

        # Require exclusive control of this subsystem
        self.addRequirements([self.armSusystem])

    def execute(self) -> None:
        # Command both motors
        self.armSusystem.extension(self.elevatorPower)  # For the spool
        self.armSusystem.ascent(self.ladderPower)  # For the lead screw

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(0)
        self.armSusystem.ascent(0)
        return True
