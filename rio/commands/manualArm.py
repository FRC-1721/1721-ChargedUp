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
        elevFine: typing.Callable[
            [],
            float,
        ],
        # Power to the ladder (angle)
        laddFine: typing.Callable[
            [],
            float,
        ],
    ) -> None:
        super().__init__()

        # Local instance of this subsystem
        self.armSusystem = armSubsystem

        # Fine Control
        self.elevatorFineControl = elevFine
        self.ladderFineControl = laddFine

        # Require exclusive control of this subsystem
        self.addRequirements([self.armSusystem])

    def execute(self) -> None:
        # Command both motors
        self.armSusystem.extension(
            self.deadZone(self.elevatorFineControl(), 0.1)
        )  # For the spool

        self.armSusystem.ascent(
            self.deadZone(self.ladderFineControl(), 0.1)
        )  # For the lead screw

    def deadZone(self, input, zone):
        if abs(input) > zone:
            return input
        else:
            return 0

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(0)
        self.armSusystem.ascent(0)
        return True
