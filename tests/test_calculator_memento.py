from datetime import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_to_dict():
    """Test converting a CalculatorMemento to a dictionary."""

    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3")
    )

    timestamp = datetime(2026, 10, 5, 12, 0, 0)

    memento = CalculatorMemento(
        history=[calc],
        timestamp=timestamp
    )

    result = memento.to_dict()

    assert result["history"] == [calc.to_dict()]
    assert result["timestamp"] == timestamp.isoformat()


def test_memento_from_dict():
    """Test restoring a CalculatorMemento from a dictionary."""

    timestamp = datetime(2026, 10, 5, 12, 0, 0)

    data = {
        "history": [
            {
                "operation": "Addition",
                "operand1": "2",
                "operand2": "3",
                "result": "5",
                "timestamp": timestamp.isoformat()
            }
        ],
        "timestamp": timestamp.isoformat()
    }

    memento = CalculatorMemento.from_dict(data)

    assert isinstance(memento, CalculatorMemento)
    assert len(memento.history) == 1

    calc = memento.history[0]

    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")
    assert memento.timestamp == timestamp