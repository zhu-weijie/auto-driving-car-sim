from unittest.mock import patch

from app.car import Car
from app.cli import CLI
from app.field import Field


def test_cli_ask_for_field_dimensions_success(capsys):
    with patch("builtins.input", return_value="10 10"):
        cli = CLI()
        field = cli._ask_for_field_dimensions()
    assert isinstance(field, Field) and field.width == 10 and field.height == 10
    assert "You have created a field of 10 x 10." in capsys.readouterr().out


@patch("builtins.input", side_effect=["abc", "10 0", "15 15"])
@patch("builtins.print")
def test_cli_ask_for_field_dimensions_reprompts_on_invalid(mock_print, mock_input):
    cli = CLI()
    field = cli._ask_for_field_dimensions()
    assert field.width == 15 and field.height == 15
    mock_print.assert_any_call(
        "Invalid input. Please enter two positive integers separated by a space."
    )


@patch("app.cli.CLI._add_car")
@patch("builtins.input", return_value="1")
def test_cli_main_menu_chooses_add_car(mock_input, mock_add_car):
    cli = CLI()
    cli.field = Field(10, 10)
    result = cli._show_main_menu()
    mock_add_car.assert_called_once()
    assert result == "CONTINUE"


@patch("builtins.input", return_value="2")
def test_cli_main_menu_chooses_run_simulation(mock_input):
    cli = CLI()
    cli.field = Field(10, 10)
    result = cli._show_main_menu()
    assert result == "RUN_SIMULATION"


@patch("builtins.input", side_effect=["A", "1 2 N", "FFR"])
def test_cli_add_car_happy_path(mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)
    cli._add_car()
    assert len(cli.cars) == 1 and cli.cars[0].name == "A"
    assert "- A, (1,2) N, FFR" in capsys.readouterr().out


@patch("builtins.input", side_effect=["B", "10 10 N", "5 5 E", "LFR"])
def test_cli_add_car_handles_invalid_position(mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)
    cli._add_car()
    assert "Position is outside the field boundaries." in capsys.readouterr().out
    assert cli.cars[0].name == "B"


@patch("builtins.input", return_value="1")
@patch("app.simulation.Simulation.run")
def test_cli_run_simulation_success_scenario(mock_run, mock_input, capsys):
    cli = CLI()
    cli.field = Field(10, 10)
    final_car_A = Car("A", 5, 4, "S")
    cli.cars = [Car("A", 1, 2, "N")]
    cli.commands = ["FFR..."]
    mock_run.return_value = {"status": "OK", "cars": [final_car_A]}
    cli._run_simulation()
    captured = capsys.readouterr()
    assert "- A, (1,2) N, FFR..." in captured.out
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

    assert "- A, collides with B at (0, 1) at step 1" in captured.out
    assert "- B, collides with A at (0, 1) at step 1" in captured.out
