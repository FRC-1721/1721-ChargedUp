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
        targetElevator=0,
        targetLadder=261,
    ) -> None:
        super().__init__()

        # Local instance of this subsystem
        self.armSusystem = armSubsystem

        # Fine Control
        self.elevatorFineControl = elevFine
        self.ladderFineControl = laddFine

        # General target
        self.targElev = targetElevator
        self.targLadd = targetLadder

        # Require exclusive control of this subsystem
        self.addRequirements([self.armSusystem])

    def execute(self) -> None:
        # Command both motors
        # self.armSusystem.extension(self.elevatorPower())  # For the spool
        # self.armSusystem.ascent(self.elevatorFineControl())  # For the lead screw
        self.armSusystem.gotoPosition(
            self.targElev + (self.elevatorFineControl() * 10),
            self.targLadd + (self.ladderFineControl() * 20),
        )

    def end(self, interrupted: bool) -> None:
        self.armSusystem.extension(0)
        self.armSusystem.ascent(0)
        return True
