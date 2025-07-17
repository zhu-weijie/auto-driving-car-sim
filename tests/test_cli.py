from unittest.mock import patch

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
