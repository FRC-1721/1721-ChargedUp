# A test autonomous, utilizing pathplanner to cross the line.


import wpilib
import commands2
import commands2.cmd

from wpimath.controller import (
    RamseteController,
    PIDController,
    SimpleMotorFeedforwardMeters,
)


from wpimath.geometry import Pose2d, Rotation2d

from wpimath.geometry import Pose2d, Rotation2d

from pathplannerlib import loadPath

from subsystems.drivesubsystem import DriveSubsystem

from constants.constants import getConstants


class CrossLinePath(commands2.RamseteCommand):
    """A command that uss a ramsete controller to follow a preset path."""

    def __init__(self, drive: DriveSubsystem) -> None:
        # get const here

        trajectory = loadPath("paths/New Path.path")

        _pose = Pose2d(3, 0, Rotation2d(0))

        # super().__init__(
        #     trajectory=trajectory,
        #     _pose,
        #     RamseteController(1, 1),
        #     SimpleMotorFeedforwardMeters(
        #         constants.ksVolts,
        #         constants.kvVoltSecondsPerMeter,
        #         constants.kaVoltSecondsSquaredPerMeter,
        #     ),
        #     # Our drive kinematics.
        #     constants.kDriveKinematics,
        #     # A reference to a method which will return a DifferentialDriveWheelSpeeds object.
        #     self.robotDrive.getWheelSpeeds,
        #     # The turn controller for the left side of the drivetrain.
        #     PIDController(constants.kPDriveVel, 0, 0),
        #     # The turn controller for the right side of the drivetrain.
        #     PIDController(constants.kPDriveVel, 0, 0),
        #     # A reference to a method which will set a specified
        #     # voltage to each motor. The command will pass the two parameters.
        #     self.robotDrive.tankDriveVolts,
        #     # The subsystems the command should require.
        #     [self.robotDrive],
        # )
