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


class ArmSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()

        # Get hardware constants
        constants = getConstants("robot_hardware")  # All the robot hardware consts
        self.armConst = constants["arm"]  # All the arm consts
        self.backCosnt = self.armConst["backMotor"]  # back specific
        self.middleCosnt = self.armConst["middleMotor"]  # middle specific
        self.imuConst = self.armConst["imu"]  # imu's constants

        # The motor on the back of the drive.
        self.backMotor = CANSparkMax(
            self.backCosnt["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.backMotors.setInverted(self.backCosnt["Inverted"])

        # The motor on the middle of the drive.
        self.middleMotor = CANSparkMax(
            self.middleCosnt["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.middleMotors.setInverted(self.middleCosnt["Inverted"])

        # TODO: Replace with proper motorconfigs
        self.backMotor.setInverted(False)
        self.middleMotor.setInverted(False)

        # TODO: These need to be replaced with CAN motor controllers
        # The back-side arm encoder
        self.backEncoder = wpilib.Encoder(
            self.backCosnt["EncoderPorts"],
            self.backCosnt["EncoderReversed"],
        )

        # The middle-side arm encoder
        self.middleEncoder = wpilib.Encoder(
            self.middleCosnt["EncoderPorts"],
            self.middleCosnt["EncoderReversed"],
        )

        # Sets the distance per pulse for the encoders
        encoderDistPerP = (
            self.armConst["kWheelDiameterInches"] * math.pi
        ) / self.armConst["kEncoderCPR"]

        self.backEncoder.setDistancePerPulse(encoderDistPerP)
        self.middleEncoder.setDistancePerPulse(encoderDistPerP)

        
        

    