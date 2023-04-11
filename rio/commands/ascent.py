import commands2


from subsystems.armsubsystem import ArmSubsystem


class Ascent(commands2.CommandBase):
    """
    Manually drives the arm subsystem to zero
    """

    def __init__(
        self,
        armSubsystem: ArmSubsystem,
        power,
    ) -> None:
        super().__init__()

        self.armSubsystem = armSubsystem
        self.power = power

        self.addRequirements([self.armSubsystem])

    def execute(self) -> None:
        self.armSubsystem.ascent(self.power)

    def end(self, interrupted: bool) -> None:
        pass
