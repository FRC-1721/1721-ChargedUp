import commands2

from subsystems.armsubsystem import ArmSubsystem


class Retract(commands2.CommandBase):
    def __init__(self, armSubsystem: ArmSubsystem) -> None:
        super().__init__()

        self.armSusystem = armSubsystem

        # this gives us full control of the arm
        self.addRequirements([self.armSusystem])

        # TODO Change me
        self.armSusystem.setCurrentlimit(1)

    def initialize(self) -> None:
        self.armSusystem.retract()

    def end(self, interrupted: bool) -> None:
        self.armSusystem.stop()
        return True
