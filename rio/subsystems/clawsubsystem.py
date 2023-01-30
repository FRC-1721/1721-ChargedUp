# FRC 1721

# Robot
import wpilib
import wpilib.drive
import commands2

# Constants
from constants.constants import getConstants

# Vendor Libs
from rev import CANSparkMax, CANSparkMaxLowLevel


class ArmSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        """
        Creates a new Claw subsystem
        """
        super().__init__()

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
        self.encoder = wpilib.Encoder(
            self.clawConst["EncoderPorts"],
            self.clawConst["EncodarmerReversed"],
        )

        # Pid values
        self.PID = self.motor.getPIDController()
        self.PID.setP(self.pidConst["kp"])
        self.PID.setI(self.pidConst["ki"])
        self.PID.setD(self.pidConst["kd"])
        self.PID.setFF(self.pidConst["ff"])

    def clamp(self, volts, time):
        self.timer = wpilib.timer()
        self.timer.start()
        self.motor.setVoltage(volts)
        if self.timer.hasElapsed(time) == time:
            self.motor.setVoltage = 0
