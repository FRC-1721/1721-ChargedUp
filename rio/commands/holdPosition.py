import typing
import commands2

import rev

from subsystems.drivesubsystem import DriveSubsystem


class HoldPosition(commands2.CommandBase):
    """
    Holds position using the embedded PID loops
    """

    def __init__(
        self,
        drivetrain: DriveSubsystem,
    ) -> None:
        super().__init__()

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain

        # Adding drivetrain as a requirement ensures no other command will interrupt us
        self.addRequirements([self.drivetrain])

        # Current rigth and left pos
        self.re = self.drivetrain.getRightEncoder().getPosition()
        self.le = self.drivetrain.getLeftEncoder().getPosition()

    def execute(self) -> None:
        self.drivetrain.rPID.setReference(
            self.re, rev.CANSparkMax.ControlType.kPosition
        )
        self.drivetrain.lPID.setReference(
            self.le, rev.CANSparkMax.ControlType.kPosition
        )

    def end(self, interrupted: bool) -> None:
        pass
