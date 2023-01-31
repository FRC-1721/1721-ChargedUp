import commands2

from subsystems.clawsubsystem import ClawSubsystem


class Clamp(commands2.CommandBase):
    def __init__(self, clawSubsystem: ClawSubsystem) -> None:
        super().__init__()

        self.clawSusystem = clawSubsystem

        # this gives us full control of the claw
        self.addRequirements([self.clawSusystem])

        # TODO Change me
        self.clawSusystem.setCurrentlimit(0.1)

    def initialize(self) -> None:
        self.clawSusystem.grab()

    def end(self, interrupted: bool) -> None:
        self.clawSusystem.release()
        return True
