# FRC 1721

import wpilib
import wpimath.controller

import logging

import commands2
import commands2.cmd
import commands2.button

# Constants
from constants.constants import getConstants

# Subsystems
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.clawsubsystem import ClawSubsystem
from subsystems.armsubsystem import ArmSubsystem

# Commands
from commands.turntoangle import TurnToAngle
from commands.turntoangleprofiled import TurnToAngleProfiled
from commands.flybywire import FlyByWire
from commands.turntoangle import TurnToAngle
from commands.turntoangleprofiled import TurnToAngleProfiled
from commands.flybywire import FlyByWire
from commands.clamp import Clamp
from commands.extend import Extend
from commands.retract import Retract
from commands.up import Up
from commands.down import Down


# Autonomous
from autonomous.curvyAuto import CurvyAuto

# NetworkTables
from ntcore import NetworkTableInstance

# Misc
from extras.deployData import getDeployData


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.

    """

    def __init__(self):
        """The container for the robot. Contains subsystems, OI devices, and commands."""
        # Configure networktables
        self.configureNetworktables()

        # Setup constants
        self.controlConsts = getConstants("robot_controls")
        self.hardConsts = getConstants("robot_hardware")
        self.pidConsts = getConstants("robot_pid")
        self.driverConsts = self.controlConsts["main mode"]["driver"]
        self.operatorConsts = self.controlConsts["main mode"]["operator"]

        # The robot's subsystems
        self.robotDrive = DriveSubsystem()
        self.clawSubsystem = ClawSubsystem()
        self.armSubsystem = ArmSubsystem()

        # The driver's controller
        self.driverController = commands2.button.CommandJoystick(
            self.driverConsts["controller_port"]
        )

        # The operators controller
        self.operatorController = commands2.button.CommandJoystick(
            self.operatorConsts["controller_port"]
        )

        # Configure the button bindings
        self.configureButtonBindings()

        # Setup all autonomous routines
        self.configureAutonomous()

        # Configure default commands
        self.robotDrive.setDefaultCommand(
            FlyByWire(
                self.robotDrive,
                lambda: -self.driverController.getRawAxis(
                    self.driverConsts["ForwardAxis"],
                ),
                lambda: self.driverController.getRawAxis(
                    self.driverConsts["SteerAxis"],
                ),
            )
        )

        # self.sd.putNumber("someNumber", 1234)
        # print(self.FMSinfo.getNumber("StationNumber", -1))

        # Setup default commands
        self.clawSubsystem.setDefaultCommand(
            Clamp(self.clawSubsystem, self.operatorController.getRawAxis(3))
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created via the button
        factories on commands2.button.CommandGenericHID or one of its
        subclasses (commands2.button.CommandJoystick or command2.button.CommandXboxController).
        """
        # Drive at half speed when the right bumper is held
        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["HalfSpeedButton"]
        ).onTrue(
            commands2.InstantCommand(
                (lambda: self.robotDrive.setMaxOutput(0.5)), [self.robotDrive]
            )
        ).onFalse(
            commands2.InstantCommand(
                (lambda: self.robotDrive.setMaxOutput(1)), [self.robotDrive]
            )
        )

        commands2.button.JoystickButton(self.driverController, 1).onTrue(
            commands2.InstantCommand(
                (lambda: self.robotDrive.resetEncoders()), [self.robotDrive]
            )
        )

        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["DiffLock"]
        ).whileTrue(
            commands2.PIDCommand(
                wpimath.controller.PIDController(
                    self.pidConsts["drive"]["kStabilizationP"],
                    self.pidConsts["drive"]["kStabilizationI"],
                    self.pidConsts["drive"]["kStabilizationD"],
                ),
                # Close the loop on the turn rate
                self.robotDrive.getTurnRate,
                # Setpoint is 0
                0,
                # Pipe the output to the turning controls
                lambda output: self.robotDrive.arcadeDrive(
                    -self.driverConsts["ForwardAxis"],
                    output,
                ),
                # Require the robot drive
                [self.robotDrive],
            )
        )

        # Turn to 90 degrees, with a 5 second timeout
        commands2.button.JoystickButton(
            self.driverController,
            self.driverConsts["Turn90"],
        ).onTrue(
            TurnToAngle(
                90,
                self.robotDrive,
            ).withTimeout(5)
        )

        # Turn to -90 degrees with a profile, with a 5 second timeout
        commands2.button.JoystickButton(
            self.driverController,
            self.driverConsts["TurnAnti90"],
        ).onTrue(
            TurnToAngleProfiled(
                -90,
                self.robotDrive,
            ).withTimeout(5)
        )

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Up"],
        ).whileHeld(Extend(self.armSubsystem).withTimeout(5))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Down"],
        ).whileHeld(Retract(self.armSubsystem).withTimeout(5))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Extend"],
        ).whileHeld(Up(self.armSubsystem).withTimeout(5))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Retract"],
        ).whileHeld(Down(self.armSubsystem).withTimeout(5))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Unclamp"],
        ).whileHeld(
            Clamp(
                self.clawSubsystem, -self.operatorController.getRawAxis(2)
            ).withTimeout(5)
        )

    def configureAutonomous(self):
        # Create a sendable chooser
        self.autoChooser = wpilib.SendableChooser()

        # Add options for chooser
        # self.autoChooser.setDefaultOption("Null Auto", NullAuto(self.drivetrain))
        self.autoChooser.setDefaultOption("Cury Auto", CurvyAuto().withTimeout(15))
        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.autoChooser)
        # self.sd.putData("Autonomous", self.autoChooser) # TODO: I don't know why this doesn't work.

    def configureNetworktables(self):
        # Configure networktables
        self.nt = NetworkTableInstance.getDefault()
        self.sd = self.nt.getTable("SmartDashboard")

        # Subtables
        self.build_table = self.sd.getSubTable("BuildData")

        # Build data (May need to be moved to a dedicated function to be updated more than once)
        data = getDeployData()
        for key in data:
            key_entry = self.build_table.getEntry(str(key))
            key_entry.setString(str(data[key]))

        self.ntmov = self.sd.getSubTable("Test")
        self.ntmov.putNumber("test", 2)

    def getAutonomousCommand(self) -> commands2.Command:
        """
        Use this to pass the autonomous command to the main :class:`.Robot` class.
        :returns: the command to run in autonomous
        """
        return self.autoChooser.getSelected()
