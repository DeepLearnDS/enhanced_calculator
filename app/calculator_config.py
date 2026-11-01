########################
# Calculator Config    #
########################

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional
from dotenv import load_dotenv
from app.exceptions import ConfigurationError
import codecs

# Load environment variables from a .env file into the program's environment
load_dotenv()


def get_project_root() -> Path:
    """
    Get the project root directory.

    This function determines the root directory of the project by navigating up
    the directory hierarchy from the current file's location.

    Returns:
        Path: The root directory path of the project.
    """
    # Get the directory of the current file (app/calculator_config.py)
    current_file = Path(__file__)
    # Navigate up two levels to reach the project root (from app/calculator_config.py to project root)
    return current_file.parent.parent


@dataclass
class CalculatorConfig:
    """
    Calculator configuration settings.

    This class manages all configuration parameters required by the calculator
    application, including directory paths, history size, auto-save preferences,
    calculation precision, maximum input values, and default encoding.

    Configuration can be set via environment variables or by passing parameters
    directly to the class constructor.
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    ):
        """Initialize calculator configuration."""

        project_root = get_project_root()

        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        # Read and validate maximum history size.
        try:
            value = max_history_size if max_history_size is not None else (
                os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
            )
            self.max_history_size = int(value)
        except (ValueError, TypeError):
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be a whole number"
            )

        # Read auto-save setting.
        if auto_save is not None:
            self.auto_save = auto_save
        else:
            auto_save_env = os.getenv(
                'CALCULATOR_AUTO_SAVE', 'true'
            ).lower()

            if auto_save_env not in ('true', 'false', '1', '0'):
                raise ConfigurationError(
                    "CALCULATOR_AUTO_SAVE must be true, false, 1, or 0"
                )

            self.auto_save = auto_save_env in ('true', '1')

        # Read and validate calculation precision.
        try:
            value = precision if precision is not None else (
                os.getenv('CALCULATOR_PRECISION', '10')
            )
            self.precision = int(value)
        except (ValueError, TypeError):
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be a whole number"
            )

        # Read maximum input value.
        try:
            value = max_input_value if max_input_value is not None else (
                os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
            )
            self.max_input_value = Decimal(str(value))
        except (ValueError, TypeError):
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be a valid number"
            )

        # Read default file encoding.
        self.default_encoding = (
            default_encoding
            if default_encoding is not None
            else os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        )

    @property
    def log_dir(self) -> Path:
        """
        Get log directory path.

        Determines the directory path where log files will be stored.

        Returns:
            Path: The log directory path.
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        """
        Get history directory path.

        Determines the directory path where calculation history files will be stored.

        Returns:
            Path: The history directory path.
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """
        Get history file path.

        Determines the file path for storing calculation history in CSV format.

        Returns:
            Path: The history file path.
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()

    @property
    def log_file(self) -> Path:
        """
        Get log file path.

        Determines the file path for storing log entries.

        Returns:
            Path: The log file path.
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
        """Validate all calculator configuration settings."""

        if not isinstance(self.max_history_size, int) or self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")

        if not isinstance(self.precision, int) or self.precision <= 0:
            raise ConfigurationError("precision must be positive")

        if not self.max_input_value.is_finite():
            raise ConfigurationError(
                "Maximum input value must be a finite number"
            )

        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")

        try:
            codecs.lookup(self.default_encoding)
        except LookupError:
            raise ConfigurationError(
                f"Unsupported encoding: {self.default_encoding}"
            )