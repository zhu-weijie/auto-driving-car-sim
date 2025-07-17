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
