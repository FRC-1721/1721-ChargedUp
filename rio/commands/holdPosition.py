import typing
import commands2

import rev

from wpimath.controller import PIDController

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

        self.re = self.drivetrain.getRightEncoder().getPosition()  # current left POS
        self.le = self.drivetrain.getLeftEncoder().getPosition()  # current right POS

        self.rPID = PIDController(0.6, 0.01, 1.0)
        self.lPID = PIDController(0.6, 0.01, 1.0)

    def execute(self) -> None:
        # This needs to be here so it will not
        # spin if you go into it with momentiun
        # self.drivetrain.leftMotors.

        print(
            f"Right target is {self.re} error pos is {self.rPID.getPositionError()} Output is: {-self.rPID.calculate(self.drivetrain.getRightEncoder().getPosition(),self.re)}"
        )

        # print(f"Left target is {self.le} error pos is {self.lPID.getPositionError()}")

        self.drivetrain.tankDriveVolts(
            -self.rPID.calculate(
                self.drivetrain.getRightEncoder().getPosition(),
                self.re,
            ),
            self.lPID.calculate(
                self.drivetrain.getLeftEncoder().getPosition(),
                self.le,
            ),
        )

        # Its ok! We're updating the motors
        self.drivetrain.drive.feed()

    def end(self, interrupted: bool) -> None:
        pass
