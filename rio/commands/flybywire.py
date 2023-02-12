import typing
import commands2
from subsystems.drivesubsystem import DriveSubsystem


class FlyByWire(commands2.CommandBase):
    """
    FlyByWire uses pure joystick inputs
    to direct the robot. Tradionally, this
    is the most direct way to command the robot."""

    def __init__(
        self,
        drivetrain: DriveSubsystem,
        forward: typing.Callable[[], float],
        rotation: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain
        self.forward = forward  # Forward command
        self.rotation = rotation  # Rotation command

        # Adding drivetrain as a requirement ensures no other command will interrupt us
        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        self.drivetrain.arcadeDrive(
            self.exponential_dampen(self.forward()) * -1,
            self.piecewise_dampen(self.rotation()),
        )

    def exponential_dampen(self, x):
        """
        Uses a simple math function
        to dampen the user input.
        """

        return x / 1.3 * -1

    def piecewise_dampen(self, x):
        """
        Uses multiple different equations to define
        a dampened user input
        """

        x = x * -1  # invert

        if abs(x) < 0.9:
            return x / 2
        else:
            return x
        # return x * -1
