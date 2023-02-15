# A test autonomous, utilizing pathplanner to cross the line.

import commands2
import commands2.cmd

from wpimath.controller import (
    RamseteController,
    PIDController,
    SimpleMotorFeedforwardMeters,
)
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveKinematics

from pathplannerlib import PathPlanner, PathConstraints

from subsystems.drivesubsystem import DriveSubsystem

from constants.constants import getConstants


class CrossLinePath(commands2.RamseteCommand):
    """A command that uses a ramsete controller to follow a preset path."""

    def __init__(self, drive: DriveSubsystem) -> None:
        const = getConstants("robot_autonomous")
        driveKinematics = DifferentialDriveKinematics(const["kTrackWidthMeters"])

        constraints = PathConstraints(0.5, 0.1)
        trajectory = PathPlanner.loadPath("New New Path", constraints, reversed=False)

        super().__init__(
            trajectory.asWPILibTrajectory(),
            drive.getPose,
            RamseteController(
                const["kRamseteB"],
                const["kRamseteZeta"],
            ),
            SimpleMotorFeedforwardMeters(
                const["ksVolts"],
                const["kvVoltSecondsPerMeter"],
                const["kaVoltSecondsSquaredPerMeter"],
            ),
            # Our drive kinematics.
            driveKinematics,
            # A reference to a method which will return a DifferentialDriveWheelSpeeds object.
            drive.getWheelSpeeds,
            # The turn controller for the left side of the drivetrain.
            PIDController(const["kRamP"], const["kRamI"], const["kRamD"]),
            # The turn controller for the right side of the drivetrain.
            PIDController(const["kRamP"], const["kRamI"], const["kRamD"]),
            # A reference to a method which will set a specified
            # voltage to each motor. The command will pass the two parameters.
            drive.tankDriveVolts,
            # The subsystems the command should require.
            [drive],
        )
