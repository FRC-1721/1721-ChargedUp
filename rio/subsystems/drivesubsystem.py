# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2
import math
import logging

from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds
from ntcore import NetworkTableInstance
from wpilib import DriverStation

# Constants
from constants.constants import getConstants

# Vendor Libs
from rev import CANSparkMax, CANSparkMaxLowLevel
from ctre import Pigeon2
from wpimath import geometry
from navx import AHRS


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.sd = self.nt.getTable("SmartDashboard")

        # network tables
        self.nt = NetworkTableInstance.getDefault()
        self.sd = self.nt.getTable("SmartDashboard")

        # Get hardware constants
        constants = getConstants("robot_hardware")  # All the robot hardware consts
        self.driveConst = constants["drivetrain"]  # All the drivetrain consts
        self.leftCosnt = self.driveConst["leftMotor"]  # Left specific
        self.rightCosnt = self.driveConst["rightMotor"]  # Right specific
        self.navXConst = self.driveConst["navX"]  # navX's constants

        # The motors on the left side of the drive.
        self.leftMotor1 = CANSparkMax(
            self.leftCosnt["Motor1Port"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )
        self.leftMotor2 = CANSparkMax(
            self.leftCosnt["Motor2Port"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Combine left motors into one group
        self.leftMotors = wpilib.MotorControllerGroup(
            self.leftMotor1,
            self.leftMotor2,
        )
        self.leftMotors.setInverted(self.leftCosnt["Inverted"])

        # The motors on the right side of the drive.
        self.rightMotor1 = CANSparkMax(
            self.rightCosnt["Motor1Port"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )
        self.rightMotor2 = CANSparkMax(
            self.rightCosnt["Motor2Port"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Combine left motors into one group
        self.rightMotors = wpilib.MotorControllerGroup(
            self.rightMotor1,
            self.rightMotor2,
        )
        self.rightMotors.setInverted(self.rightCosnt["Inverted"])
        # self.rightMotors.setInverted(False)

        # This fixes a bug in rev firmware involving flash settings.
        self.leftMotor1.setInverted(False)
        self.leftMotor2.setInverted(False)
        self.rightMotor1.setInverted(False)
        self.rightMotor2.setInverted(False)

        # The robot's drivetrain kinematics
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

        # The left-side drive encoder
        self.leftEncoder = self.leftMotor1.getEncoder()

        # The right-side drive encoder
        self.rightEncoder = self.rightMotor1.getEncoder()

        # Setup the conversion factors for the motor controllers
        # TODO: Because rev is rev, there are a lot of problems that need to be addressed.
        # https://www.chiefdelphi.com/t/spark-max-encoder-setpositionconversionfactor-not-doing-anything/396629
        self.leftEncoder.setPositionConversionFactor(
            1 / self.driveConst["encoderConversionFactor"]
        )
        self.rightEncoder.setPositionConversionFactor(
            1 / self.driveConst["encoderConversionFactor"]
        )

        # Gyro
        self.ahrs = AHRS.create_spi()  # creates navx object

        # Robot odometry
        self.odometry = DifferentialDriveOdometry(
            self.ahrs.getRotation2d(),
            self.leftEncoder.getPosition(),
            self.rightEncoder.getPosition(),
        )

    def arcadeDrive(self, fwd: float, rot: float):
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        self.drive.arcadeDrive(fwd, rot)

    def tankDriveVolts(self, leftVolts, rightVolts):
        """Control the robot's drivetrain with voltage inputs for each side."""
        # Set the voltage of the left side.
        # inverting this delays the KP issue but doesn't fix it
        self.leftMotors.setVoltage(leftVolts)

        # Set the voltage of the right side.
        self.rightMotors.setVoltage(rightVolts)

        # print(f"({leftVolts}, {rightVolts})")

        # Resets the timer for this motor's MotorSafety
        self.drive.feed()

        # Reset the encoders
        self.resetEncoders()

    def getPose(self):
        """Returns the current position of the robot using it's odometry."""
        return self.odometry.getPose()

    def getWheelSpeeds(self):
        """Return an object which represents the wheel speeds of our drivetrain."""
        speeds = DifferentialDriveWheelSpeeds(
            self.leftEncoder.getVelocity(), -self.rightEncoder.getVelocity()
        )
        return speeds

    def resetEncoders(self):
        """Resets the drive encoders to currently read a position of 0."""
        self.leftEncoder.setPosition(0)
        self.rightEncoder.setPosition(0)

        # https://docs.wpilib.org/en/stable/docs/software/kinematics-and-odometry/differential-drive-odometry.html#resetting-the-robot-pose
        self.odometry.resetPosition(
            self.ahrs.getRotation2d(),
            self.leftEncoder.getPosition(),
            -self.rightEncoder.getPosition(),
            Pose2d(),
        )

    def getAverageEncoderDistance(self):
        """
        Gets the average distance of the two encoders.
        :returns: the average of the two encoder readings
        """
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2.0

    def getLeftEncoder(self) -> wpilib.Encoder:
        """
        Gets the left drive encoder.
        :returns: the left drive encoder
        """
        return self.leftEncoder

    def getRightEncoder(self) -> wpilib.Encoder:
        """
        Gets the right drive encoder.

        :returns: the right drive encoder
        """
        return self.rightEncoder

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the drive to drive more slowly.
        :param maxOutput: the maximum output to which the drive will be constrained
        """
        self.drive.setMaxOutput(maxOutput)

    def zeroHeading(self):
        """
        Zeroes the heading of the robot.
        """
        self.ahrs.reset()

    def getHeading(self) -> float:
        """
        Returns the heading of the robot.
        :returns: the robot's heading in degrees, from 180 to 180
        """
        return geometry.Rotation2d.fromDegrees(self.ahrs.getYaw()).degrees()

    def getPitch(self):
        """
        Returns the angle of the robot
        """
        return geometry.Rotation2d.fromDegrees(self.ahrs.getPitch())

    def getTurnRate(self) -> float:
        """
        Returns the turn rate of the robot.
        :returns: The turn rate of the robot, in degrees per second
        """
        return self.ahrs.getRate()

    def periodic(self) -> None:
        """Runs every loop"""

        self.sd.putNumber("Audio/MatchTime", int(DriverStation.getMatchTime()))

        # See here for turning bug
        # https://github.com/FRC-1721/1721-ChargedUp/issues/10#issuecomment-1386472066
        return self.ahrs.getRawGyroZ()

    def periodic(self):
        """
        Called periodically when it can be called. Updates the robot's
        odometry with sensor data.
        """
        self.odometry.update(
            self.ahrs.getRotation2d(),
            self.leftEncoder.getPosition(),
            -self.rightEncoder.getPosition(),
        )

        self.sd.putNumber("Audio/MatchTime", int(wpilib.DriverStation.getMatchTime()))

        self.sd.putNumber("Pose/Pose x", self.getPose().x)
        self.sd.putNumber("Pose/Pose y", self.getPose().y)
        self.sd.putNumber("Pose/Pose t", self.getPose().rotation().radians())

        self.sd.putNumber("Temp/L1", self.leftMotor1.getMotorTemperature())
        self.sd.putNumber("Temp/L2", self.leftMotor2.getMotorTemperature())
        self.sd.putNumber("Temp/R1", self.rightMotor1.getMotorTemperature())
        self.sd.putNumber("Temp/R2", self.rightMotor2.getMotorTemperature())
        self.sd.putNumber("Pose/Pose x", self.getPose().x)
        self.sd.putNumber("Pose/Pose y", self.getPose().y)
        self.sd.putNumber("Pose/Pose t", self.getPose().rotation().radians())
