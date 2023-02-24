import typing
import commands2

import rev

from subsystems.drivesubsystem import DriveSubsystem


class HoldPosition(commands2.CommandBase):
    """
    Holds position using the embedded PID loops
    TODO fix, this currently works because it uses
    wpilibs motors saftey feature. I leave this here
    because it spits our an error when doing so.
    """

    def __init__(
        self,
        drivetrain: DriveSubsystem,
    ) -> None:
        super().__init__()

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain

        # Adding drivetrain as a requirement ensures no other command will interrupt us
        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        # This needs to be here so it will not
        # spin if you go into it with momentiun
        self.re = self.drivetrain.getRightEncoder().getPosition()  # current left POS
        self.le = self.drivetrain.getLeftEncoder().getPosition()  # current right POS

        self.drivetrain.rPID.setReference(
            self.re, rev.CANSparkMax.ControlType.kPosition
        )
        self.drivetrain.lPID.setReference(
            self.le, rev.CANSparkMax.ControlType.kPosition
        )
        commands2.WaitCommand(0.005)

    def end(self, interrupted: bool) -> None:
        pass
