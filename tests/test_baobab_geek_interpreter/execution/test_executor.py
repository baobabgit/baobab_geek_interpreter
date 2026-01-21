"""Tests unitaires pour la classe Executor."""

import pytest

from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)
from baobab_geek_interpreter.execution.executor import Executor
from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.ast_node import (
    ArgumentNode,
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)


class TestExecutorBasics:
    """Tests de base pour Executor."""

    def test_executor_creation(self) -> None:
        """Test la création d'un exécuteur."""
        table = SymbolTable()
        executor = Executor(table)
        assert executor is not None

    def test_execute_service_not_found_raises(self) -> None:
        """Test qu'un service non trouvé lève une exception."""
        table = SymbolTable()
        executor = Executor(table)

        ast = ServiceCallNode("unknown", [])

        with pytest.raises(BaobabExecutionException, match="non trouvé"):
            executor.execute(ast)


class TestExecutorSimpleServices:
    """Tests pour l'exécution de services simples."""

    def test_execute_service_no_args(self) -> None:
        """Test l'exécution d'un service sans arguments."""
        table = SymbolTable()

        @service
        def get_constant() -> int:
            return 42

        table.register("get_constant", get_constant)
        executor = Executor(table)

        ast = ServiceCallNode("get_constant", [])
        result = executor.execute(ast)
        assert result == 42

    def test_execute_service_with_int_args(self) -> None:
        """Test l'exécution d'un service avec arguments entiers."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)
        executor = Executor(table)

        ast = ServiceCallNode(
            "add",
            [
                ArgumentNode(IntNode(10)),
                ArgumentNode(IntNode(20)),
            ],
        )
        result = executor.execute(ast)
        assert result == 30

    def test_execute_service_with_float_args(self) -> None:
        """Test l'exécution d'un service avec arguments flottants."""
        table = SymbolTable()

        @service
        def multiply(a: float, b: float) -> float:
            return a * b

        table.register("multiply", multiply)
        executor = Executor(table)

        ast = ServiceCallNode(
            "multiply",
            [
                ArgumentNode(FloatNode(2.5)),
                ArgumentNode(FloatNode(4.0)),
            ],
        )
        result = executor.execute(ast)
        assert result == 10.0

    def test_execute_service_with_string_args(self) -> None:
        """Test l'exécution d'un service avec arguments chaînes."""
        table = SymbolTable()

        @service
        def concat(a: str, b: str) -> str:
            return a + b

        table.register("concat", concat)
        executor = Executor(table)

        ast = ServiceCallNode(
            "concat",
            [
                ArgumentNode(StringNode("Hello")),
                ArgumentNode(StringNode(" World")),
            ],
        )
        result = executor.execute(ast)
        assert result == "Hello World"

    def test_execute_service_with_mixed_args(self) -> None:
        """Test l'exécution d'un service avec types mixtes."""
        table = SymbolTable()

        @service
        def format_message(count: int, price: float, name: str) -> str:
            return f"{count} x {name} = {price}"

        table.register("format_message", format_message)
        executor = Executor(table)

        ast = ServiceCallNode(
            "format_message",
            [
                ArgumentNode(IntNode(3)),
                ArgumentNode(FloatNode(9.99)),
                ArgumentNode(StringNode("apple")),
            ],
        )
        result = executor.execute(ast)
        assert result == "3 x apple = 9.99"


class TestExecutorArrays:
    """Tests pour l'exécution avec des tableaux."""

    def test_execute_service_with_int_array(self) -> None:
        """Test l'exécution d'un service avec tableau d'entiers."""
        table = SymbolTable()

        @service
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)

        table.register("sum_numbers", sum_numbers)
        executor = Executor(table)

        ast = ServiceCallNode(
            "sum_numbers",
            [ArgumentNode(ArrayNode([IntNode(1), IntNode(2), IntNode(3), IntNode(4)]))],
        )
        result = executor.execute(ast)
        assert result == 10

    def test_execute_service_with_float_array(self) -> None:
        """Test l'exécution d'un service avec tableau de flottants."""
        table = SymbolTable()

        @service
        def average(numbers: list[float]) -> float:
            return sum(numbers) / len(numbers) if numbers else 0.0

        table.register("average", average)
        executor = Executor(table)

        ast = ServiceCallNode(
            "average",
            [ArgumentNode(ArrayNode([FloatNode(1.5), FloatNode(2.5), FloatNode(3.5)]))],
        )
        result = executor.execute(ast)
        assert result == 2.5

    def test_execute_service_with_string_array(self) -> None:
        """Test l'exécution d'un service avec tableau de chaînes."""
        table = SymbolTable()

        @service
        def join_strings(words: list[str]) -> str:
            return " ".join(words)

        table.register("join_strings", join_strings)
        executor = Executor(table)

        ast = ServiceCallNode(
            "join_strings",
            [ArgumentNode(ArrayNode([StringNode("Hello"), StringNode("World")]))],
        )
        result = executor.execute(ast)
        assert result == "Hello World"

    def test_execute_service_with_empty_array(self) -> None:
        """Test l'exécution d'un service avec tableau vide."""
        table = SymbolTable()

        @service
        def count_items(items: list[int]) -> int:
            return len(items)

        table.register("count_items", count_items)
        executor = Executor(table)

        ast = ServiceCallNode(
            "count_items",
            [ArgumentNode(ArrayNode([]))],
        )
        result = executor.execute(ast)
        assert result == 0


class TestExecutorReturnTypes:
    """Tests pour différents types de retour."""

    def test_execute_service_returns_int(self) -> None:
        """Test un service retournant un entier."""
        table = SymbolTable()

        @service
        def get_age() -> int:
            return 25

        table.register("get_age", get_age)
        executor = Executor(table)

        ast = ServiceCallNode("get_age", [])
        result = executor.execute(ast)
        assert isinstance(result, int)
        assert result == 25

    def test_execute_service_returns_float(self) -> None:
        """Test un service retournant un flottant."""
        table = SymbolTable()

        @service
        def get_pi() -> float:
            return 3.14159

        table.register("get_pi", get_pi)
        executor = Executor(table)

        ast = ServiceCallNode("get_pi", [])
        result = executor.execute(ast)
        assert isinstance(result, float)
        assert result == 3.14159

    def test_execute_service_returns_string(self) -> None:
        """Test un service retournant une chaîne."""
        table = SymbolTable()

        @service
        def get_name() -> str:
            return "Alice"

        table.register("get_name", get_name)
        executor = Executor(table)

        ast = ServiceCallNode("get_name", [])
        result = executor.execute(ast)
        assert isinstance(result, str)
        assert result == "Alice"

    def test_execute_service_returns_list(self) -> None:
        """Test un service retournant une liste."""
        table = SymbolTable()

        @service
        def get_numbers() -> list[int]:
            return [1, 2, 3, 4, 5]

        table.register("get_numbers", get_numbers)
        executor = Executor(table)

        ast = ServiceCallNode("get_numbers", [])
        result = executor.execute(ast)
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4, 5]

    def test_execute_service_returns_none(self) -> None:
        """Test un service retournant None."""
        table = SymbolTable()

        @service
        def do_nothing() -> None:
            pass

        table.register("do_nothing", do_nothing)
        executor = Executor(table)

        ast = ServiceCallNode("do_nothing", [])
        result = executor.execute(ast)
        assert result is None


class TestExecutorExceptionHandling:
    """Tests pour la gestion des exceptions."""

    def test_execute_service_raises_exception(self) -> None:
        """Test qu'une exception du service est encapsulée."""
        table = SymbolTable()

        @service
        def divide(a: int, b: int) -> float:
            return a / b

        table.register("divide", divide)
        executor = Executor(table)

        ast = ServiceCallNode(
            "divide",
            [
                ArgumentNode(IntNode(10)),
                ArgumentNode(IntNode(0)),
            ],
        )

        with pytest.raises(BaobabExecutionException) as exc_info:
            executor.execute(ast)

        assert "divide" in str(exc_info.value)
        assert exc_info.value.service_name == "divide"
        assert exc_info.value.original_exception is not None
        assert isinstance(exc_info.value.original_exception, ZeroDivisionError)

    def test_execute_service_raises_custom_exception(self) -> None:
        """Test qu'une exception personnalisée est encapsulée."""
        table = SymbolTable()

        @service
        def validate_age(age: int) -> str:
            if age < 0:
                raise ValueError("Age cannot be negative")
            return "Valid"

        table.register("validate_age", validate_age)
        executor = Executor(table)

        ast = ServiceCallNode(
            "validate_age",
            [ArgumentNode(IntNode(-5))],
        )

        with pytest.raises(BaobabExecutionException) as exc_info:
            executor.execute(ast)

        assert "validate_age" in str(exc_info.value)
        assert exc_info.value.service_name == "validate_age"
        assert isinstance(exc_info.value.original_exception, ValueError)
        assert "negative" in str(exc_info.value.original_exception)


class TestExecutorVisitorMethods:
    """Tests pour les méthodes visit_* individuelles."""

    def test_visit_int(self) -> None:
        """Test la visite d'un nœud entier."""
        table = SymbolTable()
        executor = Executor(table)

        node = IntNode(42)
        result = executor.visit_int(node)
        assert result == 42

    def test_visit_float(self) -> None:
        """Test la visite d'un nœud flottant."""
        table = SymbolTable()
        executor = Executor(table)

        node = FloatNode(3.14)
        result = executor.visit_float(node)
        assert result == 3.14

    def test_visit_string(self) -> None:
        """Test la visite d'un nœud chaîne."""
        table = SymbolTable()
        executor = Executor(table)

        node = StringNode("hello")
        result = executor.visit_string(node)
        assert result == "hello"

    def test_visit_array(self) -> None:
        """Test la visite d'un nœud tableau."""
        table = SymbolTable()
        executor = Executor(table)

        node = ArrayNode([IntNode(1), IntNode(2), IntNode(3)])
        result = executor.visit_array(node)
        assert result == [1, 2, 3]

    def test_visit_argument(self) -> None:
        """Test la visite d'un nœud argument."""
        table = SymbolTable()
        executor = Executor(table)

        node = ArgumentNode(IntNode(42))
        result = executor.visit_argument(node)
        assert result == 42


class TestExecutorComplexScenarios:
    """Tests pour des scénarios complexes."""

    def test_execute_service_with_multiple_arrays(self) -> None:
        """Test l'exécution avec plusieurs tableaux."""
        table = SymbolTable()

        @service
        def merge_lists(a: list[int], b: list[int]) -> list[int]:
            return a + b

        table.register("merge_lists", merge_lists)
        executor = Executor(table)

        ast = ServiceCallNode(
            "merge_lists",
            [
                ArgumentNode(ArrayNode([IntNode(1), IntNode(2)])),
                ArgumentNode(ArrayNode([IntNode(3), IntNode(4)])),
            ],
        )
        result = executor.execute(ast)
        assert result == [1, 2, 3, 4]

    def test_execute_service_with_negative_numbers(self) -> None:
        """Test l'exécution avec nombres négatifs."""
        table = SymbolTable()

        @service
        def subtract(a: int, b: int) -> int:
            return a - b

        table.register("subtract", subtract)
        executor = Executor(table)

        ast = ServiceCallNode(
            "subtract",
            [
                ArgumentNode(IntNode(-10)),
                ArgumentNode(IntNode(-5)),
            ],
        )
        result = executor.execute(ast)
        assert result == -5

    def test_execute_service_complex_computation(self) -> None:
        """Test l'exécution d'un calcul complexe."""
        table = SymbolTable()

        @service
        def calculate(numbers: list[int], multiplier: float) -> float:
            return sum(numbers) * multiplier

        table.register("calculate", calculate)
        executor = Executor(table)

        ast = ServiceCallNode(
            "calculate",
            [
                ArgumentNode(ArrayNode([IntNode(1), IntNode(2), IntNode(3)])),
                ArgumentNode(FloatNode(2.5)),
            ],
        )
        result = executor.execute(ast)
        assert result == 15.0
