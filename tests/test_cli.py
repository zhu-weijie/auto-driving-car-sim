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
