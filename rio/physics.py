import hal
import wpilib
import wpilib.simulation
from robotpy_ext.common_drivers.distance_sensors_sim import SharpIR2Y0A41Sim

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import wpimath
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor

import dataclasses
import math
import typing

# Constants
from constants.constants import getConstants


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface, robot: "RotomToaster"):
        # Controller
        self.physics_controller = physics_controller

        # Consts
        constants = getConstants("robot_physics")

        # Drivetrain motors (only simulating 2 out of 4)
        self.l_motor = robot.container.robotDrive.leftMotor1
        self.r_motor = robot.container.robotDrive.rightMotor1

        self.l_encoder = robot.container.robotDrive.leftEncoder
        self.r_encoder = robot.container.robotDrive.rightEncoder

        # Virtual drivetrain, all of these are blank numbers!
        system = LinearSystemId.identifyDrivetrainSystem(
            constants["kV_linear"],
            constants["kA_linear"],
            constants["kV_angular"],
            constants["kA_angular"],
        )

        self.drivesim = wpilib.simulation.DifferentialDrivetrainSim(
            system,
            # The robot's trackwidth, which is the distance between the wheels on the left side
            # and those on the right side. The units is meters.
            constants["kTrackWidth"],
            DCMotor.NEO(4),
            constants["kGearRatio"],
            # The radius of the drivetrain wheels in meters.
            constants["kWheelDist"],
        )

    def update_sim(self, now: float, tm_diff: float) -> None:
        # Simulated voltage of the robot
        voltage = wpilib.simulation.RoboRioSim.getVInVoltage()

        # Virtual Field
        field = self.physics_controller.field

        # Motor voltages
        l_v = self.l_motor.getAppliedOutput() * voltage
        r_v = self.r_motor.getAppliedOutput() * voltage

        self.drivesim.setInputs(l_v, r_v)
        self.drivesim.update(tm_diff)

        # print(f"{l_v}, {r_v}")
        self.l_encoder.setPosition(self.drivesim.getLeftPosition())
        self.r_encoder.setPosition(self.drivesim.getRightPosition())

        pose = self.drivesim.getPose()
        field.setRobotPose(pose)

        # print(field.getRobotPose())
