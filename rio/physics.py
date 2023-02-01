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
    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        # Controller
        self.physics_controller = physics_controller

        # Robot
        self.robot = robot

        # Consts
        constants = getConstants("robot_physics")

        # Drivetrain motors (only simulating 2 out of 4)
        self.l_motor = robot.container.robotDrive.leftMotor1
        self.r_motor = robot.container.robotDrive.leftMotor2

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
        # self.l_motor.setBusVoltage(voltage) # Dosent work
        l_v = self.l_motor.getAppliedOutput()
        # self.r_motor.setBusVoltage(voltage) # Dosent work
        r_v = self.r_motor.getAppliedOutput()

        kS = 1  # Tuning value

        if l_v > kS:
            l_v -= kS
        elif l_v < -kS:
            l_v += kS
        else:
            l_v = 0

        if r_v > kS:
            r_v -= kS
        elif r_v < -kS:
            r_v += kS
        else:
            r_v = 0

        self.drivesim.setInputs(l_v, r_v * 0.80)
        self.drivesim.update(tm_diff)

        self.l_encoder.setPosition(self.drivesim.getLeftPosition())
        self.robot.container.robotDrive.simLVelocity = self.drivesim.getLeftVelocity()
        self.r_encoder.setPosition(self.drivesim.getRightPosition())
        self.robot.container.robotDrive.simRVelocity = self.drivesim.getRightVelocity()

        pose = self.drivesim.getPose()
        field.setRobotPose(pose)
        self.robot.container.robotDrive.simPose = pose

        # print(field.getRobotPose())
