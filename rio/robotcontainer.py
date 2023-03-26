# FRC 1721

import wpilib

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
from commands.objDetect import limeLightDetector
from commands.turntoangle import TurnToAngle
from commands.turntoangleprofiled import TurnToAngleProfiled
from commands.flybywire import FlyByWire
from commands.manualGripper import ManualGripper
from commands.presetArm import PresetArm
from commands.manualArm import ManualArm
from commands.findZero import FindZero
from commands.holdPosition import HoldPosition
from commands.flyforwire import FlyForWire
from commands.crawl import Crawl

# Autonomous
from autonomous.noauto import NoAuto
from autonomous.blockDrop import BlockDrop
from autonomous.blockDrip import BlockDrip
from autonomous.shortBlock import ShortBlock
from autonomous.dropAuto import DropAuto
from autonomous.dropDriveAuto import DropDriveAuto
from autonomous.shortCone import ShortCone
from autonomous.drivestationcube import DrivestationCube

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

        # Default drive command
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

        # The default command for the arm Subsystem is manual control
        self.armSubsystem.setDefaultCommand(
            PresetArm(
                self.armSubsystem,
                lambda: -self.operatorController.getRawAxis(
                    1,
                ),
                lambda: self.operatorController.getRawAxis(
                    5,
                ),
            )
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

        # This is causing an error read the message left in the class
        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["DiffLock"]
        ).toggleOnTrue(HoldPosition(self.robotDrive))

        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["globDetect"]
        ).whileTrue(limeLightDetector(self.robotDrive))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Unclamp"],
        ).whileTrue(ManualGripper(self.clawSubsystem, grabForce=-1))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["Clamp"],
        ).whileTrue(ManualGripper(self.clawSubsystem, grabForce=1))

        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["FindZero"],
        ).whileTrue(FindZero(self.armSubsystem))

        # This is temporary low goal!
        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["LowGoal"],
        ).toggleOnTrue(
            PresetArm(
                self.armSubsystem,
                lambda: -self.operatorController.getRawAxis(
                    1,
                ),
                lambda: self.operatorController.getRawAxis(
                    5,
                ),
                45,  # Random!
                150,  # Just as random!
            )
        )

        # High Goal!
        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["HighGoal"],
        ).toggleOnTrue(
            PresetArm(
                self.armSubsystem,
                lambda: -self.operatorController.getRawAxis(
                    1,
                ),
                lambda: self.operatorController.getRawAxis(
                    5,
                ),
                82,  # Random!
                163,  # Just as random!
            )
        )

        # Starting config
        commands2.button.JoystickButton(
            self.driverController,
            self.driverConsts["StartConfig"],
        ).toggleOnTrue(
            PresetArm(
                self.armSubsystem,
                lambda: -self.operatorController.getRawAxis(
                    1,
                ),
                lambda: self.operatorController.getRawAxis(
                    5,
                ),
                0,  # Random!
                55,  # Just as random!
            )
        )

        # This is caleb's fully manual mode
        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["ManualMode"],
        ).toggleOnTrue(
            ManualArm(
                self.armSubsystem,
                lambda: -self.operatorController.getRawAxis(
                    1,
                ),
                lambda: self.operatorController.getRawAxis(
                    5,
                ),
            )
        )

        # a lock command for the claw
        commands2.button.JoystickButton(
            self.operatorController,
            self.operatorConsts["hold"],
        ).toggleOnTrue(ManualGripper(self.clawSubsystem, grabForce=-0.35))

        # a slow command
        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["Slow"]
        ).whileTrue(
            FlyForWire(
                self.robotDrive,
                lambda: -self.driverController.getRawAxis(
                    self.driverConsts["ForwardAxis"],
                ),
                lambda: self.driverController.getRawAxis(
                    self.driverConsts["SteerAxis"],
                ),
            )
        )

        commands2.button.JoystickButton(
            self.driverController, self.driverConsts["Crawl"]
        ).whileTrue(
            Crawl(
                self.robotDrive,
                lambda: self.driverController.getRawAxis(
                    self.driverConsts["SteerAxis"],
                ),
            )
        )

    def configureAutonomous(self):
        # Create a sendable chooser
        self.autoChooser = wpilib.SendableChooser()

        # Add options for chooser
        # Cones
        self.autoChooser.addOption(
            "Cone Long Drive", DropDriveAuto(self.armSubsystem, self.robotDrive)
        )
        self.autoChooser.addOption(
            "Cone Short Drive", ShortCone(self.armSubsystem, self.robotDrive)
        )
        self.autoChooser.addOption(
            "Cone No Drive",
            DropAuto(self.armSubsystem),
        )
        # Blocks
        self.autoChooser.addOption(
            "Block Long Drive",
            BlockDrop(self.clawSubsystem, self.armSubsystem, self.robotDrive),
        )
        self.autoChooser.addOption(
            "Block Short Drive",
            ShortBlock(self.clawSubsystem, self.armSubsystem, self.robotDrive),
        )
        self.autoChooser.addOption(
            "Block No Drive",
            BlockDrip(self.clawSubsystem, self.armSubsystem),
        )
        # Misc
        self.autoChooser.addOption(
            "Drivestation [Exerpimental]",
            DrivestationCube(self.clawSubsystem, self.armSubsystem, self.robotDrive),
        )
        self.autoChooser.setDefaultOption("No Auto", NoAuto())

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

    def getAutonomousCommand(self) -> commands2.Command:
        """
        Use this to pass the autonomous command to the main :class:`.Robot` class.
        :returns: the command to run in autonomous
        """
        return self.autoChooser.getSelected()
