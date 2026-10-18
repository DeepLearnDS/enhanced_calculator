# Enhanced Calculator

## Project Description
This project is an enhanced calculator built with Python. It uses object-oriented programming, design patterns, input validation, logging, and automated testing.

## Features
- Basic operations: addition, subtraction, multiplication, and division.
- Advanced operations: power, root, modulus, integer division, percentage, and absolute difference.
- Factory pattern for creating operations.
- Memento pattern for undo and redo.
- Observer pattern for logging and automatically saving calculations.
- CSV history using Pandas.
- Environment configuration using `.env`.
- Custom exceptions and input validation.
- Color-coded terminal output using Colorama.

## Requirements
- Python 3.12
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:DeepLearnDS/enhanced_calculator.git
   cd enhanced_calculator
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment on Ubuntu/WSL:

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure the environment variables in your `.env` file. Use the project's default settings if provided.

## Run the Calculator

Run the following command:

```bash
python main.py
```

Use the `help` command inside the calculator to see the available commands and operations.

## Testing

Run all tests with coverage:

```bash
python -m pytest --cov=app --cov-fail-under=90
```

The project is expected to maintain at least 90% test coverage.

## Continuous Integration

GitHub Actions automatically runs the tests when changes are pushed to the `main` branch or when a pull request targets `main`.

## Project Structure

- `app/` – Calculator logic, operations, configuration, history, and validation.
- `tests/` – Automated tests.
- `.github/workflows/tests.yml` – GitHub Actions workflow.
- `.env` – Local environment configuration.
- `main.py` – Application entry point.
- `requirements.txt` – Project dependencies.
