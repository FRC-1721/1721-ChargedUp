import commands2
from enum import Enum
import wpilib

from wpilib import RobotBase

from subsystems.drivesubsystem import DriveSubsystem


class cmds(Enum):
    FORWARD = 1
    BACKWARD = 2
    RIGHT = 3
    LEFT = 4


def parseLine(line: str):
    inp = line.split()
    ret = ["?", 0]

    # Parse cmd
    try:
        if inp[0] == "FORWARD":
            ret[0] = cmds.FORWARD
        if inp[0] == "BACK":
            ret[0] = cmds.BACKWARD
        if inp[0] == "RIGHT":
            ret[0] = cmds.RIGHT
        if inp[0] == "LEFT":
            ret[0] = cmds.LEFT
    except IndexError:
        return ret

    # Parse arg
    try:
        ret[1] = int(inp[1])
    except ValueError:
        pass

    return ret


class KidsAuto(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()

        # Load an instance of drivetrain
        self.drive = drive

        # Load custom myAuto.txt
        if RobotBase.isReal():
            path = "/home/lvuser/py/autonomous/"
        else:
            path = "autonomous/"

        with open(path + "kidsAuto.txt") as fp:
            self.lines = fp.readlines()
        self.curline = 0

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

        print("Kids Auto Started")

    def initialize(self) -> None:
        self.backgroundTimer.reset()

    def execute(self) -> None:
        cmd = parseLine(self.lines[self.curline])
        print(f"KA: Running line {cmd}")

        if cmd[0] == cmds.FORWARD:
            self.drive.arcadeDrive(
                0.2,
                0,
            )
        elif cmd[0] == cmds.BACKWARD:
            self.drive.arcadeDrive(
                -0.2,
                0,
            )
        elif cmd[0] == cmds.RIGHT:
            self.drive.arcadeDrive(
                0,
                0.3,
            )
        elif cmd[0] == cmds.LEFT:
            self.drive.arcadeDrive(
                0,
                -0.3,
            )

        if self.backgroundTimer.hasElapsed(cmd[1]):
            self.curline += 1
            self.backgroundTimer.reset()

    def end(self, interrupted: bool) -> None:
        # self.drive.arcadeDrive(0, 0)
        print("KA: Done!")

    def isFinished(self) -> bool:
        return self.curline >= len(self.lines)

    # def isFinished(self) -> bool:
    #     if self.time != -1 and self.backgroundTimer.hasElapsed(self.time):
    #         return True
    #     print("finished")
