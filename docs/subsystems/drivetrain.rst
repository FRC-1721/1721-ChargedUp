The Drivetrain
##############

.. include:: ../resources/resources.rst


Introduction
============

|outreach|

.. figure:: resources/missing.png
  :width: 200
  :alt: The Drivetrain

  The drivetrain during construction

The tank drivetrain is tried and tested, even by us! During :ref:`Prototyping` we 
experimented with our kitbot drivetrain and used it as a solid base to train new members
with.


Prototyping
===========

|outreach|

.. figure:: resources/missing.png
  :width: 200
  :alt: The Drivetrain

  The kitbot/prototype drivetrain.


Software
=========

|software|

The drive base uses simple two wheel steering kinematics and an odometry with encoders, gyro and 
accelerometers to detect robot position.

Config Files
------------

.. literalinclude:: ../../rio/constants/robot_hardware.yaml
  :lines: 6-29
  :language: YAML

.. literalinclude:: ../../rio/constants/robot_pid.yaml
  :lines: 3-18
  :language: YAML


