# FRC 1721

import wpilib
import wpimath.controller

import commands2
import commands2.cmd
import commands2.button

# Constants
from constants.constants import getConstants

# Subsystems
import subsystems.drivesubsystem

# Commands
import commands.turntoangle
import commands.turntoangleprofiled


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.

    """

    def __init__(self):
        """The container for the robot. Contains subsystems, OI devices, and commands."""
        # Setup constants
        self.controlConsts = getConstants("robot_controls")
        self.hardConsts = getConstants("robot_hardware")
        self.pidConsts = getConstants("robot_pid")
        self.driveConsts = self.controlConsts["driver"]

        # The robot's subsystems
        self.robotDrive = subsystems.drivesubsystem.DriveSubsystem()

        # The driver's controller
        self.driverController = commands2.button.CommandJoystick(
            self.driveConsts["controller_port"]
        )

        # Configure the button bindings
        self.configureButtonBindings()

        # Configure default commands
        # Set the default drive command to split-stick arcade drive
        self.robotDrive.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            commands2.RunCommand(
                lambda: self.robotDrive.arcadeDrive(
                    -self.driverController.getRawAxis(self.driveConsts["ForwardAxis"]),
                    -self.driverController.getRawAxis(self.driveConsts["SteerAxis"]),
                ),
                [self.robotDrive],
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
            self.driverController, self.driveConsts["HalfSpeedButton"]
        ).onTrue(
            commands2.InstantCommand(
                (lambda: self.robotDrive.setMaxOutput(0.5)), [self.robotDrive]
            )
        ).onFalse(
            commands2.InstantCommand(
                (lambda: self.robotDrive.setMaxOutput(1)), [self.robotDrive]
            )
        )

        # Stabilize robot to drive straight with gyro when left bumper is held
        # TODO: Load button from config file
        commands2.button.JoystickButton(
            self.driverController, self.driveConsts["DiffLock"]
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
                    -self.driverController.getLeftY(), output
                ),
                # Require the robot drive
                [self.robotDrive],
            )
        )

        # Turn to 90 degrees when the 'X' button is pressed, with a 5 second timeout
        # TODO: Load button from config file
        commands2.button.JoystickButton(
            self.driverController, self.driveConsts["Turn90"]
        ).onTrue(commands.turntoangle.TurnToAngle(90, self.robotDrive).withTimeout(5))

        # Turn to -90 degrees with a profile when the Circle button is pressed, with a 5 second timeout
        # TODO: Load button from config file
        commands2.button.JoystickButton(
            self.driverController, self.driveConsts["TurnAnti90"]
        ).onTrue(
            commands.turntoangleprofiled.TurnToAngleProfiled(
                -90, self.robotDrive
            ).withTimeout(5)
        )

    def getAutonomousCommand(self) -> commands2.Command:
        """
        Use this to pass the autonomous command to the main :class:`.Robot` class.
        :returns: the command to run in autonomous
        """
        return commands2.InstantCommand()
