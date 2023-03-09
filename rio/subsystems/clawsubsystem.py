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

        # the claw motor
        self.motor = CANSparkMax(
            self.clawConst["MotorPort"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.motor.setInverted(self.clawConst["Inverted"])

    def setCurrentlimit(self, current):
        self.motor.setSmartCurrentLimit(current)

    def grab(self, speed):
        self.motor.set(speed)

    def periodic(self) -> None:
        """Runs periodic things"""

        self.sd.putNumber("Thermals/Claw", self.motor.getMotorTemperature())
