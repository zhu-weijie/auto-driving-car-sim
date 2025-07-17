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
