# commands2
import commands2

from commands2 import WaitCommand

# sub syss
from subsystems.armsubsystem import ArmSubsystem

# commands and autonomous
from autonomous.crossLinePath import CrossLinePath
from commands.extend import Extend
from commands.down import Down


from subsystems.drivesubsystem import DriveSubsystem


class SimpleAuto(commands2.SequentialCommandGroup):
    def __init__(self, drive: DriveSubsystem) -> None:
        self.drive = drive

        super().__init__()
        pass
