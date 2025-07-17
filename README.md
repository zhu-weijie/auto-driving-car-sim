# Auto Driving Car Simulation

A simulation program for an autonomous driving car, built with Python using Test-Driven Development (TDD).

This project allows users to define a rectangular field, add multiple cars with initial positions and commands, and run a simulation that handles concurrent movement and collision detection.

## Features

-   Interactive Command-Line Interface (CLI)
-   Simultaneous multi-car simulation
-   Boundary checks
-   Collision detection
-   Fully Dockerized for consistent environment
-   Code quality enforced by Black and Ruff

## Test Coverage

The project is developed with TDD, resulting in comprehensive test coverage.

```bash
---------- coverage: platform linux, python 3.12.11-final-0 -----------
Name                Stmts   Miss  Cover
---------------------------------------
app/__init__.py         0      0   100%
app/car.py             24      0   100%
app/cli.py            122     22    82%
app/field.py            8      0   100%
app/main.py             4      4     0%
app/simulation.py      43      1    98%
---------------------------------------
TOTAL                 201     27    87%
```
