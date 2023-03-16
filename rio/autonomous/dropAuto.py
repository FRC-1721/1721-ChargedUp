import commands2

from subsystems.armsubsystem import ArmSubsystem
from commands.presetArm import PresetArm


class DropAuto(commands2.SequentialCommandGroup):
    def __init__(self, armSubsystem: ArmSubsystem) -> None:
        """
        Moving the arm down to score in auto
        """
        super().__init__(
            # keep at starting config
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 25, 163).withTimeout(1),
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 25, 236).withTimeout(1),
            PresetArm(armSubsystem, lambda: 0, lambda: 0, 0, 236).withTimeout(1),
        )
