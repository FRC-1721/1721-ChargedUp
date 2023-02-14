import commands2

from subsystems.clawsubsystem import ClawSubsystem


class Unclamp(commands2.CommandBase):
    def __init__(self, clawSubsystem: ClawSubsystem) -> None:
        super().__init__()

        self.clawSusystem = clawSubsystem

        # this gives us full control of the claw
        self.addRequirements([self.clawSusystem])

        # TODO Change me
        self.clawSusystem.setCurrentlimit(1)

    def initialize(self) -> None:
        self.clawSusystem.release()

    def end(self, interrupted: bool) -> None:
        self.clawSusystem.stop()
        return True
