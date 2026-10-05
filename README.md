# Assignment 5 - Enhanced Calculator Application

This project is an enhanced command-line calculator built with Python.

It extends the calculator from previous modules by adding advanced design patterns, calculation history, undo/redo, CSV data management with pandas, configuration settings, error handling, and automated testing.

## Features

The calculator supports the following arithmetic operations:

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root

It also includes several additional commands:

- `help` - Display available commands
- `history` - Show calculation history
- `clear` - Clear calculation history
- `undo` - Undo the previous calculation
- `redo` - Redo an undone calculation
- `save` - Save calculation history to a CSV file
- `load` - Load calculation history from a CSV file
- `exit` - Exit the calculator

## Design Patterns

This project uses several design patterns to organize the calculator and make the code easier to maintain.

### Factory Pattern

The Factory pattern is used to create operation objects based on the operation selected by the user.

For example, the factory can create addition, subtraction, multiplication, division, power, and root operations.

### Strategy Pattern

Different arithmetic operations are implemented as interchangeable strategies.

The calculator can switch between different operation strategies without changing the main calculator logic.

### Observer Pattern

The Observer pattern is used to monitor calculation history and respond to calculation events.

This helps manage history updates and automatic saving.

### Memento Pattern

The Memento pattern stores previous calculator states.

This allows the calculator to support the `undo` and `redo` commands.

### Facade Pattern

The `Calculator` class provides a simplified interface for interacting with the different parts of the application.

The REPL can use the Calculator class without directly managing history, operations, configuration, and data storage.

## Data Management with pandas

Calculation history is managed using pandas DataFrames.

The application can:

- Convert calculation history into a DataFrame
- Save calculation history to CSV
- Load previous calculation history from CSV
- Automatically save history based on configuration settings

## Project Structure

```text
Assignment5/
│
├── app/
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── calculator_repl.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   └── operations.py
│
├── tests/
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl.py
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_operations.py
│   └── test_validators.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

Python 3.13 is recommended for this project.

Clone the repository:

```bash
git clone git@github.com:Xiaodu7/Assignment5.git
cd Assignment5
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Linux or macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If `pip` is not available in the virtual environment, `uv` can also be used:

```bash
uv venv --python 3.13 venv
source venv/bin/activate
uv pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These values control settings such as the maximum history size, automatic saving, and file encoding.

## Running the Calculator

Run the application with:

```bash
python main.py
```

After the calculator starts, enter a command such as:

```text
add
```

The program will ask for the numbers needed for the calculation.

You can also use commands such as:

```text
help
history
clear
undo
redo
save
load
exit
```

## Error Handling

The calculator includes error handling for invalid user input and calculation errors.

Examples include:

- Division by zero
- Invalid operations
- Invalid numeric input
- File save/load errors
- Configuration errors

The project demonstrates both LBYL (Look Before You Leap) and EAFP (Easier to Ask Forgiveness than Permission) approaches to error handling.

## Testing

The project uses `pytest` for unit and parameterized testing.

Run all tests with:

```bash
pytest
```

The current test suite contains:

```text
138 tests
```

All tests pass successfully.

## Test Coverage

The project uses `pytest-cov` to measure code coverage.

Current test coverage:

```text
TOTAL: 100%
```

All application modules currently have 100% test coverage.

The project is configured so that the test suite fails if coverage falls below 100%.

## GitHub Actions

GitHub Actions automatically runs the test suite whenever code is pushed to the repository.

The workflow:

1. Sets up Python 3.13
2. Installs the project dependencies
3. Runs pytest
4. Measures code coverage
5. Requires 100% test coverage

This helps make sure the calculator continues to work correctly after changes are made.

## Technologies Used

- Python 3.13
- pandas
- pytest
- pytest-cov
- python-dotenv
- Git
- GitHub
- GitHub Actions

## Assignment Requirements Completed

This project includes the major requirements for Module 5:

- Object-oriented Python design
- REPL command-line interface
- Addition, subtraction, multiplication, division, power, and root operations
- Factory design pattern
- Strategy design pattern
- Observer design pattern
- Memento design pattern
- Facade design pattern
- pandas DataFrame history management
- CSV save and load functionality
- Environment variable configuration
- LBYL and EAFP error handling
- Unit testing
- Parameterized testing
- 100% code coverage
- GitHub Actions continuous integration