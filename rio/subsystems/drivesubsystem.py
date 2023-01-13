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


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()

        # Get hardware constants
        constants = getConstants("robot_hardware")  # All the robot hardware consts
        self.driveConst = constants["drivetrain"]  # All the drivetrain consts
        self.leftCosnt = self.driveConst["leftMotor"]  # Left specific
        self.rightCosnt = self.driveConst["rightMotor"]  # Right specific
        self.imuConst = self.driveConst["imu"]  # imu's constants

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

        # TODO: Replace with proper motorconfigs
        self.leftMotor1.setInverted(False)
        self.leftMotor2.setInverted(False)
        self.rightMotor1.setInverted(False)
        self.rightMotor2.setInverted(False)

        # The robot's drivetrain kinematics
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

        # TODO: These need to be replaced with CAN motor controllers
        # The left-side drive encoder
        self.leftEncoder = wpilib.Encoder(
            self.leftCosnt["EncoderPorts"][0],
            self.leftCosnt["EncoderPorts"][1],
            self.leftCosnt["EncoderReversed"],
        )

        # The right-side drive encoder
        self.rightEncoder = wpilib.Encoder(
            self.rightCosnt["EncoderPorts"][0],
            self.rightCosnt["EncoderPorts"][1],
            self.rightCosnt["EncoderReversed"],
        )

        # Sets the distance per pulse for the encoders
        encoderDistPerP = (
            self.driveConst["kWheelDiameterInches"] * math.pi
        ) / self.driveConst["kEncoderCPR"]

        self.leftEncoder.setDistancePerPulse(encoderDistPerP)
        self.rightEncoder.setDistancePerPulse(encoderDistPerP)

        # Setup Pigeon
        # Docs: https://docs.ctre-phoenix.com/en/stable/ch11_BringUpPigeon.html?highlight=pigeon#pigeon-api
        self.imu = Pigeon2(self.imuConst["can_id"])  # Create object

        # Setup Pigeon pose
        self.imu.configMountPose(
            self.imuConst["yaw"],
            self.imuConst["pitch"],
            self.imuConst["roll"],
        )

    def getGyroHeading(self):
        """
        Returns the gyro heading.
        """

        return geometry.Rotation2d.fromDegrees(self.imu.getYaw())

    def arcadeDrive(self, fwd: float, rot: float):
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """

        self.drive.arcadeDrive(fwd, rot)

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the drive to drive more slowly.

        :param maxOutput: the maximum output to which the drive will be constrained
        """
        self.drive.setMaxOutput(maxOutput)
