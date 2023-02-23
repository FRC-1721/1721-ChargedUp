[![Robot Workflow](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/build-workflow.yml/badge.svg)](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/build-workflow.yml)
[![Extras Workflow](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/extras-workflow.yml/badge.svg)](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/extras-workflow.yml)
[![Dashboard Workflow](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/dashboard-workflow.yml/badge.svg)](https://github.com/FRC-1721/1721-ChargedUp/actions/workflows/dashboard-workflow.yml)
[![Documentation Status](https://readthedocs.org/projects/1721-chargedup/badge/?version=latest)](https://1721-chargedup.readthedocs.io/en/latest/?badge=latest)

# [1721-ChargedUp](https://www.frc1721.org/)

Welcome to Tidal Force's 2023 robot, Rotom Toaster!

To get started, please see the `#software` channel on our discord or 
pm the lead of software Keegan directly.

## RobotPy

The RoboRIO (our main safety computer) runs RobotPy.

To get started developing:

```
cd rio
pipenv install
pipenv shell
make sim
```

# Dashboard

You must run the simulator or the robot if you want to test the dashboard!

```
cd dashboard
npm ci
make build
make run
```

# Documentation

```
cd docs
pipenv install -r requirements.txt
pipenv shell
make latexpdf
```
