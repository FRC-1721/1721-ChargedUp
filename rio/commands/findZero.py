import typing
import commands2

import rev

from subsystems.armsubsystem import ArmSubsystem


class FindZero(commands2.CommandBase):
    """
    Manually drives the arm subsystem to zero
    """

    def __init__(
        self,
        armSubsystem: ArmSubsystem,
    ) -> None:
        super().__init__()

        self.armSubsystem = armSubsystem

    def execute(self) -> None:
        self.armSubsystem.ascent(-0.12)
        self.armSubsystem.extension(-0.12)

    def end(self, interrupted: bool) -> None:
        pass
