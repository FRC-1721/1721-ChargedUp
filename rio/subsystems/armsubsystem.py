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
        self.armConst = constants["arm"]  # All the arm consts
        self.backCosnt = self.armConst["backMotor"]  # back specific
        self.middleCosnt = self.armConst["middleMotor"]  # middle specific
        self.pidConst = pidConstants["arm"]

        # The motor on the back of the drive. (The arm extension motor)
        self.backMotor = CANSparkMax(
            self.backCosnt["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.backMotor.setInverted(self.backCosnt["Inverted"])

        # The motor on the middle of the drive. (The screw motor)
        self.middleMotor = CANSparkMax(
            self.middleCosnt["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.middleMotor.setInverted(self.middleCosnt["Inverted"])

        # TODO: Replace with proper motorconfigs
        self.backMotor.setInverted(False)
        self.middleMotor.setInverted(False)

        # TODO: These need to be replaced with CAN motor controllers
        # The back-side arm encoder
        self.backEncoder = self.backMotor.getEncoder()

        # The middle-side arm encoder
        self.middleEncoder = self.middleMotor.getEncoder()

        # Sets the distance per pulse for the encoders

        # self.backEncoder.setPositionConversionFactor(
        #     1 / self.backCosnt["encoderConversionFactor"]
        # )
        # self.middleEncoder.setPositionConversionFactor(
        #     1 / self.middleCosnt["encoderConversionFactor"]
        # )

        # Pid values
        self.PID = self.backMotor.getPIDController()
        self.PID.setP(self.pidConst["kp"])
        self.PID.setI(self.pidConst["ki"])
        self.PID.setD(self.pidConst["kd"])
        self.PID.setFF(self.pidConst["ff"])

        # Hardware Limits
        self.spoolLimit = self.backMotor.getReverseLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )
        self.ledForwardLimit = self.middleMotor.getForwardLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )
        self.ledBackwardLimit = self.middleMotor.getReverseLimitSwitch(
            SparkMaxLimitSwitch.Type.kNormallyOpen
        )

        self.spoolLimit.enableLimitSwitch(True)
        self.ledForwardLimit.enableLimitSwitch(True)
        self.ledBackwardLimit.enableLimitSwitch(True)

    def setCurrentlimit(self, current):
        self.backMotor.setSmartCurrentLimit(current)

    def extension(self, speed):
        self.backMotor(speed)

    def ascent(self, speed):
        self.middleMotor.set(speed)

    def periodic(self) -> None:
        print("self.backEncoder:", self.backEncoder.getPosition())
