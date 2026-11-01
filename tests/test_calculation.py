
import pytest
from decimal import Decimal
from datetime import datetime

from app.calculation import Calculation
from app.exceptions import OperationError


def test_addition():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )
    assert calc.result == Decimal("5")


def test_subtraction():
    calc = Calculation(
        operation="Subtraction",
        operand1=Decimal("5"),
        operand2=Decimal("3"),
        result=Decimal("2")
    )
    assert calc.result == Decimal("2")


def test_multiplication():
    calc = Calculation(
        operation="Multiplication",
        operand1=Decimal("4"),
        operand2=Decimal("2"),
        result=Decimal("8")
    )
    assert calc.result == Decimal("8")


def test_division():
    calc = Calculation(
        operation="Division",
        operand1=Decimal("8"),
        operand2=Decimal("2"),
        result=Decimal("4")
    )
    assert calc.result == Decimal("4")


def test_power():
    calc = Calculation(
        operation="Power",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("8")
    )
    assert calc.result == Decimal("8")


def test_root():
    calc = Calculation(
        operation="Root",
        operand1=Decimal("16"),
        operand2=Decimal("2"),
        result=Decimal("4")
    )
    assert calc.result == Decimal("4")


def test_to_dict():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    result_dict = calc.to_dict()

    assert result_dict == {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }

    calc = Calculation.from_dict(data)

    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }

    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_from_dict_missing_field():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5"
    }

    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(
        operation="Division",
        operand1=Decimal("1"),
        operand2=Decimal("3"),
        result=Decimal("0.3333333333333333")
    )

    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    calc1 = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    calc2 = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    calc3 = Calculation(
        operation="Subtraction",
        operand1=Decimal("5"),
        operand2=Decimal("3"),
        result=Decimal("2")
    )

    assert calc1 == calc2
    assert calc1 != calc3


def test_not_equal_to_other_type():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    assert calc != "not a calculation"


def test_string_representation():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    assert str(calc) == "Addition(2, 3) = 5"


def test_repr():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    assert "Calculation" in repr(calc)
    assert "result=5" in repr(calc)


def test_unknown_operation_is_stored():
    """
    Calculation stores the operation name.
    Operation validation belongs to the operation factory.
    """
    calc = Calculation(
        operation="Unknown",
        operand1=Decimal("5"),
        operand2=Decimal("3"),
        result=Decimal("0")
    )

    assert calc.operation == "Unknown"
