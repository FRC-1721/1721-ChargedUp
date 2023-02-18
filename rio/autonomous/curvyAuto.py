# commands2
import commands2

from commands2 import WaitCommand

# sub syss
from subsystems.armsubsystem import ArmSubsystem

# commands and autonomous
from autonomous.crossLinePath import CrossLinePath
from commands.manualArm import ManualArm


class CurvyAuto(commands2.SequentialCommandGroup):
    def __init__(self, armSubsystem: ArmSubsystem) -> None:
        """
        extendo
        downo
        failo
        cryo
        """

        # self.addRequirements([armSubsystem])

        super().__init__(
            ManualArm(armSubsystem, elevatorPower=1, ladderPower=0),
            WaitCommand(1),
            ManualArm(armSubsystem, elevatorPower=0, ladderPower=-0.4),
            WaitCommand(1),
        )
