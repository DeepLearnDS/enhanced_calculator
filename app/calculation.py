########################
# Calculation Model    #
########################

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    Value Object representing a single calculation.

    This class stores the operation performed, operands, result, and timestamp.
    Arithmetic operations are performed by the operation strategy classes.
    It provides methods for serialization, deserialization, and result formatting.
    """

    # Required fields
    operation: str          # The name of the operation (e.g., "Addition")
    operand1: Decimal       # The first operand in the calculation
    operand2: Decimal       # The second operand in the calculation

    # Fields with default values
    result: Decimal  # The result of the calculation, computed post-initialization
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Time when the calculation was performed


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert calculation to dictionary for serialization.

        This method transforms the Calculation instance into a dictionary format,
        facilitating easy storage and retrieval (e.g., saving to a file).

        Returns:
            Dict[str, Any]: A dictionary containing the calculation data in a serializable format.
        """
        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """Reconstruct a Calculation from saved history."""
        try:
            return Calculation(
                operation=data['operation'],
                operand1=Decimal(str(data['operand1'])),
                operand2=Decimal(str(data['operand2'])),
                result=Decimal(str(data['result'])),
                timestamp=datetime.datetime.fromisoformat(
                    data['timestamp']
                )
            )
        except (KeyError, InvalidOperation, ValueError, TypeError) as e:
            raise OperationError(
                f"Invalid calculation data: {str(e)}"
            ) from e

    def __str__(self) -> str:
        """
        Return string representation of calculation.

        Provides a human-readable representation of the calculation, showing the
        operation performed and its result.

        Returns:
            str: Formatted string showing the calculation and result.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"

    def __repr__(self) -> str:
        """
        Return detailed string representation of calculation.

        Provides a detailed and unambiguous string representation of the Calculation
        instance, useful for debugging.

        Returns:
            str: Detailed string showing all calculation attributes.
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check if two calculations are equal.

        Compares two Calculation instances to determine if they represent the same
        operation with identical operands and results.

        Args:
            other (object): Another calculation to compare with.

        Returns:
            bool: True if calculations are equal, False otherwise.
        """
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )

    def format_result(self, precision: int = 10) -> str:
        """Format the result using the specified decimal precision."""

        formatted_result = f"{self.result:.{precision}f}"

        return formatted_result.rstrip("0").rstrip(".") \
            if "." in formatted_result else formatted_result