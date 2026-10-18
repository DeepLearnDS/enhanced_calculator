
########################
# Calculator REPL      #
########################

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory
from app.terminal_colors import error, info, success


def calculator_repl():
    """
    Command-line interface for the calculator.

    Supports arithmetic operations, calculation history, undo/redo,
    saving and loading history, and color-coded terminal messages.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(info("Calculator started. Type 'help' for commands."))

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == "help":
                    print("\nAvailable commands:")
                    print(
                        "  add, subtract, multiply, divide - Basic arithmetic"
                    )
                    print("  power - Raise a number to a power")
                    print("  root - Calculate an nth root")
                    print("  modulus - Calculate the remainder")
                    print("  int_divide - Perform integer division")
                    print("  percent - Calculate (first / second) * 100")
                    print("  abs_diff - Calculate absolute difference")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  help - Display available commands")
                    print("  exit - Save history and exit")
                    continue

                if command == "exit":
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(success("History saved successfully."))
                    except Exception as e:
                        print(error(f"Warning: Could not save history: {e}"))

                    print(info("Goodbye!"))
                    break

                if command == "history":
                    history = calc.show_history()

                    if not history:
                        print(info("No calculations in history."))
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == "clear":
                    calc.clear_history()
                    print(success("History cleared"))
                    continue

                if command == "undo":
                    if calc.undo():
                        print(success("Operation undone."))
                    else:
                        print(info("Nothing to undo"))
                    continue

                if command == "redo":
                    if calc.redo():
                        print(success("Operation redone."))
                    else:
                        print(info("Nothing to redo"))
                    continue

                if command == "save":
                    try:
                        calc.save_history()
                        print(success("History saved successfully."))
                    except Exception as e:
                        print(error(f"Error saving history: {e}"))
                    continue

                if command == "load":
                    try:
                        calc.load_history()
                        print(success("History loaded successfully."))
                    except Exception as e:
                        print(error(f"Error loading history: {e}"))
                    continue

                calculation_commands = [
                    "add",
                    "subtract",
                    "multiply",
                    "divide",
                    "power",
                    "root",
                    "modulus",
                    "int_divide",
                    "percent",
                    "abs_diff",
                ]

                if command in calculation_commands:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")

                        a = input("First number: ").strip()
                        if a.lower() == "cancel":
                            print(info("Operation cancelled."))
                            continue

                        b = input("Second number: ").strip()
                        if b.lower() == "cancel":
                            print(info("Operation cancelled."))
                            continue

                        # Create the operation using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize Decimal results for display
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(success(f"\nResult: {result}"))

                    except (ValidationError, OperationError, ValueError) as e:
                        print(error(f"Error: {e}"))

                    except Exception as e:
                        print(error(f"Unexpected error: {e}"))

                    continue

                # Handle unknown commands
                print(
                    error(
                        f"Unknown command: '{command}'. "
                        "Type 'help' for available commands."
                    )
                )

            except KeyboardInterrupt:
                print(info("\nOperation cancelled."))
                continue

            except EOFError:
                print(info("\nInput terminated. Exiting..."))
                break

            except Exception as e:
                print(error(f"Error: {e}"))
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(error(f"Fatal error: {e}"))
        logging.exception("Fatal error in calculator REPL")
        raise
