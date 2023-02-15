import commands2

from subsystems.armsubsystem import ArmSubsystem


class Up(commands2.CommandBase):
    def __init__(self, armsubsystem: ArmSubsystem) -> None:
        super().__init__()

        self.armsubsystem = armsubsystem

        # this gives us full control of the claw
        self.addRequirements([self.armsubsystem])

        # TODO Change me
        self.armsubsystem.setCurrentlimit(10)

    def initialize(self) -> None:
        self.armsubsystem.up()

    def end(self, interrupted: bool) -> None:
        self.armsubsystem.upstop()
        return True
