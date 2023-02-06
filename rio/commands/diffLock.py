import commands2

from subsystems.drivesubsystem import DriveSubsystem


class DiffLock(commands2.CommandBase):
    def __init__(self, driveSubsystem: DriveSubsystem) -> None:
        super().__init__()

        self.driveSubsystem = driveSubsystem

        self.addRequirements([self.driveSubsystem])

    def initialize(self):
        # what needs to be done here is as follows according to Mark
        # the motors need to spin at an small difference
        # one oposite the other (per side)
        # this will make the robot be able to stay in place
        self.driveSubsystem.lock()  # TODO press F12 on lock

    def end(self, interrupted: bool) -> None:
        return True
