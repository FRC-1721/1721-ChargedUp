import commands2

from wpimath import geometry


class FlyByWire(commands2.CommandBase):
    def __init__(self) -> None:
        pass

    def debug(self, drivetrain):
        print(geometry.Rotation2d.fromDegrees(drivetrain.imu.getYaw()))
        print(geometry.Rotation2d.fromDegrees(drivetrain.imu.getPitch()))
        print(drivetrain.imu.getRawGyro())
