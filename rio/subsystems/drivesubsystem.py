# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2
import math

# Constants
from constants.constants import getConstants


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()

        # Get hardware constants
        constants = getConstants("robot_hardware")
        self.drive_const = constants["drivetrain"]

        # The motors on the left side of the drive.
        self.leftMotors = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(self.drive_const["leftMotor"]["kLeftMotor1Port"]),
            wpilib.PWMSparkMax(self.drive_const["leftMotor"]["kLeftMotor2Port"]),
        )

        # The motors on the right side of the drive.
        self.rightMotors = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(self.drive_const["rightMotor"]["kRightMotor1Port"]),
            wpilib.PWMSparkMax(self.drive_const["rightMotor"]["kRightMotor2Port"]),
        )

        # The robot's drive
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

        # The left-side drive encoder
        self.leftEncoder = wpilib.Encoder(
            self.drive_const["leftMotor"]["kLeftEncoderPorts"][0],
            self.drive_const["leftMotor"]["kLeftEncoderPorts"][1],
            self.drive_const["leftMotor"]["kLeftEncoderReversed"],
        )

        # The right-side drive encoder
        self.rightEncoder = wpilib.Encoder(
            self.drive_const["rightMotor"]["kRightEncoderPorts"][0],
            self.drive_const["rightMotor"]["kRightEncoderPorts"][1],
            self.drive_const["rightMotor"]["kRightEncoderReversed"],
        )

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightMotors.setInverted(True)

        # Sets the distance per pulse for the encoders
        encoderDistPerP = (
            self.drive_const["kWheelDiameterInches"] * math.pi
        ) / self.drive_const["kEncoderCPR"]

        self.leftEncoder.setDistancePerPulse(encoderDistPerP)
        self.rightEncoder.setDistancePerPulse(encoderDistPerP)

        self.gyro = wpilib.ADXRS450_Gyro()

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
        self.gyro.reset()

    def getHeading(self):
        """
        Returns the heading of the robot.

        :returns: the robot's heading in degrees, from 180 to 180
        """
        return math.remainder(self.gyro.getAngle(), 180) * (
            -1 if self.drive_const["leftMotor"]["kGyroReversed"] else 1
        )

    def getTurnRate(self):
        """
        Returns the turn rate of the robot.

        :returns: The turn rate of the robot, in degrees per second
        """
        return self.gyro.getRate() * (-1 if self.drive_const["kGyroReversed"] else 1)
