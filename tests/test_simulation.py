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
    "start_x, start_y, direction, commands",
    [
        (0, 0, "S", "F"),
        (0, 0, "W", "F"),
        (9, 9, "N", "FF"),
        (9, 9, "E", "RFFF"),
    ],
)
def test_simulation_car_stops_at_boundary(start_x, start_y, direction, commands):
    field = Field(10, 10)
    car = Car(name="A", x=start_x, y=start_y, direction=direction)
    initial_pos = (car.x, car.y)

    simulation = Simulation(field, [car], [commands])
    simulation.run()

    if direction == "S" or direction == "W":
        assert (car.x, car.y) == initial_pos
    elif direction == "N":
        assert (car.x, car.y) == (9, 9)
    elif direction == "E":
        assert (car.x, car.y) == (9, 9)
