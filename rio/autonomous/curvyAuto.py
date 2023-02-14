# commands2
import commands2

from commands2 import WaitCommand

# commands and autonomous
from autonomous.crossLinePath import CrossLinePath
from commands.extend import Extend
from commands.retract import Retract
from commands.unclamp import Unclamp


class CurvyAuto(commands2.SequentialCommandGroup):
    def __init_(
        self,
    ) -> None:
        """
        This is the auto that leaves the comunity
        and goes back onto the switch
        """
        super().__init__(
            Extend(),
            WaitCommand(),
            Unclamp(),
            WaitCommand(2),
            Retract(),
            WaitCommand(2),
            CrossLinePath(2),
        )