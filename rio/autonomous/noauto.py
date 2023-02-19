# commands2
import commands2

from commands2 import WaitCommand


class NoAuto(commands2.SequentialCommandGroup):
    def __init__(self) -> None:
        """
        extendo
        downo
        failo
        cryo
        """

        super().__init__(WaitCommand(2))
