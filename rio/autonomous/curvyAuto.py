# commands2
import commands2

from commands2 import WaitCommand

# sub syss
from subsystems.armsubsystem import ArmSubsystem

# commands and autonomous
from autonomous.crossLinePath import CrossLinePath
from commands.presetArm import PresetArm


class CurvyAuto(commands2.SequentialCommandGroup):
    def __init__(self, armSubsystem: ArmSubsystem) -> None:
        """
        extendo
        downo
        failo
        cryo
        """

        super().__init__(
            PresetArm(
                armSubsystem, elevFine=self.toCallable(1), laddFine=self.toCallable(0)
            ),
            WaitCommand(1),
            PresetArm(
                armSubsystem,
                elevFine=self.toCallable(0),
                laddFine=self.toCallable(-0.4),
            ),
            WaitCommand(1),
        )

        self.addRequirements([armSubsystem])

    def toCallable(self, i):
        return i
