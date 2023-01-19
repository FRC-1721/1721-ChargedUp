# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2
import math
import logging

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
        encoderDistPerP = (
            self.driveConst["kWheelDiameterInches"] * math.pi
        ) / self.driveConst["kEncoderCPR"]

        self.leftEncoder.setPositionConversionFactor(encoderDistPerP)
        self.rightEncoder.setPositionConversionFactor(encoderDistPerP)

        self.gyro = AHRS.create_spi()  # creates navx object

    def getGyroHeading(self):
        """
        Returns the gyro heading.
        """

        return geometry.Rotation2d.fromDegrees(self.gyro.getAngle())

    def arcadeDrive(self, fwd: float, rot: float):
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        self.drive.arcadeDrive(fwd, rot)

    def resetEncoders(self):
        """Resets the drive encoders to currently read a position of 0."""
        self.leftEncoder.reset()
        self.rightEncoder.reset()

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
        # This value takes time to update
        self.gyro.reset()

    def getHeading(self):
        """
        Returns the heading of the robot.
        :returns: the robot's heading in degrees, from 180 to 180
        """
        return geometry.Rotation2d.fromDegrees(self.gyro.getAngle())

    def getAngle(self):
        """
        Returns the angle of the robot
        """
        return geometry.Rotation2d.fromDegrees(self.gyro.getPitch())

    def getTurnRate(self):
        """
        Returns the turn rate of the robot.
        :returns: The turn rate of the robot, in degrees per second
        """
        return self.gyro.getRate()
