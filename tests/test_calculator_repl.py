import pytest
from unittest.mock import Mock, patch

from app.calculator_repl import calculator_repl
from app.exceptions import ValidationError


@pytest.fixture
def calc_mock():
    """Create a mocked Calculator for isolated REPL tests."""
    calc = Mock()
    calc.show_history.return_value = []
    calc.undo.return_value = False
    calc.redo.return_value = False
    return calc


def run_repl(calc, inputs):
    """Run the REPL with mocked calculator and user input."""
    with patch('app.calculator_repl.Calculator', return_value=calc), \
         patch('builtins.input', side_effect=inputs), \
         patch('builtins.print') as mock_print:
        calculator_repl()

    return mock_print


def test_exit_when_save_fails(calc_mock):
    """Test exit when history cannot be saved."""
    calc_mock.save_history.side_effect = Exception("disk full")

    mock_print = run_repl(calc_mock, ['exit'])

    mock_print.assert_any_call(
        "Warning: Could not save history: disk full"
    )
    mock_print.assert_any_call("Goodbye!")


def test_history_empty(calc_mock):
    """Test displaying an empty history."""
    calc_mock.show_history.return_value = []

    mock_print = run_repl(calc_mock, ['history', 'exit'])

    mock_print.assert_any_call("No calculations in history")


def test_history_with_entries(calc_mock):
    """Test displaying existing history."""
    calc_mock.show_history.return_value = [
        "Addition(2, 3) = 5"
    ]

    mock_print = run_repl(calc_mock, ['history', 'exit'])

    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. Addition(2, 3) = 5")


def test_clear_history_command(calc_mock):
    """Test the clear command."""
    mock_print = run_repl(calc_mock, ['clear', 'exit'])

    calc_mock.clear_history.assert_called_once()
    mock_print.assert_any_call("History cleared")


@pytest.mark.parametrize(
    "undo_result, expected_message",
    [
        (True, "Operation undone"),
        (False, "Nothing to undo")
    ]
)
def test_undo_command(calc_mock, undo_result, expected_message):
    """Test both successful and unsuccessful undo."""
    calc_mock.undo.return_value = undo_result

    mock_print = run_repl(calc_mock, ['undo', 'exit'])

    mock_print.assert_any_call(expected_message)


@pytest.mark.parametrize(
    "redo_result, expected_message",
    [
        (True, "Operation redone"),
        (False, "Nothing to redo")
    ]
)
def test_redo_command(calc_mock, redo_result, expected_message):
    """Test both successful and unsuccessful redo."""
    calc_mock.redo.return_value = redo_result

    mock_print = run_repl(calc_mock, ['redo', 'exit'])

    mock_print.assert_any_call(expected_message)


def test_save_command_success(calc_mock):
    """Test successfully saving history."""
    mock_print = run_repl(
        calc_mock,
        ['save', EOFError()]
    )

    calc_mock.save_history.assert_called_once()
    mock_print.assert_any_call(
        "History saved successfully"
    )


def test_save_command_error(calc_mock):
    """Test an error while saving history."""
    calc_mock.save_history.side_effect = Exception(
        "save failed"
    )

    mock_print = run_repl(
        calc_mock,
        ['save', EOFError()]
    )

    mock_print.assert_any_call(
        "Error saving history: save failed"
    )


def test_load_command_success(calc_mock):
    """Test successfully loading history."""
    mock_print = run_repl(
        calc_mock,
        ['load', EOFError()]
    )

    calc_mock.load_history.assert_called_once()
    mock_print.assert_any_call(
        "History loaded successfully"
    )


def test_load_command_error(calc_mock):
    """Test an error while loading history."""
    calc_mock.load_history.side_effect = Exception(
        "load failed"
    )

    mock_print = run_repl(
        calc_mock,
        ['load', EOFError()]
    )

    mock_print.assert_any_call(
        "Error loading history: load failed"
    )


def test_operation_cancel_first_number(calc_mock):
    """Test cancelling before entering the first number."""
    mock_print = run_repl(
        calc_mock,
        ['add', 'cancel', 'exit']
    )

    mock_print.assert_any_call("Operation cancelled")
    calc_mock.perform_operation.assert_not_called()


def test_operation_cancel_second_number(calc_mock):
    """Test cancelling before entering the second number."""
    mock_print = run_repl(
        calc_mock,
        ['add', '2', 'cancel', 'exit']
    )

    mock_print.assert_any_call("Operation cancelled")
    calc_mock.perform_operation.assert_not_called()


def test_operation_validation_error(calc_mock):
    """Test a known validation error."""
    calc_mock.perform_operation.side_effect = (
        ValidationError("bad input")
    )

    mock_print = run_repl(
        calc_mock,
        ['add', 'abc', '2', EOFError()]
    )

    mock_print.assert_any_call("Error: bad input")


def test_operation_unexpected_error(calc_mock):
    """Test an unexpected calculation error."""
    calc_mock.perform_operation.side_effect = (
        RuntimeError("boom")
    )

    mock_print = run_repl(
        calc_mock,
        ['add', '2', '3', EOFError()]
    )

    mock_print.assert_any_call(
        "Unexpected error: boom"
    )


def test_unknown_command(calc_mock):
    """Test an unknown REPL command."""
    mock_print = run_repl(
        calc_mock,
        ['mystery', 'exit']
    )

    mock_print.assert_any_call(
        "Unknown command: 'mystery'. "
        "Type 'help' for available commands."
    )


def test_keyboard_interrupt(calc_mock):
    """Test Ctrl+C handling."""
    mock_print = run_repl(
        calc_mock,
        [KeyboardInterrupt(), 'exit']
    )

    mock_print.assert_any_call(
        "\nOperation cancelled"
    )


def test_eof_error(calc_mock):
    """Test Ctrl+D / EOF handling."""
    mock_print = run_repl(
        calc_mock,
        [EOFError()]
    )

    mock_print.assert_any_call(
        "\nInput terminated. Exiting..."
    )


def test_unexpected_input_error(calc_mock):
    """Test an unexpected error in the REPL loop."""
    mock_print = run_repl(
        calc_mock,
        [
            RuntimeError("input failed"),
            EOFError()
        ]
    )

    mock_print.assert_any_call(
        "Error: input failed"
    )


def test_fatal_initialization_error():
    """Test failure while initializing Calculator."""
    with patch(
        'app.calculator_repl.Calculator',
        side_effect=RuntimeError("init failed")
    ), patch(
        'builtins.print'
    ) as mock_print, patch(
        'app.calculator_repl.logging.error'
    ) as mock_logging_error:

        with pytest.raises(
            RuntimeError,
            match="init failed"
        ):
            calculator_repl()

        mock_print.assert_any_call(
            "Fatal error: init failed"
        )

        mock_logging_error.assert_called_once_with(
            "Fatal error in calculator REPL: init failed"
        )