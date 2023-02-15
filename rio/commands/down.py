import commands2

from subsystems.armsubsystem import ArmSubsystem


class Down(commands2.CommandBase):
    def __init__(self, armsubsystem: ArmSubsystem) -> None:
        super().__init__()

        self.armsubsystem = armsubsystem

        # this gives us full control of the claw
        self.addRequirements([self.armsubsystem])

    def initialize(self) -> None:
        self.armsubsystem.down()
        print("working piss off")

    def end(self, interrupted: bool) -> None:
        self.armsubsystem.upstop()
        return True
