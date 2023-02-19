# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2

from ntcore import NetworkTableInstance

# Constants
from constants.constants import getConstants

# Vendor Libs
from rev import CANSparkMax, CANSparkMaxLowLevel


class ClawSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """
        Creates a new Claw subsystem
        """
        super().__init__()

        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.sd = self.nt.getTable("SmartDashboard")

        # Get hardware constants
        constants = getConstants("robot_hardware")
        pidConstants = getConstants("robot_pid")
        self.clawConst = constants["claw"]
        self.pidConst = pidConstants["claw"]

        # the claw motor
        self.motor = CANSparkMax(
            self.clawConst["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.motor.setInverted(self.clawConst["Inverted"])

        # TODO: These should to be replaced with CAN motor controllers
        self.encoder = self.motor.getEncoder()

        # Pid values
        self.PID = self.motor.getPIDController()
        self.PID.setP(self.pidConst["kp"])
        self.PID.setI(self.pidConst["ki"])
        self.PID.setD(self.pidConst["kd"])
        self.PID.setFF(self.pidConst["ff"])

    def setCurrentlimit(self, current):
        self.motor.setSmartCurrentLimit(current)

    def grab(self, speed):
        self.motor.set(speed)

    def periodic(self) -> None:
        """Runs periodic things"""

        self.sd.putNumber("Thermals/Claw", self.motor.getMotorTemperature())
