import pytest

from app.car import Car
from app.field import Field
from app.simulation import Simulation


def test_simulation_run_single_car_success():
    field = Field(10, 10)
    car = Car(name="A", x=1, y=2, direction="N")
    commands = "FFRFFFFRRL"

    simulation = Simulation(field, [car], [commands])
    simulation.run()

    assert car.x == 5
    assert car.y == 4
    assert car.direction == "S"


@pytest.mark.parametrize(
    "start_x, start_y, direction, commands, expected_x, expected_y",
    [
        (0, 0, "S", "F", 0, 0),
        (0, 0, "W", "F", 0, 0),
        (9, 9, "N", "F", 9, 9),
        (9, 9, "E", "F", 9, 9),
        (5, 9, "N", "FF", 5, 9),
        (9, 5, "E", "FF", 9, 5),
    ],
)
def test_simulation_car_stops_at_boundary(
    start_x, start_y, direction, commands, expected_x, expected_y
):
    field = Field(10, 10)
    car = Car(name="A", x=start_x, y=start_y, direction=direction)

    simulation = Simulation(field, [car], [commands])
    simulation.run()

    assert car.x == expected_x
    assert car.y == expected_y


def test_simulation_run_two_cars_success():
    field = Field(10, 10)
    car_A = Car(name="A", x=1, y=2, direction="N")
    commands_A = "RFRFRF"
    car_B = Car(name="B", x=7, y=8, direction="W")
    commands_B = "LFLFLF"

    simulation = Simulation(field, [car_A, car_B], [commands_A, commands_B])
    simulation.run()

    assert car_A.x == 2 and car_A.y == 3 and car_A.direction == "E"
    assert car_B.x == 6 and car_B.y == 7 and car_B.direction == "S"


def test_simulation_run_cars_with_different_command_lengths():
    field = Field(10, 10)
    car_A = Car(name="A", x=0, y=0, direction="N")
    commands_A = "FF"
    car_B = Car(name="B", x=5, y=5, direction="E")
    commands_B = "RFFL"

    simulation = Simulation(field, [car_A, car_B], [commands_A, commands_B])
    simulation.run()

    assert car_A.x == 0 and car_A.y == 2 and car_A.direction == "N"
    assert car_B.x == 7 and car_B.y == 4 and car_B.direction == "N"
