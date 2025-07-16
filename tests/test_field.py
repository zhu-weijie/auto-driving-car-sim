import pytest

from app.field import Field


def test_field_initialization():
    field = Field(10, 20)
    assert field.width == 10
    assert field.height == 20


@pytest.mark.parametrize(
    "width, height, x, y, expected",
    [
        (10, 10, 5, 5, True),  # Point inside
        (10, 10, 0, 0, True),  # Bottom-left corner
        (10, 10, 9, 9, True),  # Top-right corner
        (10, 10, 0, 9, True),  # Top-left corner
        (10, 10, 9, 0, True),  # Bottom-right corner
        (10, 10, -1, 5, False),  # Negative x
        (10, 10, 5, -1, False),  # Negative y
        (10, 10, 10, 5, False),  # x equals width (out of bounds)
        (10, 10, 5, 10, False),  # y equals height (out of bounds)
        (10, 10, 15, 15, False),  # x and y out of bounds
    ],
)
def test_is_within_bounds(width, height, x, y, expected):
    field = Field(width, height)
    assert field.is_within_bounds(x, y) == expected
