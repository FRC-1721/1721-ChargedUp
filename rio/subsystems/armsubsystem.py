# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2
import math

# Constants
from constants.constants import getConstants

# Vendor Libs
from rev import CANSparkMax, CANSparkMaxLowLevel, SparkMaxLimitSwitch


class ArmSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new Arm subsystem"""
        super().__init__()

        # Get hardware constants
        constants = getConstants("robot_hardware")  # All the robot hardware consts
        pidConstants = getConstants("robot_pid")
        armConst = constants["arm"]  # All the arm consts
        self.elevatorConst = armConst["elevatorMotor"]
        self.ladderConst = armConst["ladderMotor"]
        pidConst = pidConstants["arm"]
        self.elevPIDConst = pidConst["elevator"]
        self.laddPIDConst = pidConst["ladder"]

        # This motor drives the spool in the rear
        self.elevatorMotor = CANSparkMax(
            self.elevatorConst["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )
        self.elevatorMotor.setInverted(self.elevatorConst["Inverted"])

        # This motor drives the lead screw
        self.ladderMotor = CANSparkMax(
            self.ladderConst["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )
        self.ladderMotor.setInverted(self.ladderConst["Inverted"])

        # Encoders
        self.elevatorEncoder = self.elevatorMotor.getEncoder()
        self.elevatorEncoder.setPositionConversionFactor(
            self.elevatorConst["ConversionFactor"]
        )
        self.ladderEncoder = self.ladderMotor.getEncoder()
        self.ladderEncoder.setPositionConversionFactor(
            self.ladderConst["ConversionFactor"]
        )
        # If we think we're perfectly at 0, we're prolly not.
        if self.ladderEncoder.getPosition() == 0.0:
            self.ladderEncoder.setPosition(261)

        # PID Values
        self.elevPID = self.elevatorMotor.getPIDController()
        self.elevPID.setP(self.elevPIDConst["kp"])
        self.elevPID.setI(self.elevPIDConst["ki"])
        self.elevPID.setD(self.elevPIDConst["kd"])
        self.elevPID.setFF(self.elevPIDConst["ff"])

        self.laddPID = self.ladderMotor.getPIDController()
        self.laddPID.setP(self.laddPIDConst["kp"])
        self.laddPID.setI(self.laddPIDConst["ki"])
        self.laddPID.setD(self.laddPIDConst["kd"])
        self.laddPID.setFF(self.laddPIDConst["ff"])

        # Hardware Limits
        self.spoolLimit = self.elevatorMotor.getReverseLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )
        self.ledForwardLimit = self.ladderMotor.getForwardLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )
        self.ledBackwardLimit = self.ladderMotor.getReverseLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )

        # Limits
        self.spoolLimit.enableLimitSwitch(True)
        self.ledForwardLimit.enableLimitSwitch(True)
        self.ledBackwardLimit.enableLimitSwitch(True)

        # Current limits
        self.elevatorMotor.setSmartCurrentLimit(8)

        # starting values
        self.elevatorEncoder.setPosition(self.elevatorConst["Start"])
        self.ladderEncoder.setPosition(self.ladderConst["Start"])

    def gotoPosition(self, extension: float = 0, angle: float = 0):
        """
        Takes an extension value (in meters)
        and an angle value (in radians)
        And sets the integrated PID to target.
        """

        self.elevPID.setReference(extension, CANSparkMax.ControlType.kPosition)
        self.laddPID.setReference(angle, CANSparkMax.ControlType.kPosition)

    def extension(self, speed):
        """
        This is the spool motor, it controls
        how much rope we let out.
        """
        if self.elevatorEncoder.getPosition() >= 100 and speed < 0.1:
            self.elevatorMotor.set(speed)

        else:
            self.elevatorMotor.set(speed)

    def ascent(self, speed):
        """
        This is the lead screw motor, it controls
        where on the screw the fulcrum of the lift
        is
        """
        self.ladderMotor.set(speed)

    def periodic(self) -> None:
        # Reset on limits
        if self.spoolLimit.get():
            self.elevatorEncoder.setPosition(0)

        if self.ledBackwardLimit.get():
            self.ladderEncoder.setPosition(0)
