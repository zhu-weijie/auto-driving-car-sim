import pytest

from app.car import Car
from app.field import Field
from app.simulation import Simulation


def test_simulation_run_single_car_success():
    field = Field(10, 10)
    car = Car(name="A", x=1, y=2, direction="N")
    commands = "FFRFFFFRRL"

    simulation = Simulation(field, [car], [commands])
    result = simulation.run()
    assert result["status"] == "OK"
    assert len(result["cars"]) == 1

    final_car_state = result["cars"][0]
    assert final_car_state.x == 5
    assert final_car_state.y == 4
    assert final_car_state.direction == "S"


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
    result = simulation.run()

    assert result["status"] == "OK"
    assert len(result["cars"]) == 1

    final_car_state = result["cars"][0]
    assert final_car_state.x == expected_x
    assert final_car_state.y == expected_y


def test_simulation_run_two_cars_success():
    field = Field(10, 10)
    car_A = Car(name="A", x=1, y=2, direction="N")
    commands_A = "RFRFRF"
    car_B = Car(name="B", x=7, y=8, direction="W")
    commands_B = "LFLFLF"

    simulation = Simulation(field, [car_A, car_B], [commands_A, commands_B])
    result = simulation.run()

    assert result["status"] == "OK"
    assert len(result["cars"]) == 2

    final_car_A_state = result["cars"][0]
    assert final_car_A_state.x == 1
    assert final_car_A_state.y == 1
    assert final_car_A_state.direction == "W"


def test_simulation_run_cars_with_different_command_lengths():
    field = Field(10, 10)
    car_A = Car(name="A", x=0, y=0, direction="N")
    commands_A = "FF"
    car_B = Car(name="B", x=5, y=5, direction="E")
    commands_B = "RFFL"

    simulation = Simulation(field, [car_A, car_B], [commands_A, commands_B])
    result = simulation.run()

    assert result["status"] == "OK"
    assert len(result["cars"]) == 2

    final_car_A_state = result["cars"][0]
    assert final_car_A_state.x == 0
    assert final_car_A_state.y == 2
    assert final_car_A_state.direction == "N"

    final_car_B_state = result["cars"][1]
    assert final_car_B_state.x == 5
    assert final_car_B_state.y == 3
    assert final_car_B_state.direction == "E"


def test_simulation_detects_head_on_collision():
    field = Field(10, 10)
    car_A = Car(name="A", x=5, y=3, direction="N")
    commands_A = "F"
    car_B = Car(name="B", x=5, y=5, direction="S")
    commands_B = "F"

    simulation = Simulation(field, [car_A, car_B], [commands_A, commands_B])
    result = simulation.run()

    assert result["status"] == "COLLISION"
    assert result["step"] == 1
    assert result["location"] == (5, 4)

    assert len(result["cars"]) == 2
    collided_car_names = {car.name for car in result["cars"]}
    assert collided_car_names == {"A", "B"}
