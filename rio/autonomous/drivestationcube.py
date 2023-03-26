import commands2

from subsystems.armsubsystem import ArmSubsystem
from subsystems.clawsubsystem import ClawSubsystem
from subsystems.drivesubsystem import DriveSubsystem

from commands.presetArm import PresetArm
from commands.manualGripper import ManualGripper
from autonomous.flywithwire import FlyWithWires
from autonomous.level import Level


class DrivestationCube(commands2.SequentialCommandGroup):
    def __init__(
        self,
        clawSubsystem: ClawSubsystem,
        armSubsystem: ArmSubsystem,
        driveSubsystem: DriveSubsystem,
    ) -> None:
        """
        a 'simple' drive back command
        """

        super().__init__(
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 82, 163).withTimeout(2),
            ManualGripper(clawSubsystem, 0.35).withTimeout(2),
            FlyWithWires(driveSubsystem, fwd=-0.75, time=3),
            Level(driveSubsystem, armSubsystem, fwd=-0.3, time=0.1),
        )
