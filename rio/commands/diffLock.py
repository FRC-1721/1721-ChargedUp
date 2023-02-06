import commands2

from subsystems.drivesubsystem import DriveSubsystem


class DiffLock:
    def __init__(self, driveSubsystem: DriveSubsystem) -> None:
        super().__init__()

        self.driveSubsystem = driveSubsystem

        self.addRequirements([self.driveSubsystem])

    def initialize(self):
        # what needs to be done here is as follows according to Mark
        # the motors need to spin at an small difference
        # one oposite the other (per side)
        # this will make the robot be able to stay in place
        pass

    def end(self, interrupted: bool) -> None:
        return True


# Insparation
# commands2.button.JoystickButton(
#     self.driverController, self.driverConsts["DiffLock"]
# ).whileTrue(
#     commands2.PIDCommand(
#         wpimath.controller.PIDController(
#             self.pidConsts["drive"]["kStabilizationP"],
#             self.pidConsts["drive"]["kStabilizationI"],
#             self.pidConsts["drive"]["kStabilizationD"],
#         ),
#         # Close the loop on the turn rate
#         self.robotDrive.getTurnRate,
#         # Setpoint is 0
#         0,
#         # Pipe the output to the turning controls
#         lambda output: self.robotDrive.arcadeDrive(
#             -self.driverConsts["ForwardAxis"],
#             output,
#         ),
#         # Require the robot drive
#         [self.robotDrive],
#     )
# )
