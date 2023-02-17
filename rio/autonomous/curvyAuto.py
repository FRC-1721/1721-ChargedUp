# commands2
import commands2

from commands2 import WaitCommand

# sub syss
from subsystems.armsubsystem import ArmSubsystem

# commands and autonomous
from autonomous.crossLinePath import CrossLinePath
from commands.extend import Extend
from commands.down import Down


class CurvyAuto(commands2.SequentialCommandGroup):
    def __init_(self, armSubsystem: ArmSubsystem) -> None:
        """
        extendo
        downo
        failo
        cryo
        """
        super().__init__(
            Extend(armSubsystem),
            WaitCommand(1),
            Down(armSubsystem),
            WaitCommand(1),
        )
