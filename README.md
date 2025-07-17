# Auto Driving Car Simulation

A simulation program for an autonomous driving car, built with Python using Test-Driven Development (TDD) and a modular, command-line interface.

This project allows users to define a rectangular field, add multiple cars with initial positions and commands, and run a turn-by-turn simulation that handles concurrent movement and collision detection.

## Features

-   Interactive Command-Line Interface (CLI)
-   Simultaneous multi-car simulation
-   Boundary checks for the simulation field
-   Step-by-step collision detection
-   Fully Dockerized for a consistent and reproducible environment
-   High test coverage for core logic
-   Clean code enforced by Black (formatter) and Ruff (linter)

## Project Structure

```
.
├── app/                # Main application source code (the 'app' package)
│   ├── car.py          # Car class
│   ├── cli.py          # Command-Line Interface class
│   ├── field.py        # Field class
│   ├── main.py         # Application entry point
│   └── simulation.py   # Simulation engine class
├── tests/              # Unit tests
│   ├── test_car.py
│   ├── test_cli.py
│   ├── test_field.py
│   └── test_simulation.py
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker build instructions
├── pyproject.toml      # Tool configuration (Black, Ruff)
└── requirements.txt    # Python dependencies
```

## Getting Started

This project is designed to be run with Docker and Docker Compose to ensure a consistent environment.

### Prerequisites

-   Docker
-   Docker Compose

### How to Run the Application

1.  **Build the Docker image**:
    ```bash
    docker compose build
    ```

2.  **Run the application interactively**:
    This command starts the CLI and allows you to interact with the simulation.
    ```bash
    docker compose run --rm app python -m app.main
    ```

### How to Run Tests and Linters

1.  **Run the full unit test suite**:
    ```bash
    docker compose run --rm app pytest
    ```

2.  **Run the linter (Ruff)**:
    ```bash
    docker compose run --rm app ruff check --fix .
    ```

3.  **Run the formatter (Black)**:
    ```bash
    docker compose run --rm app black .
    ```

## Test Coverage

The project was developed with a TDD approach, resulting in comprehensive test coverage for all core logic.

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
