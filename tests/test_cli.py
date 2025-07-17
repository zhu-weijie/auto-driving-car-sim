from unittest.mock import patch

from app.car import Car
from app.cli import CLI
from app.field import Field


def test_cli_ask_for_field_dimensions_success(capsys):
    with patch("builtins.input", return_value="10 10"):
        cli = CLI()
        field = cli._ask_for_field_dimensions()

    assert isinstance(field, Field)
    assert field.width == 10
    assert field.height == 10

    captured = capsys.readouterr()
    assert "You have created a field of 10 x 10." in captured.out


@patch("builtins.input", side_effect=["abc", "10", "10 0", "15 15"])
@patch("builtins.print")
def test_cli_ask_for_field_dimensions_reprompts_on_invalid(mock_print, mock_input):
    cli = CLI()
    field = cli._ask_for_field_dimensions()

    assert field.width == 15
    assert field.height == 15

    error_message = (
        "Invalid input. Please enter two positive integers separated by a space."
    )
    assert mock_print.call_count >= 3
    mock_print.assert_any_call(error_message)


@patch("app.cli.CLI._run_simulation")
@patch("app.cli.CLI._add_car")
@patch("builtins.input", side_effect=["1", "2"])
def test_cli_main_menu_calls_correct_methods(
    mock_input, mock_add_car, mock_run_simulation, capsys
):
    cli = CLI()
    cli.field = Field(10, 10)

    cli._show_main_menu()
    cli._show_main_menu()

    mock_add_car.assert_called_once()
    mock_run_simulation.assert_called_once()

    captured = capsys.readouterr()
    assert "[1] Add a car to field" in captured.out
    assert "[2] Run simulation" in captured.out


@patch("builtins.input", side_effect=["3", "abc", "1"])
@patch("app.cli.CLI._add_car")
def test_cli_main_menu_reprompts_on_invalid_input(mock_add_car, mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)

    cli._show_main_menu()

    mock_add_car.assert_called_once()

    captured = capsys.readouterr()
    assert "Invalid option. Please choose 1 or 2." in captured.out


@patch("builtins.input", side_effect=["A", "1 2 N", "FFR"])
def test_cli_add_car_happy_path(mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)

    cli._add_car()

    assert len(cli.cars) == 1
    assert len(cli.commands) == 1

    car = cli.cars[0]
    assert car.name == "A"
    assert car.x == 1
    assert car.y == 2
    assert car.direction == "N"
    assert cli.commands[0] == "FFR"

    captured = capsys.readouterr()
    assert "Your current list of cars are:" in captured.out
    assert "- A, (1,2) N, FFR" in captured.out


@patch(
    "builtins.input",
    side_effect=[
        "B",
        "10 10 N",
        "5 5 Z",
        "5 5 E",
        "LFRX",
        "LFR",
    ],
)
def test_cli_add_car_handles_all_invalid_inputs(mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)

    cli._add_car()

    assert len(cli.cars) == 1
    assert cli.cars[0].name == "B"
    assert cli.cars[0].x == 5
    assert cli.cars[0].y == 5
    assert cli.cars[0].direction == "E"
    assert cli.commands[0] == "LFR"

    captured = capsys.readouterr()
    assert "Position is outside the field boundaries." in captured.out
    assert "Invalid format." in captured.out
    assert "Commands can only contain 'F', 'L', 'R'." in captured.out


@patch("builtins.input", return_value="1")
@patch("app.simulation.Simulation.run")
def test_cli_run_simulation_success_scenario(mock_run, mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)
    car_A = Car("A", 1, 2, "N")
    final_car_A = Car("A", 5, 4, "S")
    cli.cars = [car_A]
    cli.commands = ["FFR..."]

    mock_run.return_value = {"status": "OK", "cars": [final_car_A]}

    cli._run_simulation()

    captured = capsys.readouterr()
    assert "- A, (1,2) N, FFR..." in captured.out
    assert "After simulation, the result is:" in captured.out
    assert "- A, (5,4) S" in captured.out
    assert "[1] Start over" in captured.out


@patch("builtins.input", return_value="2")
@patch("app.simulation.Simulation.run")
def test_cli_run_simulation_collision_scenario(mock_run, mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)
    cli.cars = [Car("A", 0, 0, "N"), Car("B", 0, 2, "S")]
    cli.commands = ["F", "F"]

    collided_car_A = Car("A", 0, 1, "N")
    collided_car_B = Car("B", 0, 1, "S")
    mock_run.return_value = {
        "status": "COLLISION",
        "step": 1,
        "location": (0, 1),
        "cars": [collided_car_A, collided_car_B],
    }

    cli._run_simulation()

    captured = capsys.readouterr()
    assert "After simulation, the result is:" in captured.out
    assert "- A, collides with B at (0,1) at step 1" in captured.out
    assert "- B, collides with A at (0,1) at step 1" in captured.out
