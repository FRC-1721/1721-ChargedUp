import commands2

from subsystems.armsubsystem import ArmSubsystem
from subsystems.drivesubsystem import DriveSubsystem

from commands.presetArm import PresetArm
from autonomous.flywithwire import FlyWithWires


class DropDriveAuto(commands2.SequentialCommandGroup):
    def __init__(
        self,
        armSubsystem: ArmSubsystem,
        driveSubsystem: DriveSubsystem,
    ) -> None:
        """
        Moving the arm down to score in auto
        then drive backwards
        """
        super().__init__(
            # keep at starting config
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 25, 163).withTimeout(1),
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 25, 236).withTimeout(1),
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 0, 236).withTimeout(1),
            FlyWithWires(driveSubsystem, fwd=-0.5, time=3),
        )
