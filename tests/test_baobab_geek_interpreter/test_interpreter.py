"""Tests unitaires pour la classe Interpreter."""

import pytest

from baobab_geek_interpreter import Interpreter, service
from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)
from baobab_geek_interpreter.exceptions.lexical_exception import (
    BaobabLexicalAnalyserException,
)
from baobab_geek_interpreter.exceptions.semantic_exception import (
    BaobabSemanticAnalyserException,
)
from baobab_geek_interpreter.exceptions.syntax_exception import (
    BaobabSyntaxAnalyserException,
)


class TestInterpreterBasics:
    """Tests de base pour Interpreter."""

    def test_interpreter_creation(self) -> None:
        """Test la création d'un interpréteur."""
        interpreter = Interpreter()
        assert interpreter is not None

    def test_list_services_empty(self) -> None:
        """Test que la liste des services est vide au départ."""
        interpreter = Interpreter()
        assert interpreter.list_services() == []

    def test_has_service_false_initially(self) -> None:
        """Test qu'aucun service n'existe initialement."""
        interpreter = Interpreter()
        assert interpreter.has_service("add") is False


class TestInterpreterServiceRegistration:
    """Tests pour l'enregistrement de services."""

    def test_register_service(self) -> None:
        """Test l'enregistrement d'un service."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        interpreter.register_service("add", add)
        assert interpreter.has_service("add") is True
        assert "add" in interpreter.list_services()

    def test_register_multiple_services(self) -> None:
        """Test l'enregistrement de plusieurs services."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        @service
        def multiply(a: int, b: int) -> int:
            return a * b

        interpreter.register_service("add", add)
        interpreter.register_service("multiply", multiply)

        assert interpreter.has_service("add") is True
        assert interpreter.has_service("multiply") is True
        assert len(interpreter.list_services()) == 2

    def test_register_services_from_module(self) -> None:
        """Test l'enregistrement automatique depuis un module."""

        # Créer un module simulé
        class FakeModule:
            @service
            def service1(x: int) -> int:
                return x * 2

            @service
            def service2(x: int) -> int:
                return x * 3

            def not_a_service(x: int) -> int:
                return x

        interpreter = Interpreter()
        interpreter.register_services(FakeModule())

        assert interpreter.has_service("service1") is True
        assert interpreter.has_service("service2") is True
        assert interpreter.has_service("not_a_service") is False

    def test_clear_services(self) -> None:
        """Test la suppression de tous les services."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        interpreter.register_service("add", add)
        assert len(interpreter.list_services()) == 1

        interpreter.clear_services()
        assert len(interpreter.list_services()) == 0
        assert interpreter.has_service("add") is False


class TestInterpreterExecution:
    """Tests pour l'exécution de services."""

    def test_interpret_simple_addition(self) -> None:
        """Test l'interprétation d'une addition simple."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        interpreter.register_service("add", add)
        result = interpreter.interpret("add(10, 20)")
        assert result == 30

    def test_interpret_string_concat(self) -> None:
        """Test l'interprétation d'une concaténation."""
        interpreter = Interpreter()

        @service
        def concat(a: str, b: str) -> str:
            return a + b

        interpreter.register_service("concat", concat)
        result = interpreter.interpret('concat("Hello", " World")')
        assert result == "Hello World"

    def test_interpret_float_multiplication(self) -> None:
        """Test l'interprétation d'une multiplication."""
        interpreter = Interpreter()

        @service
        def multiply(a: float, b: float) -> float:
            return a * b

        interpreter.register_service("multiply", multiply)
        result = interpreter.interpret("multiply(2.5, 4.0)")
        assert result == 10.0

    def test_interpret_with_array(self) -> None:
        """Test l'interprétation avec un tableau."""
        interpreter = Interpreter()

        @service
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)

        interpreter.register_service("sum_numbers", sum_numbers)
        result = interpreter.interpret("sum_numbers([1, 2, 3, 4, 5])")
        assert result == 15

    def test_interpret_mixed_types(self) -> None:
        """Test l'interprétation avec types mixtes."""
        interpreter = Interpreter()

        @service
        def format_message(count: int, price: float, name: str) -> str:
            return f"{count} x {name} = ${price:.2f}"

        interpreter.register_service("format_message", format_message)
        result = interpreter.interpret('format_message(3, 9.99, "apple")')
        assert result == "3 x apple = $9.99"


class TestInterpreterErrors:
    """Tests pour la gestion des erreurs."""

    def test_interpret_lexical_error(self) -> None:
        """Test qu'une erreur lexicale est levée."""
        interpreter = Interpreter()

        with pytest.raises(BaobabLexicalAnalyserException):
            interpreter.interpret("add(10, @)")

    def test_interpret_syntax_error(self) -> None:
        """Test qu'une erreur syntaxique est levée."""
        interpreter = Interpreter()

        with pytest.raises(BaobabSyntaxAnalyserException):
            interpreter.interpret("add(10, )")

    def test_interpret_semantic_error_unknown_service(self) -> None:
        """Test qu'une erreur sémantique est levée pour un service inconnu."""
        interpreter = Interpreter()

        with pytest.raises(BaobabSemanticAnalyserException, match="Service inconnu"):
            interpreter.interpret("unknown_service(10)")

    def test_interpret_semantic_error_wrong_types(self) -> None:
        """Test qu'une erreur sémantique est levée pour des types incorrects."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        interpreter.register_service("add", add)

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            interpreter.interpret('add(10, "20")')

    def test_interpret_execution_error(self) -> None:
        """Test qu'une erreur d'exécution est levée."""
        interpreter = Interpreter()

        @service
        def divide(a: int, b: int) -> float:
            return a / b

        interpreter.register_service("divide", divide)

        with pytest.raises(BaobabExecutionException):
            interpreter.interpret("divide(10, 0)")


class TestInterpreterComplexScenarios:
    """Tests pour des scénarios complexes."""

    def test_interpret_negative_numbers(self) -> None:
        """Test l'interprétation avec nombres négatifs."""
        interpreter = Interpreter()

        @service
        def subtract(a: int, b: int) -> int:
            return a - b

        interpreter.register_service("subtract", subtract)
        result = interpreter.interpret("subtract(-10, -5)")
        assert result == -5

    def test_interpret_empty_array(self) -> None:
        """Test l'interprétation avec tableau vide."""
        interpreter = Interpreter()

        @service
        def count_items(items: list[int]) -> int:
            return len(items)

        interpreter.register_service("count_items", count_items)
        result = interpreter.interpret("count_items([])")
        assert result == 0

    def test_interpret_large_array(self) -> None:
        """Test l'interprétation avec grand tableau."""
        interpreter = Interpreter()

        @service
        def max_value(numbers: list[int]) -> int:
            return max(numbers) if numbers else 0

        interpreter.register_service("max_value", max_value)
        result = interpreter.interpret("max_value([5, 2, 9, 1, 7, 3, 8, 4, 6])")
        assert result == 9

    def test_interpret_service_returns_list(self) -> None:
        """Test l'interprétation avec service retournant une liste."""
        interpreter = Interpreter()

        @service
        def create_range(start: int, end: int) -> list[int]:
            return list(range(start, end))

        interpreter.register_service("create_range", create_range)
        result = interpreter.interpret("create_range(1, 6)")
        assert result == [1, 2, 3, 4, 5]

    def test_interpret_service_no_return(self) -> None:
        """Test l'interprétation avec service sans retour."""
        interpreter = Interpreter()

        executed = []

        @service
        def log_message(message: str) -> None:
            executed.append(message)

        interpreter.register_service("log_message", log_message)
        result = interpreter.interpret('log_message("Test")')
        assert result is None
        assert executed == ["Test"]


class TestInterpreterRealWorld:
    """Tests pour des cas d'usage réels."""

    def test_interpret_calculate_total(self) -> None:
        """Test un calcul de total réel."""
        interpreter = Interpreter()

        @service
        def calculate_total(prices: list[float], tax_rate: float) -> float:
            subtotal = sum(prices)
            return subtotal * (1 + tax_rate)

        interpreter.register_service("calculate_total", calculate_total)
        result = interpreter.interpret("calculate_total([10.0, 20.0, 30.0], 0.2)")
        assert result == 72.0

    def test_interpret_filter_words(self) -> None:
        """Test un filtrage de mots."""
        interpreter = Interpreter()

        @service
        def filter_long_words(words: list[str], min_length: int) -> list[str]:
            return [w for w in words if len(w) >= min_length]

        interpreter.register_service("filter_long_words", filter_long_words)
        result = interpreter.interpret('filter_long_words(["hi", "hello", "hey", "world"], 5)')
        assert result == ["hello", "world"]

    def test_interpret_format_report(self) -> None:
        """Test un formatage de rapport."""
        interpreter = Interpreter()

        @service
        def format_report(title: str, count: int, values: list[float]) -> str:
            avg = sum(values) / len(values) if values else 0
            return f"{title}: {count} items, average = {avg:.2f}"

        interpreter.register_service("format_report", format_report)
        result = interpreter.interpret('format_report("Sales", 3, [100.0, 200.0, 300.0])')
        assert result == "Sales: 3 items, average = 200.00"
