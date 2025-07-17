import pytest

from app.car import Car


def test_car_initialization():
    car = Car(name="A", x=1, y=2, direction="N")
    assert car.name == "A"
    assert car.x == 1
    assert car.y == 2
    assert car.direction == "N"


@pytest.mark.parametrize("invalid_direction", ["X", "North", "s", "1"])
def test_car_invalid_direction_initialization(invalid_direction):
    with pytest.raises(ValueError, match="Direction must be one of N, E, S, W"):
        Car(name="B", x=0, y=0, direction=invalid_direction)


def test_car_representation():
    car = Car(name="C", x=5, y=8, direction="W")
    expected_repr = "Car(name=C, x=5, y=8, direction=W)"
    assert repr(car) == expected_repr


@pytest.mark.parametrize(
    "initial_direction, expected_direction",
    [("N", "W"), ("W", "S"), ("S", "E"), ("E", "N")],
)
def test_car_turn_left(initial_direction, expected_direction):
    car = Car(name="A", x=0, y=0, direction=initial_direction)
    car.turn_left()
    assert car.direction == expected_direction


@pytest.mark.parametrize(
    "initial_direction, expected_direction",
    [("N", "E"), ("E", "S"), ("S", "W"), ("W", "N")],
)
def test_car_turn_right(initial_direction, expected_direction):
    car = Car(name="A", x=0, y=0, direction=initial_direction)
    car.turn_right()
    assert car.direction == expected_direction


@pytest.mark.parametrize(
    "initial_direction, initial_pos, expected_pos",
    [
        ("N", (5, 5), (5, 6)),
        ("E", (5, 5), (6, 5)),
        ("S", (5, 5), (5, 4)),
        ("W", (5, 5), (4, 5)),
        ("N", (0, 0), (0, 1)),
    ],
)
def test_calculate_forward_position(initial_direction, initial_pos, expected_pos):
    car = Car(name="A", x=initial_pos[0], y=initial_pos[1], direction=initial_direction)
    calculated_pos = car.calculate_forward_position()
    assert calculated_pos == expected_pos
